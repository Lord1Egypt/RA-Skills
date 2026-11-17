#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pan-downloader — 下载报告 / 实时速度 / 任务控制（LiveMonitor、TaskControl）子模块。"""
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
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import threading
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

# 共享工具函数从 engine 懒加载（engine 的命令为懒代理，运行期才 import 本模块，避免循环引用）。
from pancli.engine import *  # noqa: F401,F403

def redact_url(url):
    """仅隐藏分享提取码等 URL 凭据，不保留明文。"""
    try:
        parts = urllib.parse.urlsplit(str(url or ""))
        if not parts.query:
            return str(url or "")
        pairs = urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
        pairs = [(k, "***" if k.lower() in ("pwd", "password", "passcode") else v) for k, v in pairs]
        return urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path, urllib.parse.urlencode(pairs), parts.fragment))
    except (TypeError, ValueError):
        return str(url or "")

def web_state_root(cfg):
    """统一保存 Web UI 所需的实时状态、报告和任务控制文件。"""
    cfg = cfg or {}
    http = cfg.get("http") or {}
    live_dir = (http.get("live_dir") or "").strip()
    if live_dir:
        return Path(live_dir).expanduser()
    report_dir = (http.get("report_dir") or "").strip()
    if report_dir:
        return Path(report_dir).expanduser()
    return Path(STATE_DIR).expanduser() / "web"


def _state_key(target):
    return hashlib.sha1(str(target or ".").encode("utf-8")).hexdigest()[:12]


def report_path_for_target(cfg, target):
    return web_state_root(cfg) / _state_key(target) / "下载报告.json"


AUTH_LOGIN_CODES = ("auth_required", "dlink_missing")
PLATFORM_LOGIN_CODES = ("member_required", "paid_required", "captcha_required", "risk_control", "platform_denied")


def report_login_required(results):
    """任一文件因未登录/拿不到直链失败，即认为该分享需要登录态。"""
    for r in results or []:
        if (r or {}).get("error_code") in AUTH_LOGIN_CODES:
            return True
    return False


def report_remediation(results):
    """把失败码翻译成下一步动作，避免"闷头失败"后无指引。"""
    codes = {(r or {}).get("error_code") for r in (results or [])}
    if codes & set(AUTH_LOGIN_CODES):
        return ("该分享需要百度账号登录态：BaiduPCS-Go 无内置扫码，请运行 "
                "`pan login baidu --qr` 用百度网盘 App 扫码，然后 "
                "`pan get <链接> --engine baidupcs`（分享文件先转存到自己的网盘）。")
    if codes & set(PLATFORM_LOGIN_CODES):
        return "官方返回验证码/风控/会员限制：按官方要求处理，工具不绕过。"
    return ""


def write_download_report(cfg, plan, results, started, finished, ok, url=""):
    path = report_path_for_target(cfg, plan.get("target", ""))
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        body = {
            "schema": 1,
            "ok": bool(ok),
            "url": redact_url(url),
            "drive": plan.get("drive", ""),
            "drive_name": plan.get("drive_name", ""),
            "engine": plan.get("engine", ""),
            "tier": plan.get("tier", ""),
            "target": plan.get("target", ""),
            "started": started.isoformat() if hasattr(started, "isoformat") else str(started),
            "finished": finished.isoformat() if hasattr(finished, "isoformat") else str(finished),
            "elapsed": round((finished - started).total_seconds(), 2) if hasattr(finished, "timestamp") else 0.0,
            "steps": results,
            "missing": plan.get("missing", []),
            "warnings": plan.get("warnings", []),
            "login_required": report_login_required(results),
            "remediation": report_remediation(results),
        }
        with path.open("w", encoding="utf-8") as fh:
            json.dump(body, fh, ensure_ascii=False, indent=2)
        return str(path)
    except OSError as exc:
        log_line("REPORT_FAILED %s %s" % (path, exc))
        return ""


