#!/usr/bin/env python3
"""对完整开通页 URL 生成二维码 PNG（供聊天/WebChat 使用）。

链接来源（二选一，优先 --url）：
- 命令行 --url
- 环境变量 FSOPENAPI_OPEN_URL（与 Ticket 流程写入 fosun.env 的字段一致）
"""

from __future__ import annotations

import argparse
import base64
import os
import sys
from io import BytesIO
from pathlib import Path

import qrcode

ENV_OPEN_URL = "FSOPENAPI_OPEN_URL"
DEFAULT_QR_FILENAME = "link_qr.png"
CHAT_MAX_EDGE = 320
CHAT_MIN_EDGE = 260
TERM_BORDER = 2


def make_qr(url: str) -> qrcode.QRCode:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=TERM_BORDER,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr


def _render_qr_png_image(
    qr: qrcode.QRCode,
    *,
    max_edge: int = CHAT_MAX_EDGE,
    min_edge: int = CHAT_MIN_EDGE,
):
    try:
        from PIL import Image
    except ImportError as e:
        raise ImportError(
            "生成二维码图片需要 Pillow，请执行: pip install qrcode[pil]"
        ) from e

    img = qr.make_image(fill_color="black", back_color="white")
    w, h = img.size
    long_side = max(w, h)
    if long_side <= 0:
        raise ValueError("二维码图像尺寸异常")

    if long_side > max_edge:
        scale = max_edge / long_side
    elif long_side < min_edge:
        scale = min_edge / long_side
    else:
        scale = 1.0

    nw, nh = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
    try:
        resample = Image.Resampling.NEAREST
    except AttributeError:
        resample = Image.NEAREST
    if nw != w or nh != h:
        img = img.resize((nw, nh), resample=resample)
    return img, nw, nh


def save_qr_png_for_chat(
    qr: qrcode.QRCode,
    output: str | Path | BytesIO,
    *,
    max_edge: int = CHAT_MAX_EDGE,
    min_edge: int = CHAT_MIN_EDGE,
) -> tuple[int, int]:
    """生成 PNG：最长边不超过 max_edge，若模块图过小则放大至约 min_edge。"""
    img, nw, nh = _render_qr_png_image(qr, max_edge=max_edge, min_edge=min_edge)
    if isinstance(output, BytesIO):
        img.save(output, format="PNG")
        return nw, nh

    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG")
    return nw, nh


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            f"对开通页 URL 生成二维码 PNG（需 Pillow）。"
            f"必须提供 --url 或环境变量 {ENV_OPEN_URL}。"
        )
    )
    parser.add_argument(
        "--url",
        default=None,
        metavar="链接",
        help=f"完整开通页 URL；若不传则读取环境变量 {ENV_OPEN_URL}",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_QR_FILENAME,
        metavar="PATH",
        help=f"二维码 PNG 保存路径（默认 ./{DEFAULT_QR_FILENAME}）",
    )
    parser.add_argument(
        "--max-edge",
        type=int,
        default=CHAT_MAX_EDGE,
        metavar="PX",
        help=f"图片最长边像素上限，默认 {CHAT_MAX_EDGE}",
    )
    parser.add_argument(
        "--min-edge",
        type=int,
        default=CHAT_MIN_EDGE,
        metavar="PX",
        help=f"模块过小时放大目标最短边约至此像素，默认 {CHAT_MIN_EDGE}",
    )
    parser.add_argument(
        "--markdown-data-uri",
        action="store_true",
        dest="markdown_data_uri",
        help=(
            "额外输出一行 Markdown：![](data:image/png;base64,...)。"
            "若 WebChat 允许渲染 data URI，可将该行贴进回复；多数环境会拦截，需自测。"
        ),
    )
    parser.add_argument(
        "--markdown-data-uri-max-bytes",
        type=int,
        default=48_000,
        metavar="N",
        help="PNG 超过此字节数则不输出 data URI，默认 48000",
    )
    args = parser.parse_args()

    url = (args.url or "").strip() or (os.environ.get(ENV_OPEN_URL) or "").strip()
    if not url:
        print(
            f"缺少开通页 URL：请传 --url，或设置环境变量 {ENV_OPEN_URL}。",
            file=sys.stderr,
        )
        print(
            f"示例：export {ENV_OPEN_URL}='https://…' && python3 scripts/gen_access_url.py",
            file=sys.stderr,
        )
        return 1

    qr = make_qr(url)

    try:
        out_path = Path(args.output).resolve()
        w, h = save_qr_png_for_chat(
            qr,
            out_path,
            max_edge=max(64, args.max_edge),
            min_edge=max(0, min(args.min_edge, args.max_edge)),
        )
    except ImportError as err:
        print(str(err), file=sys.stderr)
        return 1
    except OSError as e:
        print(f"无法写入二维码图片：{e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1

    print("--- 申请链接（可复制）---", file=sys.stdout)
    print(url, file=sys.stdout)
    print("--- 二维码 PNG（须在对话中以图片展示，勿仅回复路径文字）---", file=sys.stdout)
    print(f"{out_path}", file=sys.stdout)
    print(f"（图片尺寸 {w}×{h} 像素）", file=sys.stdout)
    print(f"（来源：{ENV_OPEN_URL} / --url）", file=sys.stdout)
    print("<<<FOSUN_QR_PNG_FOR_CHAT>>>", file=sys.stdout)
    print(str(out_path), file=sys.stdout)
    print("<<<END_FOSUN_QR_PNG_FOR_CHAT>>>", file=sys.stdout)

    if args.markdown_data_uri:
        raw = out_path.read_bytes()
        lim = max(4096, args.markdown_data_uri_max_bytes)
        if len(raw) > lim:
            print(
                f"提示：PNG 超过 {lim} 字节，已跳过 data URI。"
                "可缩短链接或略减小 --max-edge 后重试。",
                file=sys.stderr,
            )
        else:
            b64 = base64.standard_b64encode(raw).decode("ascii")
            try:
                decoded = base64.standard_b64decode(b64)
                if len(decoded) != len(raw):
                    raise ValueError("Base64 解码后长度不匹配")
                if decoded[:8] != raw[:8]:
                    raise ValueError("Base64 解码后内容不匹配")
            except Exception as e:
                print(
                    f"警告：Base64 编码验证失败，跳过 data URI 输出：{e}",
                    file=sys.stderr,
                )
            else:
                line = f"![OpenAPI申请二维码](data:image/png;base64,{b64})"
                print("<<<FOSUN_QR_MARKDOWN_DATA_URI>>>", file=sys.stdout)
                print(
                    "（Base64 已完整生成并验证，将下一行整行贴入助手回复可尝试在气泡中显示图）",
                    file=sys.stdout,
                )
                print(line, file=sys.stdout)
                print("<<<END_FOSUN_QR_MARKDOWN_DATA_URI>>>", file=sys.stdout)

    return 0


if __name__ == "__main__":
    sys.exit(main())
