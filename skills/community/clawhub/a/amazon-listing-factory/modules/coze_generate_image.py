#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

WORKFLOW_ID = os.environ.get("COZE_WORKFLOW_ID", "").strip()
COZE_TOKEN = os.environ.get("COZE_TOKEN", "").strip()
COZE_API_URL = os.environ.get("COZE_API_URL", "https://api.coze.cn/v1/workflow/run").strip()

DEFAULT_RATIO = "1:1"
DEFAULT_RESOLUTION = "1K"
DEFAULT_CONNECTOR_ID = "1024"

TOOLBOX_ROOT = Path(os.environ.get("AI_TOOLBOX_ROOT", str(Path(__file__).resolve().parents[3])))
FEISHU_HELPER = str(TOOLBOX_ROOT / "toolbox" / "tools" / "feishu_send_image_from_url.py")
DEFAULT_RECEIVE_ID = os.environ.get("FEISHU_DEFAULT_RECEIVE_ID", "").strip()
DEFAULT_RECEIVE_ID_TYPE = os.environ.get("FEISHU_DEFAULT_RECEIVE_ID_TYPE", "open_id").strip()
DEFAULT_WORKFLOW_KEY = (os.environ.get("MIHE_KEY", "").strip() or os.environ.get("COZE_IMAGE_WORKFLOW_KEY", "").strip())
RUN_LOG_PATH = str(Path(__file__).resolve().parent / "runtime.log")