def run_completion_hook(cfg, plan, report_path, url=""):
    hook = ((cfg.get("http") or {}).get("on_complete_hook") or "").strip()
    if not hook:
        return ""
    target = plan.get("target", "")
    argv = shlex.split(hook.format(
        target=target, drive=plan.get("drive", ""), engine=plan.get("engine", ""),
        report=report_path or "", url=url, tier=plan.get("tier", ""),
    ))
    # 安全修复：钩子可执行任意命令，执行前必须通过白名单校验。
    # cfg["http"]["hook_whitelist"] 为允许的目录列表（或 "-" 表示显式放行全部，不推荐）；
    # 未配置白名单时一律拒绝执行并记日志。
    whitelist = [str(x) for x in ((cfg.get("http") or {}).get("hook_whitelist") or [])]
    exe = argv[0] if argv else ""
    exe_path = Path(exe).expanduser()
    allowed = False
    if whitelist == ["-"]:
        allowed = True  # 显式全放行（不推荐，仅本机完全可信环境）
    elif exe_path.is_absolute() and exe_path.exists():
        import sys as _sys
        resolved = str(exe_path.resolve())
        for d in whitelist:
            try:
                if resolved.startswith(str(Path(d).expanduser().resolve()) + os.sep) or resolved == str(Path(d).expanduser().resolve()):
                    allowed = True
                    break
            except OSError:
                continue
        if not allowed and shutil.which(exe) and any(
            str(Path(shutil.which(exe)).resolve()).startswith(str(Path(d).expanduser().resolve()) + os.sep)
            for d in whitelist if Path(d).expanduser().exists()
        ):
            allowed = True
    if not allowed:
        log_line("HOOK_BLOCKED argv0=%s 未在 hook_whitelist 目录内，拒绝执行（白名单配置见 config.http.hook_whitelist）" % exe)
        return ""
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=60)
        log_line("HOOK exit=%s argv=%s" % (proc.returncode, " ".join(mask_argv(argv))))
        msg = (proc.stdout or "").strip().splitlines()
        return (msg[0][:200] if msg else "")
    except (OSError, subprocess.TimeoutExpired) as exc:
        log_line("HOOK_FAILED %s %s" % (" ".join(mask_argv(argv)), exc))
        return ""


LIVE_FILE_NAME = "下载速度.live.json"

_SIZE_RE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*([KMGT]?B)\s*$", re.I)
_BAIDUPCS_PROGRESS_RE = re.compile(
    r"^\[(\d+)\]\s*↓\s*([0-9]+(?:\.[0-9]+)?\s*[KMGT]?B)\s*/\s*"
    r"([0-9]+(?:\.[0-9]+)?\s*[KMGT]?B)\s+"
    r"([0-9]+(?:\.[0-9]+)?\s*[KMGT]?B)/s\s+in\s+(\S+)"
    r"(?:\s*,?\s*left\s+(\S+))?",
    re.I,
)
_DURATION_RE = re.compile(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+(?:\.\d+)?)s)?$", re.I)


def size_text_to_bytes(value):
    """把 BaiduPCS-Go 的 12.3MB / 0B 大小文本转换为字节。"""
    match = _SIZE_RE.match(str(value or ""))
    if not match:
        return 0
    number = float(match.group(1))
    unit = match.group(2).upper()
    factor = {"B": 1, "KB": 1024, "MB": 1048576, "GB": 1073741824, "TB": 1099511627776}[unit]
    return int(number * factor)


def duration_text_to_seconds(value):
    """把 1h2m3s / 13m14s / - 转换成秒；未知返回 None。"""
    text = str(value or "").strip()
    if not text or text == "-":
        return None
    match = _DURATION_RE.fullmatch(text)
    if not match:
        return None
    hours, minutes, seconds = match.groups()
    total = int(hours or 0) * 3600 + int(minutes or 0) * 60 + float(seconds or 0)
    return round(total, 1)


