#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""零客户端网页引擎桥。

该模块只负责通用流程：探测分享页、递归列出任务、下载任务、实时进度回传。
各网盘细节放在独立驱动中；百度驱动见 ``pancli.baidu_web``。
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


import json
import os
import re
import shutil
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional

# 共享工具函数从 engine 懒加载；engine 的命令为懒代理，运行期才导入本模块。
from pancli.engine import *  # noqa: F401,F403


SECRET_PATTERNS = (
    re.compile(r"(?i)\b(BDUSS|STOKEN|BAIDUID|BDCLND|sekey|jsToken|sign|timestamp)\b\s*[:=]\s*[^\s,;&]+"),
    re.compile(r"(?i)(cookie\s*[:=]\s*)[^\s,;]+"),
    re.compile(r"(?i)(authorization\s*[:=]\s*)[^\s,;]+"),
)


def redact_text(value: Any) -> str:
    """把接口错误中可能夹带的会话字段统一脱敏。"""
    text = str(value or "")
    for pat in SECRET_PATTERNS:
        text = pat.sub(lambda m: (m.group(1) if m.lastindex else "") + "***" if m.lastindex else "***", text)
    return text


class WebEngineError(RuntimeError):
    """带安全分类的网页引擎错误。"""

    def __init__(self, code: str, message: str, *, retryable: bool = False, http_status: int = 0, detail: str = ""):
        super().__init__(message)
        self.code = str(code or "web_error")
        self.message = redact_text(message or "网页引擎失败")
        self.retryable = bool(retryable)
        self.http_status = int(http_status or 0)
        self.detail = redact_text(detail)

    def public(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "retryable": self.retryable,
            "http_status": self.http_status,
            "detail": self.detail,
        }


@dataclass
class RemoteItem:
    """网页引擎中的一个远端文件/目录。"""

    name: str
    is_dir: bool = False
    size: int = 0
    remote_id: str = ""
    remote_path: str = ""
    rel_path: str = ""
    children: List["RemoteItem"] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WebProbe:
    """分享页探测结果；不含 Cookie、签名和会话密钥。"""

    driver: str
    url: str
    title: str = ""
    share_id: str = ""
    share_uk: str = ""
    surl: str = ""
    login_state: int = 0
    password_required: bool = False
    items: List[RemoteItem] = field(default_factory=list)
    total_files: int = 0
    total_bytes: int = 0


def safe_rel_path(value: str, fallback: str = "download.bin") -> str:
    """把远端相对路径限制在目标目录内，保留同名目录结构。"""
    raw = str(value or "").replace("\\", "/")
    parts = []
    for part in raw.split("/"):
        part = part.strip()
        if not part or part in (".", ".."):
            continue
        part = re.sub(r"[\x00-\x1f]", "", part)
        part = part.replace(":", "：")
        if part:
            parts.append(part)
    if not parts:
        parts = [fallback]
    return str(Path(*parts))


def safe_join(root: str | Path, rel_path: str) -> Path:
    base = Path(root).expanduser().resolve()
    rel = safe_rel_path(rel_path)
    dest = (base / rel).resolve()
    try:
        dest.relative_to(base)
    except ValueError as exc:
        raise WebEngineError("unsafe_path", "远端路径越界，已拒绝下载：%s" % rel_path) from exc
    return dest


def extract_pwd_from_url(url: str) -> str:
    try:
        query = urllib.parse.parse_qs(urllib.parse.urlparse(str(url or "")).query)
    except ValueError:
        return ""
    for key in ("pwd", "password", "passcode"):
        values = query.get(key) or []
        if values and values[0].strip():
            return values[0].strip()
    return ""


def _driver_class(driver: str):
    driver = str(driver or "").strip().lower()
    if driver in ("baidu", "baiduweb", "baidu_web"):
        from pancli import baidu_web
        return baidu_web.BaiduWebDriver
    raise WebEngineError("driver_missing", "尚未实现网盘网页驱动：%s" % (driver or "未指定"))


def build_web_plan(url: str, pwd: str = "", target: str = "", driver: str = "baidu", cfg=None) -> Dict[str, Any]:
    """构造延迟执行计划；真正的分享页请求在下载执行阶段进行。"""
    return {
        "driver": driver,
        "url": str(url or ""),
        "pwd": str(pwd or extract_pwd_from_url(url) or ""),
        "target": str(target or ""),
    }


def _append_event(events: Optional[List[Dict[str, Any]]], entry: Dict[str, Any]) -> None:
    if events is not None:
        events.append(entry)


