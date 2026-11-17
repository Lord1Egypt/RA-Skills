"""log_util.py - 统一日志工具：绝对路径 + 标准格式 + 角色标识。

遵循 local-ai-skill-authoring-main best-practices.md §Logging 规范：
  - 日志目录：%USERPROFILE%\\.openvino\\log\\（host 标准）
  - 文件名：<skill>-<role>-<timestamp>.log
  - 格式：[YYYY-MM-DD HH:MM:SS] [role pid=PID] message
  - 使用绝对路径，禁止相对路径

用法：
    from log_util import get_logger
    log = get_logger("client")        # -> ai-literacy-client-<ts>.log
    log.info("准备课程目录")
    log.error("模型不存在")
"""
from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


SKILL_NAME = "ai-literacy"
DEFAULT_LOG_DIR = Path(os.environ.get("USERPROFILE", str(Path.home()))) / ".openvino" / "log"


def _configure_stream_encoding(stream) -> None:
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")


_configure_stream_encoding(sys.stdout)
_configure_stream_encoding(sys.stderr)


def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _ts_for_filename() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


class SkillLogger:
    """轻量级日志器：同时写入文件（绝对路径）和 stderr。"""

    def __init__(self, role: str, log_dir: Optional[Path] = None):
        self.role = role
        self.pid = os.getpid()
        log_dir = log_dir or DEFAULT_LOG_DIR
        log_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = log_dir / f"{SKILL_NAME}-{role}-{_ts_for_filename()}.log"
        self._fp = None
        try:
            self._fp = open(self.log_path, "a", encoding="utf-8")
        except OSError:
            self._fp = None

    def _emit(self, level: str, msg: str) -> None:
        line = f"[{_ts()}] [{self.role} pid={self.pid}] [{level}] {msg}"
        print(line, file=sys.stderr)
        if self._fp:
            try:
                self._fp.write(line + "\n")
                self._fp.flush()
            except OSError:
                pass

    def info(self, msg: str) -> None:
        self._emit("INFO", msg)

    def warn(self, msg: str) -> None:
        self._emit("WARN", msg)

    def error(self, msg: str) -> None:
        self._emit("ERROR", msg)

    def close(self) -> None:
        if self._fp:
            try:
                self._fp.close()
            except OSError:
                pass
            self._fp = None


_default_logger: Optional[SkillLogger] = None


def get_logger(role: str = "client") -> SkillLogger:
    global _default_logger
    if _default_logger is None:
        _default_logger = SkillLogger(role)
    return _default_logger