def parse_baidupcs_progress(text):
    """解析 BaiduPCS-Go 日志中的并发分片进度。

    只读取进度行，不读取账号、Cookie、签名或下载 URL。返回的 batch_* 字段适合
    在外部引擎无法逐字节回调时接入 Web UI；overall 进度仍由目标目录实际字节计算。
    """
    queues = {}
    prepared = {}
    local_paths = {}
    shards = {}
    seen = 0
    for raw in str(text or "").splitlines():
        line = raw.strip()
        match = re.match(r"^\[(\d+)\]\s*(加入下载队列|准备下载):\s*(.+)$", line)
        if match:
            index = int(match.group(1))
            path = match.group(3).strip()
            if match.group(2) == "加入下载队列":
                queues[index] = path
            else:
                prepared[index] = path
            continue
        match = re.match(r"^\[(\d+)\]\s*将会下载到路径:\s*(.+)$", line)
        if match:
            local_paths[int(match.group(1))] = match.group(2).strip()
            continue
        match = _BAIDUPCS_PROGRESS_RE.match(line)
        if not match:
            continue
        seen += 1
        index = int(match.group(1))
        done = size_text_to_bytes(match.group(2))
        total = size_text_to_bytes(match.group(3))
        speed = size_text_to_bytes(match.group(4)) / 1024.0
        left = match.group(6)
        remote_path = prepared.get(index) or queues.get(index, "")
        local_path = local_paths.get(index, "")
        shards[index] = {
            "index": index,
            "done_bytes": done,
            "total_bytes": total,
            "speed_kbps": round(max(0.0, speed), 2),
            "eta_seconds": duration_text_to_seconds(left),
            "source": remote_path,
            "local_path": local_path,
            "name": Path(local_path).name or Path(remote_path).name,
            "line": line,
            "_seen": seen,
        }
    values = list(shards.values())
    active = [x for x in values if x["total_bytes"] <= 0 or x["done_bytes"] < x["total_bytes"]]
    batch_done = sum(max(0, x["done_bytes"]) for x in values)
    batch_total = sum(max(0, x["total_bytes"]) for x in values)
    speed_total = sum(max(0.0, x["speed_kbps"]) for x in values)
    current = max(values, key=lambda x: x.get("_seen", 0)) if values else {}
    for value in values:
        value.pop("_seen", None)
    return {
        "ok": bool(values),
        "active_shards": len(active),
        "shards": values,
        "batch_done_bytes": batch_done,
        "batch_total_bytes": batch_total,
        "batch_percent": round(batch_done * 100.0 / batch_total, 1) if batch_total else None,
        "batch_eta_seconds": round((batch_total - batch_done) / 1024.0 / speed_total, 1)
        if speed_total > 0 and batch_total > batch_done else None,
        "speed_kbps": round(speed_total, 2),
        "stalled": bool(active) and speed_total <= 0.5,
        "current_file": current.get("name", ""),
        "current_local_path": current.get("local_path", ""),
    }


def read_text_tail(path, max_bytes=1048576):
    """高效读取文本文件尾部，供长下载日志实时采样。"""
    try:
        handle_path = Path(path).expanduser()
        size = handle_path.stat().st_size
        with handle_path.open("rb") as fh:
            if size > max_bytes:
                fh.seek(size - max_bytes)
                fh.readline()
            return fh.read(max_bytes).decode("utf-8", "replace")
    except OSError:
        return ""


def live_file_for(cfg, plan, target=None):
    target_path = str(target or plan.get("target") or ".")
    return web_state_root(cfg) / _state_key(target_path) / LIVE_FILE_NAME


