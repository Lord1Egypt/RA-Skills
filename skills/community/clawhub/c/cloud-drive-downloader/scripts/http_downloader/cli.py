#!/usr/bin/env python3
"""http_downloader CLI.

仅用于下载用户已获授权或公开许可的 HTTP/HTTPS 直链文件。
下载前必须用 --confirm-own-use 明确确认授权，或交互式输入 yes。

用法示例：
  python3 -m http_downloader "https://example.com/file.mp4" -o ~/Downloads -v --confirm-own-use
  python3 -m http_downloader "https://example.com/file.zip" --split 8 --sha256 <hex> --json
  python3 -m http_downloader "ftp://..."   # 会被拒绝：模块只支持 http/https
"""

from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_here = _boot_os.path.dirname(_boot_os.path.abspath(__file__))
    _boot_parent = _boot_os.path.dirname(_boot_here)
    for _boot_dir in (_boot_here, _boot_parent):
        if _boot_dir not in _boot_sys.path:
            _boot_sys.path.insert(0, _boot_dir)
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import argparse
import json
import sys

from .compliance import COMPLIANCE_NOTICE, confirm
from .downloader import HTTPDownloader, DownloadError


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="http_downloader",
        description="通用 HTTP/HTTPS 直链下载模块（仅限已获授权/公开许可内容）",
    )
    p.add_argument("urls", nargs="+", help="要下载的 http/https 直链")
    p.add_argument("-o", "--output-dir", default=".", help="保存目录（默认当前目录）")
    p.add_argument("-f", "--filename", help="覆盖输出文件名")
    p.add_argument("--split", type=int, default=4, help="Range 并发分片数，默认 4")
    p.add_argument("--retries", type=int, default=3, help="每个请求重试次数，默认 3")
    p.add_argument("--timeout", type=float, default=30, help="读取超时秒数，默认 30")
    p.add_argument("--connect-timeout", type=float, help="连接超时秒数（默认同 --timeout）")
    p.add_argument("--no-resume", action="store_true", help="禁用断点续传")
    p.add_argument("--sha256", help="下载后校验 SHA-256（hex）")
    p.add_argument("--md5", help="下载后校验 MD5（hex）")
    p.add_argument("--json", action="store_true", help="以 JSON 输出报告")
    p.add_argument("--confirm-own-use", action="store_true",
                   help="明确确认你已获授权/该内容为公开许可，可免交互继续")
    p.add_argument("-y", "--yes", dest="confirm_own_use", action="store_true",
                   help="同 --confirm-own-use")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    interactive = sys.stdin.isatty()

    if not args.confirm_own_use:
        if not interactive:
            print(COMPLIANCE_NOTICE, file=sys.stderr)
            print("[错误] 非交互模式下必须显式添加 --confirm-own-use，表示你了解并接受责任。下载已取消。",
                  file=sys.stderr)
            return 2
        try:
            confirm(interactive=True)
        except KeyboardInterrupt:
            print("\n下载已取消。", file=sys.stderr)
            return 130
        except DownloadError as e:
            print(f"[取消] {e}", file=sys.stderr)
            return 2

    # 不提供自定义请求头/关闭证书校验，避免伪装与降低 TLS 安全。
    reports, errors = [], []
    fmt_size = lambda n: f"{n/1024/1024:.1f} MiB"

    for url in args.urls:
        try:
            dl = HTTPDownloader(
                url,
                args.output_dir,
                args.filename,
                split=args.split,
                retries=args.retries,
                timeout=args.timeout,
                connect_timeout=args.connect_timeout,
                resume=not args.no_resume,
                sha256=args.sha256,
                md5=args.md5,
            )
            rep = dl.download(confirmed=True)
            reports.append(rep)
            if not args.json:
                speed = rep.bytes_downloaded / max(rep.elapsed_sec, 0.01)
                print(f"✅ {rep.filename}: {fmt_size(rep.bytes_downloaded)}, "
                      f"{rep.elapsed_sec}s, ~{fmt_size(speed)}/s, 分片={rep.chunks}")
                print(f"   位置: {rep.dest}")
                if rep.sha256:
                    print(f"   sha256: {rep.sha256}")
        except Exception as e:  # noqa: BLE001
            errors.append({"url": url, "error": str(e)})
            if not args.json:
                print(f"❌ {url}: {e}", file=sys.stderr)

    if args.json:
        out = {
            "success": [{
                "url": r.url,
                "dest": str(r.dest),
                "bytes": r.bytes_downloaded,
                "elapsed_sec": r.elapsed_sec,
                "chunks": r.chunks,
                "verified": r.verified,
                "sha256": r.sha256,
            } for r in reports],
            "errors": errors,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0 if reports and not errors else 1

    return 0 if reports and not errors else 1


if __name__ == "__main__":
    sys.exit(main())
