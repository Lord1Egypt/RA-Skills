#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风格库 · 出图脚本 generate.py（cinematic-image-studio）

读 `<项目目录>/提示词.json`（每个「风格×主体」一条），走 NewAPI 图片中转逐条出图；
API 不通时写 `图片/generate_image参数.json` 并退出 6（generate_image / edit_image 兜底 + --adopt 收位），
落盘到 `<项目目录>/图片/<kind>/<id>.png`；支持并发出图、断点续跑、失败重试、可选参考图。

提示词.json 结构（`rows` 也可为裸数组）：
  {
    "style": "彩色水墨",
    "rows": [
      {"id": "彩色水墨-烟雨山水孤舟", "kind": "彩色水墨", "size": "1536x1024",
       "prompt": "【主体】…【负向】…", "refs": []}
    ]
  }

配置优先级：--base-url/--key/--model/--quality ＞ 环境变量 NEWAPI_IMAGE_* ＞ 本 skill 的 config.json
            （自带，不回退上级目录）。

出图口径：本 skill 只出 16:9 / 9:16；styles/54–57 是 MV 导入卡（默认 3:4），由 MV 侧脚本消费。

仅用 Python 标准库，零依赖。

用法：
  ★ 硬规则：**一次只出一张**。批量出图没有逃生口（要改就改本文件默认值）。
  ★ 出图必须显式加 `--yes`；不加只预览、不花钱。

  # 合并库模式（当前默认）：提示词在 assets/output/提示词.json，图片平铺到 assets/output/图片/
  python3 scripts/generate.py --project . --dry-run
  # 免费预览：看下一张要出什么（不调接口）
  python3 scripts/generate.py --project 彩色水墨-烟雨山水孤舟 --dry-run
  # 出 1 张（本次只出待出队列里的第一张；出完再跑一次出下一张）
  python3 scripts/generate.py --project 彩色水墨-烟雨山水孤舟 --yes
  # 指定只出某一张
  python3 scripts/generate.py --project <目录> --id 彩色水墨 --yes
  # 更省：降质量 / 降尺寸
  python3 scripts/generate.py --project <目录> --quality medium --size 1024x1024 --yes