def _sleep_with_control(seconds: float, task_control=None) -> bool:
    """等待重试间隔；返回 False 表示任务已取消。"""
    deadline = time.time() + max(0.0, float(seconds or 0))
    while time.time() < deadline:
        if task_control is not None and task_control.read_state() == "cancelled":
            return False
        time.sleep(min(0.2, max(0.0, deadline - time.time())))
    return True


def _classify_download_error(exc: BaseException) -> WebEngineError:
    if isinstance(exc, WebEngineError):
        return exc
    if isinstance(exc, urllib.error.HTTPError):
        code = "http_%s" % exc.code
        msg = "官方直链返回 HTTP %s" % exc.code
        if exc.code in (401, 403):
            return WebEngineError("auth_required", msg, http_status=exc.code)
        if exc.code == 416:
            return WebEngineError("range_invalid", msg, retryable=True, http_status=exc.code)
        return WebEngineError(code, msg, retryable=exc.code >= 500, http_status=exc.code)
    if isinstance(exc, (TimeoutError, urllib.error.URLError)):
        return WebEngineError("network_error", "网络请求失败：%s" % redact_text(exc), retryable=True)
    return WebEngineError("download_error", redact_text(exc), retryable=True)


def download_http_url(
    url: str,
    dest: str | Path,
    *,
    referer: str = "",
    user_agent: str = "",
    retries: int = 3,
    chunk_size: int = 1024 * 1024,
    progress: Optional[Callable[[int, int], None]] = None,
    task_control=None,
    opener=None,
) -> Dict[str, Any]:
    """带续传和静默重试的直链下载；返回值不含请求头或 Cookie。"""
    target = Path(dest)
    target.parent.mkdir(parents=True, exist_ok=True)
    part = target.with_name(target.name + ".part")
    headers = {"Accept": "*/*", "Connection": "close"}
    if referer:
        headers["Referer"] = referer
    if user_agent:
        headers["User-Agent"] = user_agent
    last_exc: Optional[BaseException] = None
    attempts = max(1, int(retries or 3))
    for attempt in range(1, attempts + 1):
        try:
            offset = part.stat().st_size if part.exists() else 0
            req_headers = dict(headers)
            if offset:
                req_headers["Range"] = "bytes=%d-" % offset
            req = urllib.request.Request(url, headers=req_headers, method="GET")
            open_url = opener.open if opener is not None else urllib.request.urlopen
            with open_url(req, timeout=60) as resp:
                status = int(getattr(resp, "status", 200) or 200)
                content_length = int(resp.headers.get("Content-Length") or 0)
                if status == 416 and offset:
                    expected = content_length
                    if expected and offset >= expected:
                        part.replace(target)
                        return {"ok": True, "path": str(target), "bytes": offset, "resumed": True}
                mode = "ab" if status == 206 and offset else "wb"
                if status not in (200, 206):
                    raise WebEngineError("http_%s" % status, "官方直链返回 HTTP %s" % status, retryable=status >= 500)
                written = 0
                with part.open(mode + "") as fh:
                    while True:
                        if task_control is not None and task_control.read_state() == "cancelled":
                            raise WebEngineError("cancelled", "任务已取消")
                        chunk = resp.read(chunk_size)
                        if not chunk:
                            break
                        fh.write(chunk)
                        written += len(chunk)
                        if progress:
                            progress(offset + written, content_length + offset if content_length else 0)
                if content_length and status == 206:
                    expected_total = offset + content_length
                else:
                    expected_total = (offset + content_length) if content_length else 0
                actual = part.stat().st_size if part.exists() else 0
                if expected_total and actual < expected_total:
                    raise WebEngineError("short_read", "直链下载不完整：%s/%s 字节" % (actual, expected_total), retryable=True)
            part.replace(target)
            return {"ok": True, "path": str(target), "bytes": target.stat().st_size, "resumed": bool(offset)}
        except WebEngineError as exc:
            last_exc = exc
            if not exc.retryable or attempt >= attempts:
                raise
        except BaseException as exc:  # noqa: BLE001 - 统一转换为安全的网页引擎错误
            last_exc = _classify_download_error(exc)
            if not last_exc.retryable or attempt >= attempts:
                raise last_exc
        if not _sleep_with_control(min(2 ** (attempt - 1), 4), task_control):
            raise WebEngineError("cancelled", "任务已取消")
    raise _classify_download_error(last_exc or RuntimeError("download failed"))


