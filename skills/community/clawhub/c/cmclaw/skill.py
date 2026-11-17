"""
cmclaw — 创意管家 AI 策略分析 Skill 示例实现（流式 NDJSON 消费）

调用 dam.ai.claw.v1.DamClaw/Chat（HTTP chunked NDJSON 流）。
部署/联调时：设置环境变量 YOUCLOUD_API_KEY + DAM_API_BASE，import 后调用 cmclaw_chat。

仅使用 Python 内置标准库，无需安装第三方依赖。
接口文档：见 references/cm-claw-api.md
"""

import json
import os
import ssl
import urllib.request
import urllib.error
from typing import Optional, Tuple

DEFAULT_BASE = "https://console.dam.youcloud.com"
TIMEOUT = 650  # 客户端超时 650s，服务端最长约 600s，留安全边界

# SSL 上下文：优先加载 certifi 证书包（macOS python.org Python 兼容），
# 若 certifi 未安装则回退到系统默认证书。
_SSL_CONTEXT = ssl.create_default_context()
try:
    import certifi
    _SSL_CONTEXT.load_verify_locations(certifi.where())
except (ImportError, FileNotFoundError):
    pass  # 回退到系统默认证书


class DamClawError(Exception):
    """DamClaw 调用异常（含 HTTP 非 2xx / 网络错误 / 解析错误）。"""


def _get_identity(base: str, api_key: str) -> Tuple[int, str]:
    """调 userInfo:get 拿 user_id / team_id。

    每次发起对话前若没有身份都必须先调；后端校验其与 yc_key 鉴权身份一致。
    """
    url = f"{base}/api/rpc/user/v1/user/userInfo:get"
    req = urllib.request.Request(url, headers={"Authorization": f"YC_API_KEY {api_key}"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=_SSL_CONTEXT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise DamClawError(f"userInfo:get 失败 status={e.code} body={e.read().decode('utf-8', errors='replace')}")
    except urllib.error.URLError as e:
        raise DamClawError(f"userInfo:get 网络错误: {e.reason}")

    return int(data["user_id"]), str(data["team_id"])


def cmclaw_chat(
    question: str,
    user_id: int,
    team_id: str,
    api_key: str,
    base: str = DEFAULT_BASE,
    session_id: Optional[str] = None,
    chat_mode: Optional[int] = None,
) -> Tuple[str, str]:
    """发起一次对话，流式消费 NDJSON，返回 (完整 markdown, session_id)。

    - 新对话：不传 session_id，传 chat_mode（2=策略探索/3=灵感激发，默认 2）。
    - 跟进：传 session_id，不传 chat_mode。
    - 流式协议：首包带 session_id（answer_content 空），后续包 answer_content 为增量片段，
      空行（answer_content 空）为心跳/首包跳过，连接关闭 = 流结束。
    - HTTP 非 2xx：worker 出错（done 带 error），抛 DamClawError；首包 session_id 在 error 前已发，
      可在异常对象的 .session_id 取到（若已读到）。

    返回 (output, session_id)。
    """
    body = {"input": question, "user_id": user_id, "team_id": team_id}
    if session_id:
        body["session_id"] = session_id
    if chat_mode is not None:
        body["chat_mode"] = chat_mode
    elif not session_id:
        body["chat_mode"] = 2  # 新对话默认策略探索

    url = f"{base}/api/rpc/ai/claw/v1/chat"
    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"YC_API_KEY {api_key}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )

    output_parts = []
    got_session_id = session_id or ""
    http_status = None

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=_SSL_CONTEXT) as resp:
            http_status = resp.status
            # 逐行读取流式响应（chunked transfer）
            # resp.read() 会阻塞直到流结束，我们用 read().splitlines() 处理
            raw = resp.read().decode("utf-8")
            for line in raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    envelope = json.loads(line)
                except json.JSONDecodeError:
                    continue  # 跳过无法解析的行
                # 流中段错误尾包
                if isinstance(envelope, dict) and "error" in envelope:
                    err_data = envelope["error"]
                    err = DamClawError(
                        f"DamClaw.Chat 流中段错误 code={err_data.get('code')} "
                        f"msg={err_data.get('message')} session_id={got_session_id}"
                    )
                    err.session_id = got_session_id  # type: ignore[attr-defined]
                    err.partial_output = "".join(output_parts)  # type: ignore[attr-defined]
                    raise err
                chunk = envelope.get("result") if isinstance(envelope, dict) else None
                if not isinstance(chunk, dict):
                    continue
                if chunk.get("session_id"):
                    got_session_id = chunk["session_id"]
                if not chunk.get("answer_content"):
                    continue
                output_parts.append(chunk["answer_content"])
    except urllib.error.HTTPError as e:
        # HTTP 非 2xx，尝试读取已返回的 body
        http_status = e.code
        body_text = e.read().decode("utf-8", errors="replace")
        err = DamClawError(
            f"DamClaw.Chat 请求失败 status={http_status} body={body_text}"
        )
        err.session_id = got_session_id  # type: ignore[attr-defined]
        err.partial_output = "".join(output_parts)  # type: ignore[attr-defined]
        raise err
    except urllib.error.URLError as e:
        err = DamClawError(f"DamClaw.Chat 网络错误: {e.reason}")
        err.session_id = got_session_id  # type: ignore[attr-defined]
        err.partial_output = "".join(output_parts)  # type: ignore[attr-defined]
        raise err
    except DamClawError:
        # 流中段错误已在上面构造好，直接上抛
        raise

    if http_status != 200:
        err = DamClawError(
            f"DamClaw.Chat 流中段失败 status={http_status}；"
            f"已读 session_id={got_session_id or '<未读到>'}"
        )
        err.session_id = got_session_id  # type: ignore[attr-defined]
        err.partial_output = "".join(output_parts)  # type: ignore[attr-defined]
        raise err

    return "".join(output_parts), got_session_id


def main() -> None:
    """命令行联调入口：python skill.py "分析这个美妆品牌的投放策略"。

    环境变量：YOUCLOUD_API_KEY（必填）、DAM_API_BASE（可选，默认生产域名）。
    """
    import sys

    api_key = os.environ.get("YOUCLOUD_API_KEY", "")
    base = os.environ.get("DAM_API_BASE", DEFAULT_BASE)
    if not api_key:
        print("请设置 YOUCLOUD_API_KEY 环境变量", file=sys.stderr)
        sys.exit(1)

    question = " ".join(sys.argv[1:]) or "分析这个美妆品牌的投放策略，重点 @灵感库"

    user_id, team_id = _get_identity(base, api_key)
    print(f"[identity] user_id={user_id} team_id={team_id}", flush=True)

    output, session_id = cmclaw_chat(question, user_id, team_id, api_key, base)
    print(f"[session_id] {session_id}", flush=True)
    print("---- output ----", flush=True)
    print(output)


if __name__ == "__main__":
    main()