class LiveMonitor:
    """下载期间周期性采样目标目录字节增量，写入实时速度状态 JSON 文件。"""

    HISTORY_CAP = 300

    def __init__(self, cfg, plan, url="", interval=1.0, progress_log=None):
        self.cfg = cfg
        self.plan = plan
        self.url = url or ""
        self.interval = max(0.3, float(interval or 1.0))
        self.progress_log = Path(progress_log).expanduser() if progress_log else None
        self.target = Path(plan.get("target") or ".")
        self.live_path = live_file_for(cfg, plan)
        self._stop = threading.Event()
        self._thread = None
        self.state = "running"
        self.started = time.time()
        self.last_bytes = 0
        self.last_ts = None
        self.current_step = ""
        self._baseline = self._total_bytes()
        self._progress_offset = self._baseline
        self.total_bytes = 0
        try:
            self.total_bytes = int(plan.get("total_bytes") or 0)
        except (TypeError, ValueError):
            self.total_bytes = 0
        self.history = []  # [(elapsed_seconds, speed_kbps), ...] 画曲线用
        self.files_total = 0
        self.files_done = 0
        self.files_failed = 0
        self.current_file = ""
        self.local_path = str(self.target)
        self.file_bytes = 0
        self.file_size = 0
        self.file_percent = None
        self.status_text = ""
        self._web_mode = False
        self._web_bytes_done = 0
        self._web_completed_bytes = 0
        self.external_progress = {}

    def attach_progress_log(self, path):
        """接入 BaiduPCS-Go 等外部引擎的文本进度日志。"""
        self.progress_log = Path(path).expanduser() if path else None
        return self.progress_log

    def _read_external_progress(self):
        if not self.progress_log:
            return {}
        parsed = parse_baidupcs_progress(read_text_tail(self.progress_log))
        self.external_progress = parsed if parsed.get("ok") else {}
        return self.external_progress

    def _total_bytes(self):
        total = 0
        try:
            if self.target.exists():
                for p in self.target.rglob("*"):
                    if p.is_file() and p.name != LIVE_FILE_NAME:
                        try:
                            total += p.stat().st_size
                        except OSError:
                            pass
        except OSError:
            pass
        return total

    def set_step(self, note=""):
        self.current_step = note or ""

    def set_total_bytes(self, value):
        try:
            value = int(value)
        except (TypeError, ValueError):
            return self.total_bytes
        self.total_bytes = max(0, value)
        return self.total_bytes

    def configure_web_queue(self, *, files_total=0, total_bytes=0, title="", local_path=""):
        """初始化网页桥的逐文件队列；总进度按实际下载字节计算。"""
        self._web_mode = True
        self.files_total = max(0, int(files_total or 0))
        self.files_done = 0
        self.files_failed = 0
        self.total_bytes = max(0, int(total_bytes or 0))
        self.current_file = title or ""
        self.local_path = str(local_path or self.target)
        self._web_bytes_done = 0
        self._web_completed_bytes = 0
        self._baseline = 0
        self._progress_offset = 0
        self.last_bytes = 0

    def set_web_file(self, task, *, index=1, files_total=None, state="running", message=""):
        self._web_mode = True
        if files_total is not None:
            self.files_total = max(0, int(files_total or 0))
        self.current_file = str((task or {}).get("name") or (task or {}).get("rel_path") or "")
        self.local_path = str((task or {}).get("local_path") or self.local_path or self.target)
        self.file_size = max(0, int((task or {}).get("size") or 0))
        self.file_bytes = 0
        self.file_percent = 0.0 if self.file_size else None
        self.status_text = message or state

    def update_web_bytes(self, done_total, *, file_total=0, current_file="", local_path=""):
        self._web_mode = True
        self.current_file = current_file or self.current_file
        self.local_path = local_path or self.local_path
        self.file_size = max(0, int(file_total or self.file_size or 0))
        self.file_bytes = max(0, int(done_total or 0))
        self.file_percent = round(self.file_bytes * 100.0 / self.file_size, 1) if self.file_size > 0 else None
        self._web_bytes_done = self._web_completed_bytes + self.file_bytes

    def finish_web_file(self, task, *, successful=True, bytes_value=0, error="", index=1, files_total=None):
        self._web_mode = True
        if files_total is not None:
            self.files_total = max(0, int(files_total or 0))
        value = max(0, int(bytes_value or 0))
        if successful:
            self.files_done += 1
            self._web_completed_bytes += value
            self._web_bytes_done = self._web_completed_bytes
            self.file_bytes = 0
            self.file_percent = 100.0 if value else None
            self.status_text = "已完成"
        else:
            self.files_failed += 1
            self._web_bytes_done = self._web_completed_bytes
            self.file_bytes = 0
            self.status_text = error or "下载失败"

    def set_web_state(self, state, *, current_file="", local_path="", message=""):
        self.state = str(state or self.state)
        if current_file:
            self.current_file = str(current_file)
        if local_path:
            self.local_path = str(local_path)
        if message:
            self.status_text = str(message)

    def start(self):
        """启动后台线程：按 interval 周期采样并写入实时速度 JSON，直到 stop() 为止。"""
        if self._thread and self._thread.is_alive():
            return self._thread

        def _loop():
            interval = max(0.3, self.interval)
            while not self._stop.is_set():
                try:
                    self.write(state=self.state)
                except Exception as exc:  # 监控线程异常不应中断下载
                    log_line("LIVE_LOOP_ERR %s" % exc)
                self._stop.wait(interval)

        self._thread = threading.Thread(target=_loop, daemon=True, name="pan-live-monitor")
        self._thread.start()
        return self._thread

    def _sample(self):
        now = time.time()
        cur = self._web_bytes_done if self._web_mode else self._total_bytes()
        dt = (now - self.last_ts) if self.last_ts else 0.0
        speed = 0.0
        if dt and dt > 0:
            speed = (cur - self.last_bytes) / dt / 1024.0
        self.last_bytes, self.last_ts = cur, now
        elapsed = max(0.0, now - self.started)
        done = max(0, cur - (0 if self._web_mode else self._progress_offset))
        external = self._read_external_progress()
        if external and self._progress_offset == 0 and not self._web_mode:
            avg = float(external.get("speed_kbps") or 0.0)
        else:
            avg = (done / elapsed / 1024.0) if elapsed > 0 else 0.0
        if external:
            speed = max(speed, float(external.get("speed_kbps") or 0.0))
            if external.get("current_file"):
                self.current_file = external.get("current_file", "")
            if external.get("current_local_path"):
                self.local_path = external.get("current_local_path", "")
            active = int(external.get("active_shards") or 0)
            self.current_step = "百度网盘下载（%d 个并发分片）" % active if active else "百度网盘下载"
        self.history.append((round(elapsed, 2), max(speed, 0.0)))
        if len(self.history) > self.HISTORY_CAP:
            self.history = self.history[-self.HISTORY_CAP:]
        return done, max(speed, 0.0), max(avg, 0.0), elapsed

    def write(self, state=None):
        done, speed, avg, elapsed = self._sample()
        external = self.external_progress or {}
        status_text = self.status_text
        stalled = bool(external.get("stalled")) and speed <= 0.5
        if state != "done" and external:
            if stalled:
                status_text = "百度端暂时 0 B/s，可能限速或在等待分片，下载进程仍保留断点"
            elif external.get("active_shards"):
                status_text = "%d 个分片下载中，当前批次 %.1f%%" % (
                    int(external.get("active_shards") or 0), float(external.get("batch_percent") or 0.0))
        body = {
            "schema": 1,
            "state": state or self.state,
            "url": redact_url(self.url),
            "drive": self.plan.get("drive", ""),
            "drive_name": self.plan.get("drive_name", ""),
            "engine": self.plan.get("engine", ""),
            "tier": self.plan.get("tier", ""),
            "target": str(self.target),
            "started": datetime.fromtimestamp(self.started).strftime("%Y-%m-%dT%H:%M:%S%z"),
            "updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
            "elapsed": round(elapsed, 2),
            "bytes_done": int(done),
            "speed_kbps": round(speed, 2),
            "avg_speed_kbps": round(avg, 2),
            "total_bytes": int(self.total_bytes or 0),
            "percent": round(done * 100.0 / self.total_bytes, 1) if self.total_bytes and self.total_bytes > 0 else None,
            "eta_seconds": round((self.total_bytes - done) / 1024.0 / avg, 1) if (self.total_bytes and self.total_bytes > 0 and avg and avg > 0) else None,
            "history": [[t, v] for (t, v) in self.history],
            "current_step": self.current_step,
            "files_total": int(self.files_total or 0),
            "files_done": int(self.files_done or 0),
            "files_failed": int(self.files_failed or 0),
            "current_file": self.current_file,
            "local_path": self.local_path,
            "file_bytes": int(self.file_bytes or 0),
            "file_size": int(self.file_size or 0),
            "file_percent": self.file_percent,
            "status_text": status_text,
            "active_shards": int(external.get("active_shards") or 0),
            "batch_done_bytes": int(external.get("batch_done_bytes") or 0),
            "batch_total_bytes": int(external.get("batch_total_bytes") or 0),
            "batch_percent": external.get("batch_percent"),
            "batch_eta_seconds": external.get("batch_eta_seconds"),
            "stalled": stalled,
        }
        try:
            self.live_path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.live_path.with_suffix(self.live_path.suffix + ".tmp")
            tmp.write_text(json.dumps(body, ensure_ascii=False), encoding="utf-8")
            tmp.replace(self.live_path)
        except OSError as exc:
            log_line("LIVE_WRITE_FAIL %s %s" % (self.live_path, exc))
        return body

    def stop(self, ok=True):
        if self._stop.is_set() and self.state not in ("done", "failed"):
            self.state = "running"
        self.state = "done" if ok else "failed"
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=self.interval * 3 + 1)
        self.write(state=self.state)