def _task_signature(tasks: Iterable[Dict[str, Any]]) -> str:
    payload = "|".join("%s:%s:%s" % (t.get("rel_path", ""), t.get("size", 0), t.get("remote_id", "")) for t in tasks)
    import hashlib
    return hashlib.sha1(payload.encode("utf-8", "replace")).hexdigest()


def _resolve_with_retries(driver, probe, task, *, index=1, attempts=3, task_control=None) -> str:
    """解析官方直链；仅对可重试错误做静默退避，平台限制直接安全失败。"""
    last_exc = None
    total = max(1, int(attempts or 3))
    for attempt in range(1, total + 1):
        try:
            return driver.resolve_download_url(probe, task, index=index)
        except WebEngineError as exc:
            last_exc = exc
            if not exc.retryable or attempt >= total:
                raise
            if not _sleep_with_control(min(2 ** (attempt - 1), 4), task_control):
                raise WebEngineError("cancelled", "任务已取消")
    raise last_exc or WebEngineError("download_error", "无法获取官方直链")


def execute_web_plan(
    plan: Dict[str, Any],
    *,
    emit_events: bool = False,
    live=None,
    task_control=None,
) -> tuple[int, List[Dict[str, Any]]]:
    """执行 ``build_web_plan`` 生成的计划，返回 (rc, 逐文件结果)。"""
    info = plan.get("web") or {}
    driver_name = info.get("driver") or plan.get("drive") or "baidu"
    url = info.get("url") or ""
    pwd = info.get("pwd") or extract_pwd_from_url(url)
    target_root = Path(plan.get("target") or info.get("target") or ".").expanduser()
    target_root.mkdir(parents=True, exist_ok=True)
    results: List[Dict[str, Any]] = []
    driver_cls = _driver_class(driver_name)
    driver = driver_cls(plan.get("cfg") or {}, target_root=target_root)
    if emit_events:
        print(json.dumps({"event": "web_probe_start", "driver": driver_name}, ensure_ascii=False), flush=True)
    try:
        probe = driver.probe(url, pwd=pwd)
    except WebEngineError as exc:
        entry = {
            "index": 1,
            "engine": "webengine",
            "note": "探测分享页失败",
            "argv": [],
            "rc": 1,
            "elapsed": 0.0,
            "error": exc.message,
            "error_code": exc.code,
            "retryable": exc.retryable,
        }
        results.append(entry)
        if live is not None:
            live.set_web_state("failed", current_file="", local_path=str(target_root), message=exc.message)
        if emit_events:
            print(json.dumps({"event": "web_probe_error", **exc.public()}, ensure_ascii=False), flush=True)
        return 1, results
    tasks = driver.list_tasks(probe)
    total_bytes = max(0, int(probe.total_bytes or sum(int(t.get("size") or 0) for t in tasks)))
    plan["detected"] = {
        "driver": probe.driver,
        "title": probe.title,
        "share_id": probe.share_id,
        "share_uk_present": bool(probe.share_uk),
        "login_state": probe.login_state,
        "password_required": probe.password_required,
        "files_total": len(tasks),
        "total_bytes": total_bytes,
        "task_signature": _task_signature(tasks),
    }
    if live is not None:
        live.configure_web_queue(
            files_total=len(tasks),
            total_bytes=total_bytes,
            title=probe.title,
            local_path=str(target_root),
        )
    if emit_events:
        print(json.dumps({
            "event": "web_probe_done",
            "title": probe.title,
            "files_total": len(tasks),
            "total_bytes": total_bytes,
        }, ensure_ascii=False), flush=True)
    if not tasks:
        if live is not None:
            live.set_web_state("failed", current_file="", local_path=str(target_root), message="分享页没有可下载文件")
        return 1, results

    completed = 0
    failed = 0
    last_platform_error: Optional[WebEngineError] = None
    for idx, task in enumerate(tasks, start=1):
        if task_control is not None:
            state = task_control.read_state()
            if state == "cancelled":
                if live is not None:
                    live.set_web_state("cancelled", current_file=task.get("name", ""), local_path=task.get("local_path", ""), message="任务已取消")
                return 130, results
            while state == "paused":
                if live is not None:
                    live.set_web_state("paused", current_file=task.get("name", ""), local_path=task.get("local_path", ""), message="任务已暂停")
                time.sleep(0.2)
                state = task_control.read_state()
        rel_path = task.get("rel_path") or task.get("name") or ("file-%d" % idx)
        dest = safe_join(target_root, rel_path)
        task["local_path"] = str(dest)
        entry = {
            "index": idx,
            "engine": "webengine",
            "note": "下载 %s" % task.get("name", ""),
            "argv": [],
            "rc": -1,
            "elapsed": 0.0,
            "error": "",
            "name": task.get("name", ""),
            "rel_path": rel_path,
            "local_path": str(dest),
            "size": int(task.get("size") or 0),
            "files_total": len(tasks),
            "file_index": idx,
        }
        results.append(entry)
        if live is not None:
            live.set_web_file(task, index=idx, files_total=len(tasks), state="running", message="获取官方直链")
        if emit_events:
            print(json.dumps({"event": "file_start", "index": idx, "name": task.get("name", ""), "rel_path": rel_path}, ensure_ascii=False), flush=True)

        started = time.time()
        try:
            # 每个文件单独解析官方直链，避免多文件 batch 被平台整体拒绝。
            file_total = int(task.get("size") or 0)
            if dest.exists() and dest.stat().st_size == file_total:
                entry["rc"] = 0
                entry["bytes"] = file_total
                entry["resumed"] = True
                completed += 1
                if live is not None:
                    live.finish_web_file(task, successful=True, bytes_value=file_total, index=idx, files_total=len(tasks))
                    live.set_web_file(task, index=idx, files_total=len(tasks), state="done", message="已完成，跳过重复下载")
                if emit_events:
                    print(json.dumps({"event": "file_skip", "index": idx, "name": task.get("name", ""), "rc": 0}, ensure_ascii=False), flush=True)
                continue
            direct_url = _resolve_with_retries(driver, probe, task, index=idx, task_control=task_control)

            def _progress(done_total: int, _total: int, *, _idx=idx, _name=task.get("name", ""), _dest=dest) -> None:
                if live is None:
                    return
                current = max(0, int(done_total or 0))
                live.update_web_bytes(current, file_total=file_total, current_file=_name, local_path=str(_dest))

            dl = driver.download(direct_url, dest, progress=_progress, task_control=task_control)
            entry["rc"] = 0
            entry["bytes"] = int(dl.get("bytes") or (dest.stat().st_size if dest.exists() else 0))
            entry["resumed"] = bool(dl.get("resumed"))
            completed += 1
            if live is not None:
                live.finish_web_file(task, successful=True, bytes_value=entry["bytes"], index=idx, files_total=len(tasks))
                live.set_web_file(task, index=idx, files_total=len(tasks), state="done", message="完成")
            if emit_events:
                print(json.dumps({"event": "file_done", "index": idx, "name": task.get("name", ""), "rc": 0}, ensure_ascii=False), flush=True)
        except WebEngineError as exc:
            entry["rc"] = 130 if exc.code == "cancelled" else 1
            entry["error"] = exc.message
            entry["error_code"] = exc.code
            entry["retryable"] = exc.retryable
            if exc.code == "cancelled":
                failed += 1
                if live is not None:
                    live.set_web_state("cancelled", current_file=task.get("name", ""), local_path=str(dest), message="任务已取消")
                return 130, results
            failed += 1
            if live is not None:
                live.finish_web_file(task, successful=False, error=exc.message, index=idx, files_total=len(tasks))
            if exc.code in ("captcha_required", "risk_control", "platform_denied", "auth_required", "member_required", "paid_required", "unsupported"):
                last_platform_error = exc
            if emit_events:
                print(json.dumps({"event": "file_error", "index": idx, "name": task.get("name", ""), **exc.public()}, ensure_ascii=False), flush=True)
        except BaseException as exc:  # noqa: BLE001
            safe = _classify_download_error(exc)
            entry["rc"] = 1
            entry["error"] = safe.message
            entry["error_code"] = safe.code
            failed += 1
            if live is not None:
                live.finish_web_file(task, successful=False, error=safe.message, index=idx, files_total=len(tasks))
            if emit_events:
                print(json.dumps({"event": "file_error", "index": idx, "name": task.get("name", ""), **safe.public()}, ensure_ascii=False), flush=True)
        finally:
            entry["elapsed"] = round(time.time() - started, 2)

    rc = 0 if failed == 0 and completed == len(tasks) else 1
    if live is not None:
        if rc == 0:
            live.set_web_state("done", current_file="", local_path=str(target_root), message="全部完成")
        else:
            message = last_platform_error.message if last_platform_error is not None else "部分文件下载失败"
            live.set_web_state("failed", current_file="", local_path=str(target_root), message=message)
    return rc, results
