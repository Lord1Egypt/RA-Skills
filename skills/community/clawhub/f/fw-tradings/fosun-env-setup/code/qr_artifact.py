"""Generate QR PNG and platform-agnostic media delivery hints."""

from __future__ import annotations

import base64
import importlib.util
import os
import tempfile
from pathlib import Path
from typing import Any

SETUP_ROOT = Path(__file__).resolve().parent.parent

_QR_DELIVERY_RULE = (
    "二维码发送规则：\n"
    "1. 一次多发：同一条回复里同时做：\n"
    "   - 必做：把 exact_open_url 写进回复文本（用户随时可点击）\n"
    "   - 必做：调用 deliver_attachments 发 qr_png_path（最广泛兼容）；"
    "同时在回复正文中明确提醒用户「请在附件中查看二维码」\n"
    "   - 可选：若平台支持 media，同时发 qr_media.path\n"
    "   - 可选：若平台支持 Markdown data URI，同时发 qr_image.data\n"
    "2. 发完必须问：「收到附件中的二维码了吗？如不能（只有链接/报错等），告诉我，我换方式重发」\n"
    "3. 用户说看不到 → 问「看到了什么？」→ 换一种方式重试（不要重复已失败的方式）\n"
    "禁止：只发一种方式就停手；用 Read 工具\"展示\"图片（用户看不到）；假设某平台一定支持某能力。"
)


def _load_gen_access_url_module():
    script_path = SETUP_ROOT / "scripts" / "gen_access_url.py"
    spec = importlib.util.spec_from_file_location("fosun_gen_access_url", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载 gen_access_url.py: {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generate_qr_artifact(url: str) -> dict[str, Any]:
    """在脚本执行机生成 PNG，返回 media 发图提示与元数据。"""
    gen_mod = _load_gen_access_url_module()
    output = os.path.join(tempfile.gettempdir(), f"fosun_openapi_qr_{os.getpid()}.png")
    qr = gen_mod.make_qr(url)
    width, height = gen_mod.save_qr_png_for_chat(qr, output)

    with open(output, "rb") as f:
        raw = f.read()
    content_base64 = base64.standard_b64encode(raw).decode("ascii")

    png_path = os.path.abspath(output)
    return {
        "qr_png_path": png_path,
        "qr_media": {
            "method": "media",
            "path": png_path,
            "mime_type": "image/png",
            "width": width,
            "height": height,
            "filename": "openapi_authority_qr.png",
        },
        "qr_image": {
            "type": "image",
            "mime_type": "image/png",
            "encoding": "base64",
            "data": content_base64,
            "width": width,
            "height": height,
            "alt": "OpenAPI开通二维码",
            "filename": "openapi_authority_qr.png",
        },
    }


def apply_qr_delivery(payload: dict[str, Any], open_url: str) -> dict[str, Any]:
    """把 media 发图提示写入 pending/账号动作 JSON。"""
    try:
        qr = generate_qr_artifact(open_url)
        payload["qr_png_path"] = qr["qr_png_path"]
        payload["qr_media"] = qr["qr_media"]
        payload["qr_image"] = qr["qr_image"]
        payload["show_qr_rule"] = _QR_DELIVERY_RULE
    except Exception as exc:
        payload["qr_generation_error"] = str(exc)
        payload["show_qr_rule"] = (
            "二维码生成失败，仅提供 exact_open_url；请提示用户点击链接完成开通。"
        )
    return payload
