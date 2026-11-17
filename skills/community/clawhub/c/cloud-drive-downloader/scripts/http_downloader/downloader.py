"""HTTP/HTTPS 直链下载核心实现（仅 Python 标准库）。

特性：
- 仅 http/https 直链
- 断点续传（服务端支持 Range 时）
- 可选并发分片下载（Range 分片）
- 超时/重试/大小与哈希校验
- 无网盘解析、无鉴权绕过、无盗版搜索
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
import os
import re
import shutil
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

if sys.version_info < (3, 8):
    raise SystemExit("http_downloader 需要 Python 3.8+")

DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3
DEFAULT_SPLIT = 4


class DownloadError(RuntimeError):
    pass


@dataclass
class DownloadReport:
    url: str
    dest: Path
    filename: str
    bytes_downloaded: int
    elapsed_sec: float
    chunks: int
    resumed: bool
    verified: bool
    final_url: Optional[str] = None
    content_type: Optional[str] = None
    sha256: Optional[str] = None
    expected_size: Optional[int] = None


def _safe_name(name: str) -> str:
    name = os.path.basename(name or "").strip()
    name = re.sub(r"[/\\:\x00-\x1f]+", "_", name)
    name = name.strip(". ")
    return name or "download"


def _guess_filename(disposition: Optional[str], url: str) -> str:
    if disposition:
        m = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)"?', disposition, re.I)
        if m:
            raw = m.group(1).strip().strip("\"'")
            try:
                return _safe_name(urllib.parse.unquote(raw))
            except Exception:
                return _safe_name(raw)
        m2 = re.search(r'filename="([^"]+)"', disposition, re.I)
        if m2:
            return _safe_name(m2.group(1))
    path = urllib.parse.urlsplit(url).path
    return _safe_name(path.rsplit("/", 1)[-1])


class HTTPDownloader:
    """通用 HTTP/HTTPS 直链下载器。"""

    def __init__(
        self,
        url: str,
        output_dir: str | os.PathLike = ".",
        filename: Optional[str] = None,
        *,
        split: int = DEFAULT_SPLIT,
        retries: int = DEFAULT_RETRIES,
        timeout: float = DEFAULT_TIMEOUT,
        connect_timeout: Optional[float] = None,
        resume: bool = True,
        sha256: Optional[str] = None,
        md5: Optional[str] = None,
        tmp_dir: Optional[str | os.PathLike] = None,
        progress: Optional[Callable[[int, int], None]] = None,
    ) -> None:
        if isinstance(url, str):
            scheme = urllib.parse.urlparse(url).scheme.lower()
            if scheme not in ("http", "https"):
                raise DownloadError(f"仅支持 http/https 直链，收到: {scheme or '未知'}://")
        else:
            raise DownloadError("url 必须是字符串")

        self.url = url
        self.output_dir = Path(output_dir)
        self.filename = filename
        self.split = max(1, int(split))
        self.retries = max(1, int(retries))
        self.timeout = float(timeout)
        self.connect_timeout = float(connect_timeout) if connect_timeout else self.timeout
        # 不允许用户自定义请求头/UA，避免伪装；只使用本模块自报身份。
        self._headers = {}
        self.verify_ssl = True
        self.resume = resume
        self.sha256 = (sha256 or "").strip().lower() or None
        self.md5 = (md5 or "").strip().lower() or None
        self.tmp_dir = Path(tmp_dir) if tmp_dir else None
        self.progress = progress

        self._final_url: Optional[str] = None
        self._content_type: Optional[str] = None
        self._accept_ranges: bool = False
        self._content_length: Optional[int] = None
        self._disposition: Optional[str] = None

    # ---------- 底层请求 ----------
    def _request(self, method: str, extra_headers: Optional[dict] = None, timeout: Optional[float] = None, retries: Optional[int] = None):
        headers = dict(self._headers)
        headers["User-Agent"] = self._user_agent()
        headers.update(extra_headers or {})
        req = urllib.request.Request(self.url, method=method, headers=headers)
        ctx = self._ssl_context()
        last_err = None
        for attempt in range(1, (retries or self.retries) + 1):
            try:
                return urllib.request.urlopen(req, timeout=timeout or self.timeout, context=ctx)
            except Exception as e:  # noqa: BLE001 - 统一按重试策略处理
                last_err = e
                if attempt < (retries or self.retries):
                    time.sleep(min(2 ** attempt, 6))
        raise DownloadError(f"请求失败（重试 {self.retries} 次后）: {last_err}")

    def _user_agent(self) -> str:
        # 固定自报身份，不伪装成浏览器/客户端。
        return "http_downloader/0.1 (+authorized-public-links)"

    def _ssl_context(self):
        import ssl
        # 恒定开启证书校验，不提供关闭项。
        return ssl.create_default_context()

    # ---------- 元信息 ----------
    def probe(self) -> None:
        """通过 HEAD（失败退回 Range 探测）获取大小、文件名、是否支持 Range。"""
        headers = {}
        try:
            with self._request("HEAD", timeout=self.connect_timeout, retries=1) as r:
                self._final_url = r.geturl() or self.url
                self._content_type = r.headers.get("Content-Type")
                self._disposition = r.headers.get("Content-Disposition")
                self._content_length = self._parse_int(r.headers.get("Content-Length"))
                self._accept_ranges = self._accepts_ranges(r.headers.get("Accept-Ranges"),
                                                          r.headers.get("Content-Range"))
        except Exception:
            pass

        if self._content_length is None:
            # 用 Range bytes=0-0 测试
            try:
                with self._request("GET", {"Range": "bytes=0-0"}, timeout=self.connect_timeout, retries=1) as r:
                    if r.status in (206, 200):
                        self._final_url = self._final_url or r.geturl()
                        self._content_type = self._content_type or r.headers.get("Content-Type")
                        self._disposition = self._disposition or r.headers.get("Content-Disposition")
                        cr = r.headers.get("Content-Range")
                        if r.status == 206 and cr:
                            m = re.search(r"bytes \d+-\d+/(\d+)", cr or "")
                            if m:
                                self._content_length = int(m.group(1))
                            self._accept_ranges = True
            except Exception:
                pass

        if not self.filename:
            self.filename = _guess_filename(self._disposition, self._final_url or self.url) or "download"
        self.filename = _safe_name(self.filename)

    @staticmethod
    def _parse_int(v: Optional[str]) -> Optional[int]:
        if not v:
            return None
        try:
            return int(v.strip())
        except ValueError:
            return None

    @staticmethod
    def _accepts_ranges(*values: Optional[str]) -> bool:
        for v in values:
            if v and v.strip().lower() == "bytes":
                return True
        return False

    # ---------- 主入口 ----------
    def download(self, confirmed: bool = True) -> DownloadReport:
        if not confirmed:
            raise DownloadError("未确认授权，拒绝下载。")
        start = time.time()
        self.probe()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        dest = self.output_dir / self.filename

        final_tmp = self.output_dir / f".{self.filename}.part"
        support_range = self._accept_ranges and (self._content_length or 0) > 0 and self.split > 1

        resumed = final_tmp.exists() and self.resume
        if support_range:
            chunks = self._download_range_chunks(final_tmp)
            resume = final_tmp.exists()
        else:
            self._download_single(final_tmp)
            chunks = 1

        expected = self._content_length
        actual = final_tmp.stat().st_size if final_tmp.exists() else 0
        if expected and actual != expected:
            raise DownloadError(f"大小不一致: 预期 {expected}, 实际 {actual}")
        shutil.move(str(final_tmp), str(dest))

        sha = None
        if self.sha256:
            sha = self._hash(dest, "sha256")
            if sha != self.sha256:
                raise DownloadError(f"SHA-256 不匹配: 期望 {self.sha256}, 实际 {sha}")
        if self.md5:
            md = self._hash(dest, "md5")
            if md != self.md5:
                raise DownloadError(f"MD5 不匹配: 期望 {self.md5}, 实际 {md}")

        elapsed = time.time() - start
        return DownloadReport(
            url=self.url,
            dest=dest,
            filename=self.filename,
            bytes_downloaded=actual,
            elapsed_sec=round(elapsed, 2),
            chunks=chunks,
            resumed=bool(resumed),
            verified=True,
            final_url=self._final_url,
            content_type=self._content_type,
            sha256=sha,
            expected_size=expected,
        )

    # ---------- 单流下载（含断点续传）----------
    def _download_single(self, part: Path) -> None:
        offset = 0
        if part.exists() and self.resume:
            offset = part.stat().st_size
        extra = {"Range": f"bytes={offset}-"} if offset > 0 else {}
        with self._request("GET", extra) as r:
            if r.status not in (200, 206):
                raise DownloadError(f"HTTP 状态异常: {r.status}")
            with open(part, "ab" if offset else "wb") as f:
                self._copy_stream(r, f, hint=offset)

    def _copy_stream(self, src, dst, hint: int = 0):
        downloaded = hint
        expected = self._content_length or 0
        while True:
            buf = src.read(1024 * 256)
            if not buf:
                break
            dst.write(buf)
            downloaded += len(buf)
            if self.progress and expected:
                self.progress(downloaded, expected)

    # ---------- 并发分片下载 ----------
    def _download_range_chunks(self, part: Path) -> int:
        total = self._content_length
        if not total or total <= 0:
            return self._download_single(part) or 1
        chunk_count = min(self.split, total)
        chunk_size = (total + chunk_count - 1) // chunk_count
        tmp_root = self.tmp_dir or self.output_dir
        tmp_root.mkdir(parents=True, exist_ok=True)
        piece_map: dict[int, Path] = {}
        with tempfile.TemporaryDirectory(prefix=".chunks.", dir=str(tmp_root)) as td:
            td_path = Path(td)
            futures = {}
            with ThreadPoolExecutor(max_workers=chunk_count) as pool:
                for i in range(chunk_count):
                    start = i * chunk_size
                    end = (start + chunk_size - 1) if i < chunk_count - 1 else total - 1
                    piece = td_path / f"piece.{i:04d}"
                    piece_map[i] = piece
                    futures[pool.submit(self._download_piece, i, start, end, piece)] = i
                for fut in as_completed(futures):
                    fut.result()  # 失败即抛
            with open(part, "wb") as out:
                for i in range(chunk_count):
                    with open(piece_map[i], "rb") as p:
                        shutil.copyfileobj(p, out, length=1024 * 256)
        return chunk_count

    def _download_piece(self, idx: int, start: int, end: int, piece: Path) -> None:
        if piece.exists() and piece.stat().st_size == (end - start + 1):
            return
        extra = {"Range": f"bytes={start}-{end}"}
        with self._request("GET", extra, timeout=self.timeout) as r:
            if r.status not in (200, 206):
                raise DownloadError(f"分片 {idx} 状态异常: {r.status}")
            with open(piece, "wb") as f:
                copied = 0
                need = end - start + 1
                while copied < need:
                    buf = r.read(min(256 * 1024, need - copied))
                    if not buf:
                        break
                    f.write(buf)
                    copied += len(buf)
                    if self.progress and self._content_length:
                        self.progress(start + copied, self._content_length)
                # 不能在 with 内统计文件大小（缓冲未落盘）；用已读字节数判断长度
                if copied != need:
                    raise DownloadError(f"分片 {idx} 长度不足: 已完成 {copied}/{need}")

    # ---------- 哈希 ----------
    @staticmethod
    def _hash(path: Path, algo: str) -> str:
        h = hashlib.new(algo)
        with open(path, "rb") as f:
            for buf in iter(lambda: f.read(1024 * 1024), b""):
                h.update(buf)
        return h.hexdigest()
