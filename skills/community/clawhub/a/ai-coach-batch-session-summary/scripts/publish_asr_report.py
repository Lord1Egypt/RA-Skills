#!/usr/bin/env python3
"""上传 ASR 洞察 HTML，向 stdout 输出 deliverable.reportUrl（供 Agent 原样贴给用户）。"""
from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_UPLOAD_URL = "https://legion.tongfudun.com/version/upload"
DEFAULT_BUCKET = "legionclaw"
DEFAULT_DOWNLOAD_BASE = "https://chat-minio.tongfudun.com/legionclaw"
HTML_CONTENT_TYPE = "text/html; charset=utf-8"


def build_report_object_name(now: datetime | None = None) -> str:
    t = now or datetime.now()
    return f"asr_insight_{t.strftime('%Y%m%d_%H%M%S')}.html"


def _multipart_body(fields: dict[str, str], file_field: str, file_path: Path) -> tuple[bytes, str]:
    boundary = f"----FormBoundary{uuid.uuid4().hex}"
    lines: list[bytes] = []
    crlf = b"\r\n"

    for name, value in fields.items():
        lines.append(f"--{boundary}".encode())
        lines.append(f'Content-Disposition: form-data; name="{name}"'.encode())
        lines.append(b"")
        lines.append(value.encode("utf-8"))

    lines.append(f"--{boundary}".encode())
    lines.append(
        f'Content-Disposition: form-data; name="{file_field}"; filename="{file_path.name}"'.encode()
    )
    lines.append(f"Content-Type: {HTML_CONTENT_TYPE}".encode())
    lines.append(b"")
    lines.append(file_path.read_bytes())
    lines.append(f"--{boundary}--".encode())
    lines.append(b"")

    body = crlf.join(lines)
    return body, boundary


def publish_report_html(
    html_path: Path,
    *,
    object_name: str | None = None,
    upload_url: str | None = None,
    bucket: str | None = None,
    download_base: str | None = None,
) -> dict[str, Any]:
    if not html_path.is_file():
        return {"ok": False, "error": f"文件不存在: {html_path}"}

    obj = object_name or build_report_object_name()
    if not obj.endswith(".html"):
        obj = f"{obj}.html" if "." not in obj else obj

    up = (upload_url or os.environ.get("LEGION_UPLOAD_URL") or DEFAULT_UPLOAD_URL).strip()
    bkt = (bucket or os.environ.get("LEGION_UPLOAD_BUCKET") or DEFAULT_BUCKET).strip()
    base = (download_base or os.environ.get("LEGION_DOWNLOAD_BASE") or DEFAULT_DOWNLOAD_BASE).rstrip("/")

    body, boundary = _multipart_body(
        {
            "bucket": bkt,
            "objectName": obj,
            "contentType": HTML_CONTENT_TYPE,
            "contentDisposition": "inline",
        },
        "file",
        html_path,
    )
    req = Request(
        up,
        data=body,
        method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urlopen(req, timeout=120) as res:
            if res.status < 200 or res.status >= 300:
                return {
                    "ok": False,
                    "error": f"报告上传失败（HTTP {res.status}）",
                    "objectName": obj,
                }
    except HTTPError as e:
        return {
            "ok": False,
            "error": f"报告上传失败（HTTP {e.code}）",
            "objectName": obj,
        }
    except URLError:
        return {"ok": False, "error": "报告上传失败（网络异常）", "objectName": obj}

    report_url = f"{base}/{obj}"
    return {
        "ok": True,
        "reportUrl": report_url,
        "objectName": obj,
        "bucket": bkt,
    }


def load_meta(path: Path | None) -> dict[str, Any]:
    if not path or not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _configure_stdio_utf8() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass


def main() -> int:
    _configure_stdio_utf8()
    parser = argparse.ArgumentParser(description="上传 ASR 洞察 HTML 并输出 deliverable JSON")
    parser.add_argument("html", type=Path, help="待上传的 HTML 文件路径")
    parser.add_argument(
        "--object-name",
        help="上传用 objectName（默认按时间生成 asr_insight_YYYYMMDD_HHMMSS.html）",
    )
    parser.add_argument(
        "--meta",
        type=Path,
        help="可选元数据 JSON（含 title、executiveSummary、recordCount 等，由 generate 脚本写出）",
    )
    args = parser.parse_args()

    published = publish_report_html(args.html, object_name=args.object_name)
    meta = load_meta(args.meta)

    out: dict[str, Any] = {"ok": published.get("ok", False)}
    if not published.get("ok"):
        out["error"] = published.get("error", "上传失败")
        print(json.dumps(out, ensure_ascii=False))
        return 1

    deliverable: dict[str, Any] = {
        "reportUrl": published["reportUrl"],
        "objectName": published["objectName"],
    }
    for key in ("title", "executiveSummary", "recordCount", "covered_dims", "dim_count", "window_label"):
        if key in meta and meta[key] is not None:
            deliverable[key] = meta[key]

    out["report"] = {"reportUrl": published["reportUrl"], **{k: v for k, v in meta.items() if k != "reportUrl"}}
    out["deliverable"] = deliverable
    out["agentInstructions"] = (
        "向用户返回 deliverable.reportUrl（单独一行纯 https URL，前后禁止反引号）"
        "与 deliverable.executiveSummary（若有）；禁止粘贴原始转写或拉数 JSON。"
    )
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