def output(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def append_runtime_log(payload: dict):
    try:
        from datetime import datetime
        line = {"ts": datetime.now().isoformat(timespec="seconds"), **payload}
        with open(RUN_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")
    except Exception:
        pass


def try_parse_json(text: str):
    text = (text or "").strip()
    if not text:
        return None
    if not ((text.startswith("{") and text.endswith("}")) or (text.startswith("[") and text.endswith("]"))):
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


def extract_urls(text: str):
    return re.findall(r'https?://[^\s,，]+', text or "")


def is_debug_request(text: str) -> bool:
    t = (text or "").strip().lower()
    keys = [
        "调试生图",
        "检查生图环境",
        "debug image",
        "debug coze",
        "debug env",
        "生图调试",
    ]
    return any(k in t for k in keys)


def normalize_text(raw: str):
    raw = (raw or "").strip()
    for prefix in [
        "调试生图：", "调试生图:", "调试生图",
        "生成图片：", "生成图片:", "生成图片",
        "生图：", "生图:", "生图",
        "coze生成图片",
        "用coze工作流生成图片",
        "画图：", "画图:", "画图"
    ]:
        if raw.startswith(prefix):
            return raw[len(prefix):].strip()
    return raw


def detect_runtime_receive_target_from_env():
    candidates = [
        ("OPENCLAW_FEISHU_OPEN_ID", "open_id"),
        ("OPENCLAW_FEISHU_SENDER_OPEN_ID", "open_id"),
        ("OPENCLAW_OPEN_ID", "open_id"),
        ("FEISHU_OPEN_ID", "open_id"),
        ("SENDER_OPEN_ID", "open_id"),
        ("OPEN_ID", "open_id"),
        ("USER_OPEN_ID", "open_id"),

        ("OPENCLAW_FEISHU_USER_ID", "user_id"),
        ("OPENCLAW_FEISHU_SENDER_USER_ID", "user_id"),
        ("OPENCLAW_USER_ID", "user_id"),
        ("FEISHU_USER_ID", "user_id"),
        ("SENDER_USER_ID", "user_id"),
        ("USER_ID", "user_id"),

        ("OPENCLAW_FEISHU_UNION_ID", "union_id"),
        ("OPENCLAW_UNION_ID", "union_id"),
        ("FEISHU_UNION_ID", "union_id"),
        ("SENDER_UNION_ID", "union_id"),
        ("UNION_ID", "union_id"),

        ("OPENCLAW_FEISHU_CHAT_ID", "chat_id"),
        ("OPENCLAW_CHAT_ID", "chat_id"),
        ("FEISHU_CHAT_ID", "chat_id"),
        ("CHAT_ID", "chat_id"),
    ]

    for env_name, receive_id_type in candidates:
        value = os.environ.get(env_name, "").strip()
        if value:
            return {
                "receive_id": value,
                "receive_id_type": receive_id_type,
                "source": f"env:{env_name}",
                "chat_id": os.environ.get("OPENCLAW_FEISHU_CHAT_ID", "").strip() or os.environ.get("CHAT_ID", "").strip(),
                "chat_type": os.environ.get("OPENCLAW_FEISHU_CHAT_TYPE", "").strip(),
            }

    return {
        "receive_id": "",
        "receive_id_type": "",
        "source": "",
        "chat_id": "",
        "chat_type": "",
    }


def detect_runtime_receive_target_from_tmux():
    try:
        proc = subprocess.run(
            ["tmux", "capture-pane", "-pt", "openclaw", "-S", "-300"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if proc.returncode != 0:
            return {"receive_id": "", "receive_id_type": "", "source": "", "chat_id": "", "chat_type": ""}

        text = proc.stdout or ""
        lines = text.splitlines()

        pattern = re.compile(
            r"received message from (ou_[A-Za-z0-9]+) in (oc_[A-Za-z0-9]+) \(([^)]+)\)"
        )

        for line in reversed(lines):
            m = pattern.search(line)
            if m:
                sender_open_id = m.group(1)
                chat_id = m.group(2)
                chat_type = m.group(3)
                if sender_open_id:
                    return {
                        "receive_id": sender_open_id,
                        "receive_id_type": "open_id",
                        "source": "tmux:openclaw",
                        "chat_id": chat_id,
                        "chat_type": chat_type,
                    }
        return {"receive_id": "", "receive_id_type": "", "source": "", "chat_id": "", "chat_type": ""}
    except Exception:
        return {"receive_id": "", "receive_id_type": "", "source": "", "chat_id": "", "chat_type": ""}


def detect_runtime_receive_target():
    env_hit = detect_runtime_receive_target_from_env()
    if env_hit["receive_id"]:
        return env_hit

    tmux_hit = detect_runtime_receive_target_from_tmux()
    if tmux_hit["receive_id"]:
        return tmux_hit

    return {
        "receive_id": "",
        "receive_id_type": "",
        "source": "",
        "chat_id": "",
        "chat_type": "",
    }


def parse_natural_language(text: str):
    raw = normalize_text(text)
    runtime_target = detect_runtime_receive_target()

    result = {
        "prompt": "",
        "ratio": DEFAULT_RATIO,
        "resolution": DEFAULT_RESOLUTION,
        "image_urls": [],
        "key": DEFAULT_WORKFLOW_KEY,
        "receive_id": runtime_target["receive_id"] or DEFAULT_RECEIVE_ID,
        "receive_id_type": runtime_target["receive_id_type"] or DEFAULT_RECEIVE_ID_TYPE,
        "receive_target_source": runtime_target["source"] or ("env:FEISHU_DEFAULT_RECEIVE_ID" if DEFAULT_RECEIVE_ID else ""),
        "chat_id": runtime_target["chat_id"],
        "chat_type": runtime_target["chat_type"],
        "link_only": False,
        "label": "",
    }

    maybe_json = try_parse_json(raw)
    if isinstance(maybe_json, dict):
        result["prompt"] = maybe_json.get("prompt", "") or ""
        result["ratio"] = maybe_json.get("ratio", DEFAULT_RATIO) or DEFAULT_RATIO
        result["resolution"] = maybe_json.get("resolution", DEFAULT_RESOLUTION) or DEFAULT_RESOLUTION
        result["image_urls"] = maybe_json.get("image_urls", []) or []
        result["key"] = maybe_json.get("key", result["key"]) or result["key"]
        result["link_only"] = bool(maybe_json.get("link_only", False))
        result["label"] = maybe_json.get("label", "") or ""

        explicit_receive_id = maybe_json.get("receive_id", "") or ""
        explicit_receive_id_type = maybe_json.get("receive_id_type", "") or ""
        if explicit_receive_id:
            result["receive_id"] = explicit_receive_id
            result["receive_id_type"] = explicit_receive_id_type or "open_id"
            result["receive_target_source"] = "input:json"

        return result

    kv_pattern = re.compile(
        r'(\b(?:prompt|ratio|resolution|key|image_urls|refs|receive_id|receive_id_type|link_only|label)\b)\s*=\s*(".*?"|\'.*?\'|\[.*?\]|[^ ]+)'
    )
    matches = list(kv_pattern.finditer(raw))
    if matches:
        consumed_spans = []

        for m in matches:
            k = m.group(1)
            v = m.group(2).strip()
            consumed_spans.append((m.start(), m.end()))

            if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                v = v[1:-1]

            if k == "prompt":
                result["prompt"] = v
            elif k == "ratio":
                result["ratio"] = v
            elif k == "resolution":
                result["resolution"] = v
            elif k == "key":
                result["key"] = v
            elif k in ("image_urls", "refs"):
                if v.startswith("[") and v.endswith("]"):
                    try:
                        arr = json.loads(v)
                        if isinstance(arr, list):
                            result["image_urls"] = [str(x).strip() for x in arr if str(x).strip()]
                    except Exception:
                        pass
                else:
                    result["image_urls"] = [x.strip() for x in v.split(",") if x.strip()]
            elif k == "receive_id":
                result["receive_id"] = v
                result["receive_target_source"] = "input:kv"
            elif k == "receive_id_type":
                result["receive_id_type"] = v
            elif k == "link_only":
                result["link_only"] = str(v).strip().lower() in {"1", "true", "yes", "y"}
            elif k == "label":
                result["label"] = v

        if not result["prompt"]:
            tmp = raw
            for s, e in reversed(consumed_spans):
                tmp = tmp[:s] + " " + tmp[e:]
            tmp = re.sub(r"\s+", " ", tmp).strip()
            if tmp:
                result["prompt"] = tmp

        return result

    ratio_match = re.search(r'(?:比例|ratio)\s*[:： ]?\s*([0-9]+\s*[:：]\s*[0-9]+)', raw, re.I)
    if ratio_match:
        result["ratio"] = ratio_match.group(1).replace("：", ":").replace(" ", "")

    resolution_match = re.search(r'(?:分辨率|resolution)\s*[:： ]?\s*([0-9]+[kK])', raw, re.I)
    if resolution_match:
        result["resolution"] = resolution_match.group(1).upper()

    urls = extract_urls(raw)
    if urls:
        result["image_urls"] = urls

    cleaned = raw
    cleaned = re.sub(r'(?:比例|ratio)\s*[:： ]?\s*[0-9]+\s*[:：]\s*[0-9]+', '', cleaned, flags=re.I)
    cleaned = re.sub(r'(?:分辨率|resolution)\s*[:： ]?\s*[0-9]+[kK]', '', cleaned, flags=re.I)
    cleaned = re.sub(r'(?:参考图|参考链接|参考)\s*[:： ]?', '', cleaned)
    cleaned = re.sub(r'https?://[^\s,，]+', '', cleaned)
    cleaned = re.sub(r'[，,]+', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip(" ，,")
    result["prompt"] = cleaned or raw

    return result


def first_url(value):
    if isinstance(value, str):
        if value.startswith("http://") or value.startswith("https://"):
            return value
        maybe = try_parse_json(value)
        if maybe is not None:
            return first_url(maybe)
        return None

    if isinstance(value, dict):
        for k in ["url", "image_url", "image", "output", "result", "data"]:
            if k in value:
                hit = first_url(value[k])
                if hit:
                    return hit
        for _, v in value.items():
            hit = first_url(v)
            if hit:
                return hit
        return None

    if isinstance(value, list):
        for item in value:
            hit = first_url(item)
            if hit:
                return hit
        return None

    return None


def debug_env_snapshot():
    runtime_target = detect_runtime_receive_target()
    return {
        "COZE_WORKFLOW_ID_set": bool(WORKFLOW_ID),
        "COZE_TOKEN_set": bool(COZE_TOKEN),
        "MIHE_KEY_set": bool(DEFAULT_WORKFLOW_KEY),
        "FEISHU_DEFAULT_RECEIVE_ID": DEFAULT_RECEIVE_ID,
        "FEISHU_DEFAULT_RECEIVE_ID_TYPE": DEFAULT_RECEIVE_ID_TYPE,
        "FEISHU_APP_ID_set": bool(os.environ.get("FEISHU_APP_ID", "").strip()),
        "FEISHU_APP_SECRET_set": bool(os.environ.get("FEISHU_APP_SECRET", "").strip()),
        "runtime_receive_target": runtime_target,
    }


def validate_required_config():
    missing = []
    if not WORKFLOW_ID:
        missing.append("COZE_WORKFLOW_ID")
    if not COZE_TOKEN:
        missing.append("COZE_TOKEN")
    if not DEFAULT_WORKFLOW_KEY:
        missing.append("MIHE_KEY")
    return missing


def call_coze_once(parameters: dict):
    body = {
        "workflow_id": WORKFLOW_ID,
        "parameters": parameters,
        "connector_id": DEFAULT_CONNECTOR_ID
    }

    req = urllib.request.Request(
        COZE_API_URL,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {COZE_TOKEN}",
            "Content-Type": "application/json"
        }
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def call_coze(parameters: dict, retries: int = 1):
    last_error = None
    for attempt in range(retries + 1):
        try:
            return call_coze_once(parameters)
        except urllib.error.HTTPError as e:
            try:
                err_body = e.read().decode("utf-8")
            except Exception:
                err_body = str(e)
            last_error = {
                "ok": False,
                "stage": "http_request",
                "error": "调用 Coze 工作流失败",
                "http_status": getattr(e, "code", None),
                "details": err_body
            }
        except Exception as e:
            last_error = {
                "ok": False,
                "stage": "http_request",
                "error": "调用 Coze 工作流异常",
                "details": str(e)
            }

        if attempt < retries:
            time.sleep(1)

    output(last_error or {"ok": False, "error": "调用 Coze 工作流失败"})
    sys.exit(1)


def send_image_to_(image_url: str, receive_id: str, receive_id_type: str):
    if not os.path.exists(FEISHU_HELPER):
        return {"ok": False, "error": "飞书发送脚本不存在"}

    if not receive_id:
        return {"ok": False, "error": "缺少接收人，且未识别到当前消息发送者"}

    cmd = [
        "python3",
        FEISHU_HELPER,
        "--image-url", image_url,
        "--receive-id", receive_id,
        "--receive-id-type", receive_id_type or "open_id",
    ]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except Exception as e:
        return {"ok": False, "error": "调用飞书发送脚本异常", "details": str(e)}

    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()

    if proc.returncode != 0:
        return {
            "ok": False,
            "error": "飞书发送失败",
            "returncode": proc.returncode,
            "stdout": stdout,
            "stderr": stderr,
        }

    try:
        data = json.loads(stdout) if stdout else {}
    except Exception:
        data = {
            "ok": False,
            "error": "飞书发送脚本输出不是合法 JSON",
            "stdout": stdout,
            "stderr": stderr,
        }

    return data


def main():
    user_input = sys.argv[1] if len(sys.argv) > 1 else ""
    debug_mode = is_debug_request(user_input)

    if user_input.strip() in ["检查生图环境", "debug image env", "debug env"]:
        output({"ok": True, "env": debug_env_snapshot()})
        return

    missing = validate_required_config()
    if missing:
        payload = {"ok": False, "answer": "生图配置缺失，请检查 skill 配置。"}
        if debug_mode:
            payload["missing"] = missing
            payload["env"] = debug_env_snapshot()
        output(payload)
        return

    parsed = parse_natural_language(user_input)
    receive_id = parsed.get("receive_id", "")
    receive_id_type = parsed.get("receive_id_type", "") or "open_id"
    receive_target_source = parsed.get("receive_target_source", "")
    link_only = bool(parsed.get("link_only", False))

    if user_input.strip() in ["查看生图路由", "检查生图接收人", "检查当前接收人", "probe image route"]:
        output({
            "ok": True,
            "answer": "生图路由已输出。",
            "receive_id": receive_id,
            "receive_id_type": receive_id_type,
            "receive_target_source": receive_target_source,
            "chat_id": parsed.get("chat_id", ""),
            "chat_type": parsed.get("chat_type", ""),
            "env": debug_env_snapshot(),
        })
        return

    if not parsed.get("prompt"):
        output({
            "ok": False,
            "answer": "请直接描述你想生成的图片。"
        })
        return

    parameters = {
        "key": parsed.get("key", ""),
        "prompt": parsed.get("prompt", ""),
        "image_urls": parsed.get("image_urls", []),
        "ratio": parsed.get("ratio", DEFAULT_RATIO),
        "resolution": parsed.get("resolution", DEFAULT_RESOLUTION),
    }

    resp = call_coze(parameters, retries=1)

    code = resp.get("code", 0)
    if code not in (0, "0", None):
        payload = {"ok": False, "answer": "图片生成失败，请稍后重试。"}
        if debug_mode:
            payload["code"] = code
            payload["msg"] = resp.get("msg")
            payload["debug_url"] = resp.get("debug_url")
        output(payload)
        return

    data = resp.get("data")
    if isinstance(data, str):
        maybe = try_parse_json(data)
        if maybe is not None:
            data = maybe

    image_url = first_url(data) or first_url(resp)
    if not image_url:
        output({
            "ok": False,
            "answer": "图片已生成，但结果解析失败。"
        })
        return

    append_runtime_log({
        "user_input": user_input,
        "prompt": parsed.get("prompt"),
        "label": parsed.get("label", ""),
        "receive_id": receive_id,
        "receive_id_type": receive_id_type,
        "receive_target_source": receive_target_source,
        "chat_id": parsed.get("chat_id", ""),
        "chat_type": parsed.get("chat_type", ""),
        "link_only": link_only,
        "image_url": image_url,
    })

    if link_only:
        output({
            "ok": True,
            "answer": "图片链接已生成。",
            "prompt": parsed.get("prompt"),
            "label": parsed.get("label", ""),
            "url": image_url,
            "link_only": True
        })
        return

    _result = send_image_to_(image_url, receive_id, receive_id_type)

    if not _result.get("ok"):
        if debug_mode:
            output({
                "ok": False,
                "answer": "图片已生成，但发送失败。",
                "prompt": parsed.get("prompt"),
                "url": image_url,
                "debug_url": resp.get("debug_url"),
                "receive_id": receive_id,
                "receive_id_type": receive_id_type,
                "receive_target_source": receive_target_source,
                "_send": _result,
                "env": debug_env_snapshot(),
            })
        else:
            output({
                "ok": False,
                "answer": "图片已生成，但发送失败。"
            })
        return

    if debug_mode:
        debug_answer = (
            "[调试模式]\n"
            "图片已发送。\n"
            f"prompt={parsed.get('prompt')}\n"
            f"ratio={parsed.get('ratio', DEFAULT_RATIO)}\n"
            f"resolution={parsed.get('resolution', DEFAULT_RESOLUTION)}\n"
            f"receive_id_type={receive_id_type}\n"
            f"receive_target_source={receive_target_source}\n"
            f"coze=ok\n"
            f"={'ok' if _result.get('ok') else 'fail'}\n"
            f"debug_url={resp.get('debug_url')}"
        )
        output({
            "ok": True,
            "answer": debug_answer,
            "prompt": parsed.get("prompt"),
            "ratio": parsed.get("ratio", DEFAULT_RATIO),
            "resolution": parsed.get("resolution", DEFAULT_RESOLUTION),
            "url": image_url,
            "debug_url": resp.get("debug_url"),
            "receive_id": receive_id,
            "receive_id_type": receive_id_type,
            "receive_target_source": receive_target_source,
            "_send": _result,
            "env": debug_env_snapshot(),
            "raw_data": data
        })
    else:
        output({
            "ok": True,
            "answer": "图片已发送。"
        })


if __name__ == "__main__":
    main()