def _pid_is_alive(pid):
    if not pid:
        return True
    try:
        os.kill(int(pid), 0)
        return True
    except PermissionError:
        return True
    except (OSError, ValueError):
        return False


def cmd_live_attach(args):
    """把外部 BaiduPCS-Go 下载日志接入 Web UI 实时页。"""
    cfg = load_config()
    state_dir = str(getattr(args, "state_dir", "") or "").strip()
    if state_dir:
        cfg = json.loads(json.dumps(cfg))
        cfg.setdefault("http", {})["live_dir"] = state_dir
    target = Path(str(getattr(args, "target", "") or ".")).expanduser().resolve()
    log_path = Path(str(getattr(args, "log", "") or "")).expanduser().resolve()
    plan = {
        "target": str(target),
        "drive": "baidu",
        "drive_name": "百度网盘",
        "engine": "baidupcs",
        "tier": "auto",
    }
    interval = float(getattr(args, "interval", 1.0) or 1.0)
    monitor = LiveMonitor(cfg, plan, url=getattr(args, "url", "") or "", interval=interval, progress_log=log_path)
    if getattr(args, "total_bytes", 0):
        monitor.set_total_bytes(args.total_bytes)
    if getattr(args, "files_total", 0):
        monitor.files_total = max(0, int(args.files_total))
    # 外部下载可能在接入监控前已写入部分文件，整体进度按目录现有字节计算。
    monitor._progress_offset = 0
    monitor.last_bytes = monitor._total_bytes()
    monitor.current_step = "百度网盘下载（外部 BaiduPCS-Go 进程）"
    monitor.local_path = str(target)
    if getattr(args, "open", False):
        from pancli.web import ensure_web_ui
        info = ensure_web_ui(cfg, open_browser=True)
        if not getattr(args, "json", False):
            print("实时状态：%s/live" % info.get("url", "") if info.get("ok") else "Web UI 未启动：%s" % info.get("error", ""))
    if getattr(args, "once", False):
        body = monitor.write(state="running")
        if getattr(args, "json", False):
            print(json.dumps(body, ensure_ascii=False, indent=2))
        else:
            print("已写入实时状态：%s" % monitor.live_path)
            print("下载位置：%s" % target)
        return 0
    monitor.start()
    try:
        while _pid_is_alive(getattr(args, "pid", 0)):
            time.sleep(max(0.3, min(interval, 5.0)))
    except KeyboardInterrupt:
        pass
    markers = []
    try:
        markers = list(target.rglob("*.BaiduPCS-Go-downloading"))
    except OSError:
        pass
    ok = not markers
    monitor.stop(ok=ok)
    if getattr(args, "json", False):
        print(json.dumps(monitor.write(state="done" if ok else "failed"), ensure_ascii=False, indent=2))
    else:
        print(("✅ 外部下载进程已结束：%s" if ok else "⚠️ 外部下载进程已结束，仍有未完成标记：%s") % target)
    return 0 if ok else 1


