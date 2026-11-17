"""本地自测：用本机 HTTP 服务器下载一个已授权测试文件，验证直链下载模块。

用法：python3 -m http_downloader.self_test
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


import hashlib
import io
import os
import tempfile
import threading
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .downloader import DownloadError, HTTPDownloader


class RangeHandler(BaseHTTPRequestHandler):
    payload = b""

    def log_message(self, *a):  # 静默
        pass

    def _send(self, status, headers, body: bytes):
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _serve(self):
        payload = self.payload
        rng = self.headers.get("Range")
        if rng and rng.startswith("bytes="):
            spec = rng[len("bytes="):]
            start_s, _, rest = spec.partition("-")
            start = int(start_s or 0)
            end = int(rest or len(payload) - 1)
            end = min(end, len(payload) - 1)
            chunk = payload[start:end + 1]
            self._send(206, {
                "Content-Type": "application/octet-stream",
                "Accept-Ranges": "bytes",
                "Content-Disposition": 'attachment; filename="test-license.bin"',
                "Content-Range": f"bytes {start}-{end}/{len(payload)}",
            }, chunk)
        else:
            self._send(200, {
                "Content-Type": "application/octet-stream",
                "Accept-Ranges": "bytes",
                "Content-Disposition": 'attachment; filename="test-license.bin"',
            }, payload)

    do_GET = _serve
    do_HEAD = _serve


def run_self_test() -> None:
    payload = os.urandom(5 * 1024 * 1024 + 123)  # ~5MB，制造分片需要
    RangeHandler.payload = payload
    server = ThreadingHTTPServer(("127.0.0.1", 0), RangeHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}/demo.bin"
    sha = hashlib.sha256(payload).hexdigest()

    cases = [
        ("单流+断点续传路径", 1, {}),
        ("并发分片（split=4）+校验", 4, {"sha256": sha}),
    ]
    works = 0
    with tempfile.TemporaryDirectory(prefix="httpdl_test_") as td:
        for name, split, kwargs in cases:
            dest_dir = Path(td) / name
            dl = HTTPDownloader(base, dest_dir, split=split, **kwargs)
            rep = dl.download(confirmed=True)
            data = rep.dest.read_bytes()
            assert data == payload, f"{name}: 内容不一致"
            assert rep.verified, f"{name}: verified 应为 True"
            if "sha256" in kwargs:
                assert rep.sha256 == sha, f"{name}: sha256 校验失败"
            print(f"  ✔ {name}: {rep.filename}, {rep.bytes_downloaded}B, chunks={rep.chunks}, sha256={'OK' if rep.sha256 else '-'}")
            works += 1

    server.shutdown()
    taught_rej = False
    try:
        HTTPDownloader("ftp://example.com/file.bin", td).download(confirmed=True)
    except DownloadError as e:
        assert "仅支持 http/https" in str(e)
        taught_rej = True
    assert taught_rej, "应拒绝非 http/https 链接"
    print("  ✔ 拒绝非 http/https 直链: OK")
    print(f"SELF_TEST OK: {works} 个下载用例通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_self_test())
