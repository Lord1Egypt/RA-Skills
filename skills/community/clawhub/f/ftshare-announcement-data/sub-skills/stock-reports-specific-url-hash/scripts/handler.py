#!/usr/bin/env python3
"""通过 url_hash 下载 A 股研报 PDF 文件"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

BASE_URL = "https://market.ft.tech"


def _safe_output_path(path: str, base_dir: str | None = None) -> str:
    """将 output 规范为绝对路径，并限制在 base_dir 内，防止路径遍历。"""
    base_dir = (base_dir or os.getcwd()).rstrip(os.sep)
    base_abs = os.path.abspath(base_dir)
    resolved = os.path.abspath(os.path.normpath(path))
    if os.path.commonpath([base_abs, resolved]) != base_abs:
        print(
            json.dumps({"error": "output path must be under base directory", "base": base_abs},
                ensure_ascii=False),
            file=sys.stderr,
        )
        sys.exit(1)
    return resolved


def main():
    parser = argparse.ArgumentParser(description="通过 url_hash 下载 A 股研报 PDF")
    parser.add_argument("--url-hash", required=True, help="研报文件的 url_hash，从研报列表接口获取")
    parser.add_argument("--output", default=None, help="保存的文件名（默认 {url_hash}.pdf）")
    args = parser.parse_args()

    raw_output = args.output or f"{args.url_hash}.pdf"
    output = _safe_output_path(raw_output)
    url = f"{BASE_URL}/data/api/v1/market/data/report/stock-reports/{args.url_hash}"

    try:
        with urllib.request.urlopen(url) as resp:
            data = resp.read()

        if b"{" in data[:10]:
            try:
                err = json.loads(data.decode())
                print(json.dumps(err, ensure_ascii=False, indent=2), file=sys.stderr)
                sys.exit(1)
            except Exception:
                pass

        with open(output, "wb") as f:
            f.write(data)
        print(json.dumps({"saved_to": os.path.abspath(output), "size_bytes": len(data)}, ensure_ascii=False))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            err = json.loads(body)
        except Exception:
            err = {"error": body}
        print(json.dumps(err, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