# ------------------------------------------------------------------ 任务控制
# 任务登记在 http.live_dir / http.report_dir / 目标目录 的“任务控制.json”，
# 供 serve 任务中心和 `pan task ...` 实现 暂停/继续/取消/删除/重试。
TASK_FILE_NAME = "任务控制.json"


def _task_file_for_dir(reports_dir):
    return Path(reports_dir) / TASK_FILE_NAME


def read_task_records(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        recs = data.get("tasks")
        return recs if isinstance(recs, dict) else {}
    except (OSError, json.JSONDecodeError, AttributeError):
        return {}


def _atomic_write_json(path, body):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        tmp.chmod(0o600)
    except OSError:
        pass
    tmp.replace(path)


def task_control_file_for(cfg, plan, target=None):
    """任务控制文件与实时速度文件同目录，便于任务中心集中管理。"""
    return live_file_for(cfg, plan, target=target).with_name(TASK_FILE_NAME)


def _task_id(target):
    import hashlib
    return hashlib.sha1(str(target).encode("utf-8")).hexdigest()[:12]


class TaskControl:
    """任务状态机：running / paused / cancelled / done / failed，落盘到任务控制.json。"""

    def __init__(self, cfg, plan, url="", args=None):
        self.cfg = cfg
        self.plan = plan
        self.url = url or ""
        self.args = dict(args or {})
        self.target = plan.get("target") or "."
        self.path = task_control_file_for(cfg, plan)
        self.task_id = _task_id(self.target)
        self._lock = threading.Lock()

    def register(self):
        rec = self._rec()
        rec["state"] = "running"
        self._mutate(lambda recs: recs.update({self.task_id: rec}) or recs)
        return rec

    def _rec(self):
        return {
            "id": self.task_id,
            "schema": 1,
            "state": "running",
            "url": redact_url(self.url),
            "drive": self.plan.get("drive", ""),
            "drive_name": self.plan.get("drive_name", ""),
            "engine": self.plan.get("engine", ""),
            "tier": self.plan.get("tier", ""),
            "target": str(self.target),
            "pwd_present": bool(self.args.get("pwd")),
            "args": {k: v for k, v in self.args.items() if k != "pwd"},
            "pid": os.getpid(),
            "started": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
            "updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
            "current_step": "",
            "finished": "",
            "rc": None,
        }

    def _mutate(self, fn):
        with self._lock:
            recs = read_task_records(self.path)
            recs = fn(recs) or recs
            _atomic_write_json(self.path, {"schema": 1, "tasks": recs})

    def read_state(self):
        rec = read_task_records(self.path).get(self.task_id) or {}
        return rec.get("state", "running")

    def set_step(self, note=""):
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
        self._mutate(lambda recs: (recs.get(self.task_id) or {}).update(
            {"current_step": note or "", "updated": now}) or recs)

    def finish(self, ok=True, rc=0):
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
        _rc = int(rc or 0)
        state = "cancelled" if _rc == 130 else ("done" if ok else "failed")
        self._mutate(lambda recs: (recs.get(self.task_id) or {}).update(
            {"state": state, "rc": _rc, "finished": now, "updated": now}) or recs)
        return state


def _signal_group(proc, sig):
    try:
        os.killpg(os.getpgid(proc.pid), sig)
    except (OSError, ProcessLookupError, PermissionError):
        pass


def _terminate_group(proc):
    _signal_group(proc, signal.SIGTERM)
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        _signal_group(proc, signal.SIGKILL)
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            pass


def _wait_controlled(proc, tc):
    """在任务状态机控制下等待单个子进程结束；支持暂停/继续/取消。返回 (rc, status)。"""
    suspended = False
    try:
        while True:
            state = tc.read_state()
            if state == "cancelled":
                _terminate_group(proc)
                return (proc.returncode if proc.poll() is not None else 130), "cancelled"
            if state == "paused":
                if not suspended and proc.poll() is None:
                    _signal_group(proc, signal.SIGSTOP)
                    suspended = True
                if proc.poll() is None:
                    while tc.read_state() == "paused" and proc.poll() is None:
                        time.sleep(0.2)
                    if proc.poll() is None:
                        _signal_group(proc, signal.SIGCONT)
                    suspended = False
            elif suspended:
                if proc.poll() is None:
                    _signal_group(proc, signal.SIGCONT)
                suspended = False
            if proc.poll() is not None:
                return proc.returncode, "ok"
            time.sleep(0.2)
    except KeyboardInterrupt:
        _terminate_group(proc)
        return 130, "cancelled"


def _run_step_controlled(argv, kwargs, tc, timeout=0):
    """以可暂停/取消的方式执行单个子进程；返回 (rc, status, error)。"""
    kwargs = dict(kwargs)
    kwargs.pop("timeout", None)
    input_data = kwargs.pop("input", None)
    kwargs.pop("text", None)
    try:
        proc = subprocess.Popen(argv, stdin=subprocess.PIPE if input_data is not None else None,
                                start_new_session=True, **kwargs)
    except (OSError, ValueError) as exc:
        return 127, "error", exc
    if input_data is not None:
        try:
            data = input_data if isinstance(input_data, bytes) else str(input_data).encode("utf-8")
            proc.stdin.write(data)
            proc.stdin.flush()
            proc.stdin.close()
        except (OSError, ValueError):
            pass
    deadline = (time.time() + timeout) if timeout else None
    rc, status = _wait_controlled(proc, tc)
    if status == "cancelled":
        return rc, status, None
    if deadline and time.time() >= deadline:
        _terminate_group(proc)
        return 124, "timeout", None
    return rc, status, None


