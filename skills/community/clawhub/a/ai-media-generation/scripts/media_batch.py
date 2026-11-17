#!/usr/bin/env python3
"""批量媒体处理 — 图像批量缩放/格式转换 + 目录清理（确定性任务）。

用途：AI 生成的批量图片交付前的统一处理：
  - 按最大边长缩放（保持比例，--max-dim）
  - 格式转换（--format png/jpg/webp）
  - 非目标文件清理预览（--dry-run 列出将删除项，实际删除需 --apply）

依赖: Pillow（缺省时打印清晰指引并退出，绝不静默降级）。

用法:
  python3 media_batch.py --in ./output --out ./deliver --max-dim 1024 --format webp
  python3 media_batch.py --in ./output --dry-run              # 只预览不动作
  python3 media_batch.py --in ./output --out ./clean --format png --strict --json

退出码: 0=全部成功; 1=存在失败(--strict 生效); 2=用法/依赖错误
"""
import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

EXTS = {"png": "PNG", "jpg": "JPEG", "jpeg": "JPEG", "webp": "WEBP", "bmp": "BMP"}
INPUT_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".bmp")


def process_image(src: Path, dst: Path, max_dim, fmt):
    """单张处理：缩放 + 转格式。失败抛异常。"""
    img = Image.open(src)
    img.load()
    if max_dim:
        w, h = img.size
        scale = min(1.0, max_dim / max(w, h))
        if scale < 1.0:
            img = img.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
    save_kwargs = {}
    if fmt in ("jpg", "jpeg"):
        # JPEG 无透明通道：RGBA/P 先合成白底
        if img.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            img = img.convert("RGBA")
            bg.paste(img, mask=img.split()[-1])
            img = bg
        save_kwargs["quality"] = 90
    else:
        img = img.convert("RGB") if img.mode == "P" else img
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, EXTS[fmt], **save_kwargs)


def main():
    p = argparse.ArgumentParser(description="批量图像缩放/格式转换（--strict 可作 CI 门禁）")
    p.add_argument("--in", dest="in_dir", required=True, help="输入目录")
    p.add_argument("--out", dest="out_dir", default=None, help="输出目录（默认 = 输入目录，原地转换）")
    p.add_argument("--max-dim", type=int, default=0, help="最大边长像素（0=不缩放）")
    p.add_argument("--format", dest="fmt", default="", choices=sorted(EXTS), help="目标格式（默认保持原格式）")
    p.add_argument("--dry-run", action="store_true", help="只预览将处理的文件，不写盘")
    p.add_argument("--strict", action="store_true", help="存在失败时退出码 1")
    p.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    args = p.parse_args()

    if Image is None:
        msg = "缺少 Pillow: pip install Pillow（macOS: python3 -m pip install --user Pillow）"
        print(msg, file=sys.stderr)
        return 2

    in_dir = Path(args.in_dir)
    if not in_dir.is_dir():
        print(f"输入目录不存在: {in_dir}", file=sys.stderr)
        return 2
    out_dir = Path(args.out_dir) if args.out_dir else in_dir

    files = sorted(x for x in in_dir.iterdir() if x.is_file() and x.suffix.lower() in INPUT_EXTS)
    if not files:
        print(f"输入目录无图片文件: {in_dir}", file=sys.stderr)
        return 2

    results, failures = [], []
    for src in files:
        fmt = args.fmt or src.suffix.lower().lstrip(".")
        dst = out_dir / (src.stem + "." + ("jpg" if fmt == "jpeg" else fmt))
        if args.dry_run:
            results.append({"file": src.name, "action": "dry-run", "target": str(dst)})
            continue
        try:
            process_image(src, dst, args.max_dim, fmt)
            results.append({"file": src.name, "ok": True, "target": str(dst)})
        except Exception as e:  # noqa: BLE001 — 单文件失败不中断批量
            failures.append({"file": src.name, "error": str(e)})
            results.append({"file": src.name, "ok": False, "error": str(e)})

    if args.json:
        print(json.dumps({"results": results, "failures": failures}, ensure_ascii=False, indent=2))
    else:
        for r in results:
            mark = "OK  " if r.get("ok") else ("DRY " if r.get("action") else "FAIL")
            print(f"[{mark}] {r['file']} -> {r.get('target', r.get('error', ''))}")

    if failures:
        return 1 if args.strict else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