"""
import argparse
import base64
import concurrent.futures
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import uuid

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_CANDIDATES = [
    os.path.join(SKILL_ROOT, "config.json"),   # 只读本 skill 自带配置
]
OUTPUT_ROOT = os.path.join(SKILL_ROOT, "assets", "output")
IMG_EXTS = (".png", ".jpg", ".jpeg", ".webp")
DEFAULT_BASE_URL = "https://api.openai.com"   # 换成你自己的 OpenAI 兼容网关（也可用 --base-url / NEWAPI_IMAGE_BASE_URL）
DEFAULT_MODEL = "gpt-image-2-c"
DEFAULT_QUALITY = "high"
RATIO_TO_SIZE = {"16:9": "1536x1024", "9:16": "1024x1536"}

# ── 出图渠道 ────────────────────────────────────────────────────────────
# newapi：OpenAI 兼容中转（/v1/images/generations，支持 quality）
# ark   ：火山方舟 Seedream（/api/v3/images/generations，无 quality，支持 1K/2K/4K 像素尺寸）
CHANNELS = {
    "newapi": {
        "base": DEFAULT_BASE_URL,
        "model": DEFAULT_MODEL,
        "key_env": ("NEWAPI_IMAGE_KEY",),
        "base_env": ("NEWAPI_IMAGE_BASE_URL",),
        "model_env": ("NEWAPI_IMAGE_MODEL",),
        "quality": True,
        "api_path": "/images/generations",
        "api_edit_path": "/images/edits",
    },
    "ark": {
        "base": "https://ark.cn-beijing.volces.com/api/v3",
        "model": "doubao-seedream-5-0-pro-260628",
        "key_env": ("ARK_API_KEY", "HUOSHAN_SEEDANCE_KEY", "NEWAPI_IMAGE_KEY"),
        "base_env": ("ARK_IMAGE_BASE_URL",),
        "model_env": ("ARK_IMAGE_MODEL",),
        "quality": False,
        "api_path": "/images/generations",
        "api_edit_path": "/images/generations",   # Seedream 走同一端点 + image 字段
    },
}
# Ark(Seedream) 像素尺寸：按取向给 2K 档
ARK_RATIO_SIZE = {"16:9": "2048x1152", "9:16": "1152x2048", "3:4": "1536x2048", "1:1": "2048x2048"}
# 常见尺寸 → Ark 尺寸（API 只认自身档位，先映射再兜底原样传）
ARK_SIZE_MAP = {
    "1536x1024": "2048x1152", "1024x1536": "1152x2048",
    "1024x1024": "2048x2048", "1280x720": "2048x1152", "720x1280": "1152x2048",
    "2048x1152": "2048x1152", "1152x2048": "1152x2048", "2048x2048": "2048x2048",
}
RC_FILES = ("~/.zshrc", "~/.zshenv", "~/.zprofile", "~/.bash_profile", "~/.bashrc")


def env_or_rc(name):
    """先读环境变量；非交互 shell（IDE / 常驻进程）读不到时，回落到 shell 配置文件的 export 行。"""
    v = os.environ.get(name)
    if v:
        return v.strip()
    pat = re.compile(r'^\s*(?:export\s+)?' + re.escape(name) + r'\s*=\s*["\']?([^"\'\s#]+)', re.M)
    for p in RC_FILES:
        path = os.path.expanduser(p)
        try:
            if not os.path.isfile(path):
                continue
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                m = pat.search(f.read())
            if m:
                return m.group(1).strip()
        except OSError:
            continue
    return ""


def ark_size(size):
    s = str(size or "").strip().lower()
    if not s:
        return ""
    if s in ARK_SIZE_MAP:
        return ARK_SIZE_MAP[s]
    for ratio, px in ARK_RATIO_SIZE.items():
        if s == ratio.replace(":", "x"):
            return px
    return s


def record_provenance(prompts_path, eid, api, model, size, ts=None):
    """出图成功后把「哪个 API 出的」写回 提示词.json 的对应行（gallery.py 据此打标签）。"""
    if not prompts_path or not os.path.isfile(prompts_path):
        return False
    try:
        with open(prompts_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        rows = data.get("rows") if isinstance(data, dict) else data
        if not isinstance(rows, list):
            return False
        hit = False
        for r in rows:
            if isinstance(r, dict) and str(r.get("id", "")) == str(eid):
                r["api"] = api
                r["model"] = model or ""
                if size:
                    r["api_size"] = size
                r["api_at"] = ts or time.strftime("%Y-%m-%d %H:%M")
                hit = True
        if not hit:
            return False
        tmp = prompts_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp, prompts_path)
        return True
    except (OSError, ValueError):
        return False



def load_config():
    for path in CONFIG_CANDIDATES:
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (OSError, ValueError):
                continue
    return {}


def normalize_base(url):
    u = (url or "").strip().rstrip("/")
    if not u:
        return ""
    return u if u.endswith("/v1") else u + "/v1"


def _parse_image_response(obj):
    if obj.get("error"):
        raise RuntimeError(f"接口报错: {str(obj['error'])[:300]}")
    data = obj.get("data") or []
    if not data:
        raise RuntimeError(f"响应无 data: {str(obj)[:300]}")
    item = data[0]
    if item.get("b64_json"):
        return base64.b64decode(item["b64_json"])
    if item.get("url"):
        with urllib.request.urlopen(item["url"], timeout=180) as r:
            return r.read()
    raise RuntimeError(f"响应字段无法识别: {list(item.keys())}")


def _post_json(url, key, payload, timeout):
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), method="POST")
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")
    except Exception as e:
        raise RuntimeError(f"网络错误: {e}")


def _post_multipart(url, key, fields, files, timeout):
    boundary = "----cinema" + uuid.uuid4().hex
    buf = []
    for name, value in fields:
        if value is None or value == "":
            continue
        buf.append(f"--{boundary}\r\n".encode("utf-8"))
        buf.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        buf.append(str(value).encode("utf-8"))
        buf.append(b"\r\n")
    for field, filename, blob in files:
        lower = filename.lower()
        ctype = ("image/png" if lower.endswith(".png")
                 else "image/jpeg" if lower.endswith((".jpg", ".jpeg")) else "image/webp")
        buf.append(f"--{boundary}\r\n".encode("utf-8"))
        buf.append((f'Content-Disposition: form-data; name="{field}"; filename="{filename}"\r\n'
                    f"Content-Type: {ctype}\r\n\r\n").encode("utf-8"))
        buf.append(blob)
        buf.append(b"\r\n")
    buf.append(f"--{boundary}--\r\n".encode("utf-8"))
    req = urllib.request.Request(url, data=b"".join(buf), method="POST")
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")
    except Exception as e:
        raise RuntimeError(f"网络错误: {e}")


def api_generate(base, key, model, prompt, size, quality, timeout, channel="newapi"):
    ch = CHANNELS.get(channel, CHANNELS["newapi"])
    if channel == "ark":
        payload = {"model": model, "prompt": prompt, "response_format": "url", "watermark": False}
        px = ark_size(size)
        if px:
            payload["size"] = px
    else:
        payload = {"model": model, "prompt": prompt}
        if size:
            payload["size"] = size
        if quality:
            payload["quality"] = quality
    return _parse_image_response(_post_json(f"{base}{ch['api_path']}", key, payload, timeout))


def api_edit(base, key, model, prompt, size, quality, ref_files, timeout, field="image[]", channel="newapi"):
    if channel == "ark":
        # Seedream 多图/图生图：JSON 里传 data URL 数组
        imgs = []
        for name, blob in ref_files:
            lower = name.lower()
            mime = ("image/png" if lower.endswith(".png")
                    else "image/jpeg" if lower.endswith((".jpg", ".jpeg")) else "image/webp")
            imgs.append(f"data:{mime};base64," + base64.b64encode(blob).decode("utf-8"))
        payload = {"model": model, "prompt": prompt, "response_format": "url", "watermark": False}
        if imgs:
            payload["image"] = imgs if len(imgs) > 1 else imgs[0]
        px = ark_size(size)
        if px:
            payload["size"] = px
        return _parse_image_response(
            _post_json(f"{base}{CHANNELS['ark']['api_path']}", key, payload, timeout))
    fields = [("model", model), ("prompt", prompt), ("size", size), ("quality", quality)]
    files = [(field, name, blob) for name, blob in ref_files]
    return _parse_image_response(
        _post_multipart(f"{base}{CHANNELS['newapi']['api_edit_path']}", key, fields, files, timeout))



def detect_ext(raw):
    if raw[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if raw[:2] == b"\xff\xd8":
        return ".jpg"
    if raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        return ".webp"
    return ".png"


def png_dimensions(b):
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", b[16:24])
        return f"{w}x{h}"
    return "?"


# ==================== 出图通道：API 优先 · 工具兜底 ====================
# 规则：本地 API 优先；没 key / 连不通 / 出图失败时不再硬失败，而是写出
#   <出图目录>/generate_image参数.json 并返回退出码 6：
#     · 无参考图的条目 → generate_image(image_configs=[...])，每批 ≤10 张
#     · 有参考图的条目 → edit_image(image_path=<主参考>, prompt=..., size=...)，一次一张
#   工具出图后：python3 scripts/generate.py --project <项目> --adopt <图片…>
EXIT_NEED_TOOL = 6
MANIFEST_NAME = "generate_image参数.json"
TOOL_SIZES = ("1024x1024", "1536x1024", "1024x1536", "2048x2048",
              "2048x1152", "3840x2130", "2130x3840")
TOOL_BATCH = 10
IMG_EXTS_ALL = (".png", ".jpg", ".jpeg", ".webp")


def tool_size(size, default="1024x1536"):
    """把任意尺寸映射到 generate_image 的 7 档标准尺寸。"""
    s = str(size or "").strip().lower()
    if s in TOOL_SIZES:
        return s
    try:
        w, h = (int(x) for x in s.split("x"))
    except (ValueError, TypeError):
        return default
    if not w or not h:
        return default
    r = w / h
    big = max(w, h) >= 2000
    if 0.95 <= r <= 1.05:
        return "2048x2048" if big else "1024x1024"
    if r > 1.05:
        if r > 1.9:
            return "3840x2130" if big else "2048x1152"
        return "1536x1024"
    return "1024x1536"


def probe_image_api(base, key, timeout=20):
    """只读探测本地出图 API（免费），返回 (可用?, 说明)。"""
    if not key:
        return False, "没读到 API key（--key / NEWAPI_IMAGE_KEY / config.json newapi_image_key）"
    if not base:
        return False, "没有 base_url"
    url = base + "/models"
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("Authorization", "Bearer " + key)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp.read(2048)
        return True, f"HTTP 200（{url}）"
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return False, f"HTTP {e.code}：key 被拒（{url}）"
        if e.code in (404, 405):
            return True, f"HTTP {e.code}：/models 未实现，但网关可达，按可用处理"
        return False, f"HTTP {e.code}（{url}）"
    except Exception as e:  # noqa: BLE001
        return False, f"连不通：{e}"


def build_tool_manifest(items, target_rel, reason, adopt_hint):
    """items: [{id,file,size,tool,prompt,refs,call?}]；generate_image 按 ≤10 张分批。"""
    gen = [it for it in items if it.get("tool") == "generate_image"]
    batches = [[{"prompt": it["prompt"], "size": it["size"], "output_format": "png"}
                for it in gen[i:i + TOOL_BATCH]]
               for i in range(0, len(gen), TOOL_BATCH)]
    return {
        "note": ("本地出图 API 不可用时的兜底清单：无参考图用 generate_image（每批 ≤10 张），"
                 "有参考图用 edit_image（一次一张）。出图后按 items 顺序 --adopt 收位。"),
        "channel": "tool",
        "reason": reason,
        "target_dir": target_rel,
        "generate_count": len(gen),
        "edit_count": len(items) - len(gen),
        "items": items,
        "batches": batches,
        "after": adopt_hint + " <图片…>",
    }


def print_tool_handoff(manifest_path, manifest):
    print("")
    print(f"[降级] 本地出图 API 不可用（{manifest['reason']}）→ 改走宿主工具 generate_image / edit_image")
    print(f"[清单] {manifest_path}")
    print(f"[任务] generate_image {manifest['generate_count']} 张"
          f"（{len(manifest['batches'])} 批）· edit_image {manifest['edit_count']} 张")
    for i, batch in enumerate(manifest["batches"], 1):
        print("-" * 60)
        print(f"[generate_image 第 {i}/{len(manifest['batches'])} 批 · {len(batch)} 张]")
        for j, cfg in enumerate(batch, 1):
            print(f"  {j}) size={cfg['size']}")
            print(f"     {cfg['prompt']}")
    edits = [it for it in manifest["items"] if it.get("tool") == "edit_image"]
    if edits:
        print("-" * 60)
        print(f"[edit_image · {len(edits)} 张，一次一张]")
        for it in edits:
            call = it.get("call") or {}
            print(f"  - {it['id']} → {it['file']}")
            print(f"    edit_image(image_path=\"{call.get('image_path', '')}\", "
                  f"prompt=<见清单>, size=\"{it['size']}\")")
            if call.get("ref_paths"):
                print(f"    （多参考图可选：再加 ref_paths={call['ref_paths']}）")
    print("-" * 60)
    print(f"[收位] {manifest['after']}")


def image_size_bytes(raw):
    """从 PNG / JPEG 头里读宽高（读不出返回 0,0）。"""
    if raw[:8] == b"\x89PNG\r\n\x1a\n" and len(raw) >= 24:
        w, h = struct.unpack(">II", raw[16:24])
        return int(w), int(h)
    if raw[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(raw):
            if raw[i] != 0xFF:
                i += 1
                continue
            marker = raw[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                          0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", raw[i + 5:i + 9])
                return int(w), int(h)
            if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            i += 2 + struct.unpack(">H", raw[i + 2:i + 4])[0]
    return 0, 0


def _write_png(src, dst):
    raw = open(src, "rb").read()
    if not raw:
        raise RuntimeError("空文件")
    if raw[:8] == b"\x89PNG\r\n\x1a\n":
        with open(dst, "wb") as f:
            f.write(raw)
        return image_size_bytes(raw)
    ff = shutil.which("ffmpeg")
    if not ff:
        raise RuntimeError("非 PNG 且本机没有 ffmpeg（brew install ffmpeg）")
    subprocess.run([ff, "-y", "-v", "error", "-i", src, "-frames:v", "1", dst], check=True)
    with open(dst, "rb") as f:
        return image_size_bytes(f.read())


def _natural_key(name):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def adopt_tool_images(paths, manifest_path, proj_dir, force=False):
    """按清单顺序收位工具出好的图；支持目录、按序文件、id=路径。"""
    if not os.path.isfile(manifest_path):
        print(f"[FAIL] 找不到出图清单：{manifest_path}\n"
              f"       先跑一次本脚本（API 不通会自动写出），或加 --tool-json 生成")
        return 1
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    items = [it for it in (manifest.get("items") or []) if it.get("id")]
    if not items:
        print("[FAIL] 清单里没有 items")
        return 1
    by_id = {str(it["id"]): it for it in items}
    mapping, plain = {}, []
    for p in paths:
        key = p.split("=", 1)[0] if "=" in p else ""
        if key in by_id:
            mapping[key] = p.split("=", 1)[1]
        else:
            plain.append(p)

    expanded = []
    for p in plain:
        full = p if os.path.isabs(p) else os.path.join(proj_dir, p)
        if os.path.isdir(full):
            expanded.extend(sorted(
                (os.path.join(full, f) for f in os.listdir(full)
                 if f.lower().endswith(IMG_EXTS_ALL)),
                key=lambda x: _natural_key(os.path.basename(x))))
        else:
            expanded.append(full)
    pending = [it for it in items if str(it["id"]) not in mapping]
    if len(expanded) != len(pending):
        print(f"[FAIL] 图片数与清单不符：给了 {len(expanded)} 张，清单待收位 {len(pending)} 张")
        print("       待收位：" + "、".join(str(it["id"]) for it in pending[:20])
              + ("…" if len(pending) > 20 else ""))
        print("       可改用 id=路径 精确对应，或 --adopt <目录>（按文件名自然排序）")
        return 1
    for it, path in zip(pending, expanded):
        mapping[str(it["id"])] = path

    done = 0
    skipped = 0
    for it in items:
        eid = str(it["id"])
        src = mapping.get(eid)
        if not src:
            continue
        if not os.path.isfile(src):
            print(f"[FAIL] {eid} 图片不存在：{src}")
            continue
        target = it["file"] if os.path.isabs(it["file"]) else os.path.join(proj_dir, it["file"])
        os.makedirs(os.path.dirname(target) or proj_dir, exist_ok=True)
        if os.path.isfile(target) and not force:
            print(f"[skip] {eid}（已存在；覆盖加 --force）")
            skipped += 1
            continue
        try:
            w, h = _write_png(src, target)
        except Exception as e:  # noqa: BLE001
            print(f"[FAIL] {eid} 收位失败：{e}")
            continue
        done += 1
        record_provenance(os.path.join(proj_dir, "提示词.json"), eid, "tool", "", "")
        print(f"[完成] {eid} → {it['file']}（{w}x{h}，{os.path.getsize(target) // 1024} KB）")
    tail = f"（另有 {skipped} 张已存在跳过）" if skipped else ""
    print(f"\n[收位] {done}/{len(mapping)} 张已就位{tail}")
    print("[下一步] 先看这些图：主体对不对、风格对不对、有没有文字。不对就改提示词重出。")
    return 0 if done + skipped == len(mapping) else 1


def main():
    # 行缓冲：否则输出被管道整块缓冲，运行中看不到任何进度（本项目踩过：干等 10 分钟无输出）
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description="风格库 · 读 提示词.json 出图（cinematic-image-studio）")
    ap.add_argument("--project", required=True,
                    help="项目目录名（在 assets/output/ 下）或目录路径")
    ap.add_argument("--prompts", default="提示词.json", help="提示词文件（默认 提示词.json）")
    ap.add_argument("--img-dir", default="图片", help="图片根目录名（默认 图片）")
    ap.add_argument("--kind", default="", help="只出某风格（按 kind 字段）")
    ap.add_argument("--id", default="", help="只出指定 id（前缀匹配，逗号分隔）")
    ap.add_argument("--size", default="", help="统一覆盖尺寸（如 1536x1024）")
    ap.add_argument("--ratio", default="", choices=["", "16:9", "9:16"],
                    help="按取向统一覆盖尺寸：16:9→1536x1024，9:16→1024x1536")
    ap.add_argument("--base-url", default="")
    ap.add_argument("--key", default="")
    ap.add_argument("--model", default="")
    ap.add_argument("--quality", default="")
    ap.add_argument("--channel", default="newapi", choices=["newapi", "ark", "auto"],
                    help="出图渠道：newapi=OpenAI兼容中转 gpt-image-2-c（默认）/ "
                         "ark=火山方舟 seedream-5-0-pro / auto=有 NewAPI key 用 newapi，否则用 ark")
    ap.add_argument("--ref-field", default="image[]", help="多图 multipart 字段名（默认 image[]）")
    ap.add_argument("--limit", type=int, default=0, help="最多出几张（0=不限）")
    ap.add_argument("--force", action="store_true", help="已存在的图也重新生成")
    ap.add_argument("--dry-run", action="store_true", help="只预览，不调接口")
    ap.add_argument("--yes", action="store_true",
                    help="★确认真的调用付费接口出图。不加此参数则只预览、不出图（防误花钱）")
    ap.add_argument("--max-images", type=int, default=1,
                    help="★单次出图张数上限，硬规则=1（一次只出一张）。调大于 1 会被拒绝，"
                         "确实要改请改本文件的默认值，不要用命令行绕过")
    ap.add_argument("--concurrency", type=int, default=1,
                    help="并发数（固定 1：一次只出一张，并发无意义）")
    ap.add_argument("--timeout", type=int, default=180,
                    help="单张超时秒数（默认 180）。★别调太大：超时 × (重试+1) = 最坏干等时长，"
                         "600×3 就是 30 分钟")
    ap.add_argument("--retries", type=int, default=1,
                    help="失败重试次数（默认 1）。★每多一次，最坏时长翻倍")
    ap.add_argument("--probe", action="store_true",
                    help="只探测本地出图 API（免费）：0=可用 / 6=需走 generate_image")
    ap.add_argument("--tool-json", action="store_true",
                    help=f"不出图，只写 {MANIFEST_NAME}（generate_image / edit_image 参数）")
    ap.add_argument("--adopt", nargs="*", default=[],
                    help="工具出图后收位：按清单顺序给图片/目录，或 id=路径")
    ap.add_argument("--no-fallback", "--api-only", dest="no_fallback", action="store_true",
                    help="强制走通道 A：API 失败不降级到工具，直接退出 1（默认降级并退出 6）")
    args = ap.parse_args()

    # 定位项目目录
    if os.path.isabs(args.project) or os.sep in args.project:
        proj_dir = os.path.abspath(args.project)
    else:
        proj_dir = os.path.join(OUTPUT_ROOT, args.project)
        if not os.path.isdir(proj_dir):
            sys.exit(f"[FAIL] 找不到项目目录：{proj_dir}")
    base_img = os.path.join(proj_dir, args.img_dir)
    manifest_path = os.path.join(base_img, MANIFEST_NAME)
    adopt_hint = f"python3 scripts/generate.py --project {args.project} --adopt"

    cfg = load_config()

    def first_env(names):
        for n in names:
            v = env_or_rc(n)
            if v:
                return v
        return ""

    channel = args.channel
    if channel == "auto":
        channel = "newapi" if (args.key or first_env(CHANNELS["newapi"]["key_env"])) else "ark"
    ch = CHANNELS[channel]
    cfg_base_key = "ark_image_base_url" if channel == "ark" else "newapi_image_base_url"
    cfg_model_key = "ark_image_model" if channel == "ark" else "newapi_image_model"
    cfg_key_key = "ark_image_key" if channel == "ark" else "newapi_image_key"
    cfg_quality_key = "newapi_image_quality"

    base_raw = (args.base_url or first_env(ch["base_env"]) or cfg.get(cfg_base_key) or ch["base"])
    base = base_raw.rstrip("/") if channel == "ark" else normalize_base(base_raw)
    key = args.key or first_env(ch["key_env"]) or cfg.get(cfg_key_key) or ""
    model = args.model or first_env(ch["model_env"]) or cfg.get(cfg_model_key) or ch["model"]
    quality = ""
    if ch["quality"]:
        quality = (args.quality or first_env(("NEWAPI_IMAGE_QUALITY",))
                   or cfg.get(cfg_quality_key) or DEFAULT_QUALITY)
    size_override = args.size or RATIO_TO_SIZE.get(args.ratio, "")

    # ① 只探通道：不调接口、不花钱，也不需要提示词文件
    if args.probe:
        ok, detail = probe_image_api(base, key, min(args.timeout, 30))
        print(f"[渠道] {channel} · {base} · {model}")
        print(f"[通道] {'A 本地 API 可用' if ok else 'B 走 generate_image / edit_image（API 不可用）'}：{detail}")
        return 0 if ok else EXIT_NEED_TOOL

    # ② 收位工具出好的图：只读 图片/generate_image参数.json，也不需要提示词文件
    if args.adopt or "--adopt" in sys.argv[1:]:
        if not args.adopt:
            print("[FAIL] --adopt 后面要跟图片/目录，或 id=路径")
            print(f"       例：python3 scripts/generate.py --project {args.project} "
                  f"--img-dir {args.img_dir} --adopt {args.img_dir}/")
            return 2
        return adopt_tool_images(args.adopt, manifest_path, proj_dir, force=args.force)

    # ③ 以下（预览 / 出图）才需要提示词文件
    prompts_path = (args.prompts if os.path.isabs(args.prompts)
                    else os.path.join(proj_dir, args.prompts))
    if not os.path.isfile(prompts_path):
        sys.exit(f"[FAIL] 找不到提示词文件：{prompts_path}")

    with open(prompts_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    entries = data["rows"] if isinstance(data, dict) and isinstance(data.get("rows"), list) else data
    if isinstance(data, dict) and data.get("negative"):
        for e in entries:
            e.setdefault("negative", data["negative"])

    if args.kind:
        entries = [e for e in entries if (e.get("kind") or "") == args.kind]
    if args.id:
        pats = [p.strip() for p in args.id.split(",") if p.strip()]
        entries = [e for e in entries if any(str(e.get("id", "")).startswith(p) for p in pats)]

    def is_flat_lib():
        # 合并库：assets/output/提示词.json + 图片/<id>.png（不再按风格分子目录）
        return os.path.abspath(proj_dir) == os.path.abspath(OUTPUT_ROOT)

    def kind_dir(kind):
        if is_flat_lib():
            return base_img
        return os.path.join(base_img, (kind or "").strip() or "默认")

    def existing(eid, kind):
        for d in (kind_dir(kind), base_img):
            for ext in IMG_EXTS:
                p = os.path.join(d, eid + ext)
                if os.path.isfile(p):
                    return p
        return None

    def find_ref(ref_id):
        for sub in ("", "彩色水墨", "山海经神兽"):
            d = os.path.join(base_img, sub) if sub else base_img
            for ext in IMG_EXTS:
                p = os.path.join(d, ref_id + ext)
                if os.path.isfile(p):
                    return p
        return None

    def make_items(rows_):
        items = []
        for e in rows_:
            eid = str(e["id"])
            size = tool_size(size_override or e.get("size") or "")
            refs = e.get("refs") or []
            if isinstance(refs, str):
                refs = [refs]
            ref_paths = []
            for r in refs:
                hit = find_ref(str(r))
                if hit:
                    ref_paths.append(os.path.relpath(hit, proj_dir))
            prompt = str(e["prompt"])
            neg = str(e.get("negative") or "").strip()
            if neg:
                prompt = prompt.rstrip("。") + "。\n【负向】" + neg
            target = os.path.join(kind_dir(e.get("kind")), eid + ".png")
            item = {
                "id": eid,
                "file": os.path.relpath(target, proj_dir),
                "size": size,
                "tool": "edit_image" if ref_paths else "generate_image",
                "prompt": prompt,
            }
            if ref_paths:
                item["refs"] = ref_paths
                item["call"] = {"tool": "edit_image", "image_path": ref_paths[0],
                                "ref_paths": ref_paths[1:], "prompt": prompt, "size": size}
            items.append(item)
        return items

    def handoff(reason, rows_):
        """API 走不通：写出工具清单并交棒（退出码 6）。"""
        if args.no_fallback:
            print(f"[FAIL] 出图 API 不可用（{reason}）；--no-fallback 已关闭降级")
            return 1
        items = make_items(rows_)
        if not items:
            print("[完成] 没有需要出的图。")
            return 0
        manifest = build_tool_manifest(items, args.img_dir, reason, adopt_hint)
        os.makedirs(base_img, exist_ok=True)
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print_tool_handoff(manifest_path, manifest)
        return EXIT_NEED_TOOL

    todo = [e for e in entries
            if e.get("id") and e.get("prompt") and (args.force or not existing(e["id"], e.get("kind")))]
    for e in entries:
        if e.get("id") and e.get("prompt") and not args.force and existing(e["id"], e.get("kind")):
            print(f"[skip] {e['id']}（已存在）")
    if args.limit:
        todo = todo[:args.limit]

    key_desc = f"{key[:8]}…{key[-4:]}" if key else "(未提供)"
    print(f"[配置] channel={channel}  base={base}  model={model}  "
          f"{'quality=' + quality + '  ' if quality else ''}key={key_desc}")
    suffix = "" if is_flat_lib() else "<风格>/"
    print(f"[计划] 共 {len(todo)} 张 → {base_img}/{suffix}")

    if args.dry_run:
        for e in todo:
            print(f"  - [{e.get('kind')}] {e['id']}  size={size_override or e.get('size') or '(默认)'}"
                  f"  refs={e.get('refs') or '无'}")
        print("[dry-run] 未调接口。")
        return 0
    if args.tool_json:
        print("[通道] B 指定：只写 generate_image / edit_image 参数，不调本地 API")
        return handoff("--tool-json 指定走工具通道", todo)
    if not key:
        return handoff("没读到 API key", todo)
    if not todo:
        print("[完成] 无待出图。")
        return 0

    # ── 硬规则：一次只出一张（没有批量逃生口） ────────────────────────
    if args.max_images != 1:
        sys.exit("[STOP] 本 skill 的硬规则是**一次只出一张**（--max-images 固定为 1）。\n"
                 "       如确需改，请直接改本文件的默认值并说明理由，不要用命令行绕过。")
    if len(todo) > 1:
        nxt = todo[0]["id"]
        print(f"[一张一张出] 本次只出 1 张，还有 {len(todo)} 张待出。")
        print(f"             本次出：{nxt}")
        print(f"             出完再跑一次即出下一张（已存在的会自动跳过）。")
        todo = todo[:1]

    # ── 成本闸门 ②：必须显式 --yes 才真的调付费接口 ──────────────────
    if not args.yes:
        print(f"\n[STOP] 未加 --yes，已中止：本次将调用**付费接口**出 {len(todo)} 张图。")
        print(f"       确认要出图：加 --yes")
        print(f"       只想看要出哪些：加 --dry-run（不出图、不花钱）")
        print(f"       想更省：--quality medium 或 --size 1024x1024")
        return 0

    lock = threading.Lock()

    def gen_one(idx, e):
        eid = e["id"]
        size = size_override or e.get("size") or ""
        refs = e.get("refs") or []
        if isinstance(refs, str):
            refs = [refs]
        ref_files = []
        for r in refs:
            p = find_ref(r)
            if p:
                with open(p, "rb") as fh:
                    ref_files.append((os.path.basename(p), fh.read()))
            else:
                with lock:
                    print(f"[{idx}/{len(todo)}] ⚠ {eid} 参考图缺失({r})，忽略", flush=True)
        t0, raw, err = time.time(), None, None
        for attempt in range(args.retries + 1):
            with lock:
                tag = f"（第 {attempt + 1}/{args.retries + 1} 次尝试）" if args.retries else ""
                print(f"[{idx}/{len(todo)}] → 请求已发出{tag}，等待中"
                      f"（单张超时 {args.timeout}s，最坏 {args.timeout * (args.retries + 1)}s）…",
                      flush=True)
            try:
                if ref_files:
                    raw = api_edit(base, key, model, e["prompt"], size, quality,
                                   ref_files, args.timeout, field=args.ref_field, channel=channel)
                else:
                    raw = api_generate(base, key, model, e["prompt"], size, quality,
                                       args.timeout, channel=channel)
                break
            except RuntimeError as ex:
                err = str(ex)
                if attempt < args.retries:
                    with lock:
                        print(f"[{idx}/{len(todo)}] {eid} 重试({attempt + 1}/{args.retries})…", flush=True)
                    time.sleep(5 * (attempt + 1))
        if raw is None:
            with lock:
                print(f"[{idx}/{len(todo)}] ✗ {eid} · {err}", flush=True)
            return eid, None, err
        d = kind_dir(e.get("kind"))
        os.makedirs(d, exist_ok=True)
        out = os.path.join(d, eid + detect_ext(raw))
        with open(out, "wb") as f:
            f.write(raw)
        used_size = ark_size(size) if channel == "ark" else size
        with lock:
            record_provenance(prompts_path, eid, channel, model, used_size)
            print(f"[{idx}/{len(todo)}] ✓ {eid} · {time.time() - t0:.0f}s · {len(raw) // 1024}KB · "
                  f"{png_dimensions(raw)} · 出图API={channel}:{model} → {out}", flush=True)
        return eid, out, None

    ok, fail = 0, []
    t_all = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as pool:
        futs = [pool.submit(gen_one, i, e) for i, e in enumerate(todo, 1)]
        for fut in concurrent.futures.as_completed(futs):
            eid, _p, err = fut.result()
            if err is None:
                ok += 1
            else:
                fail.append((eid, err))

    print(f"\n[完成] 成功 {ok} / {len(todo)}，总耗时 {(time.time() - t_all) / 60:.1f} 分钟")
    if fail:
        print("[失败清单]")
        for eid, err in fail:
            print(f"  - {eid}: {err[:160]}")
        fail_ids = {eid for eid, _err in fail}
        rows_bad = [e for e in todo if str(e["id"]) in fail_ids]
        print("[说明] 失败的那几张已写进工具清单：可以修 API 后 --force 重出，也可以走 generate_image")
        return handoff("API 出图失败：" + str(fail[0][1]).splitlines()[0][:80], rows_bad)
    print(f"[完成] 图片已落盘：{base_img}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
