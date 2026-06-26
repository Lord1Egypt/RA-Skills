"""
Operation Log - 操作日志与审计追踪

功能：
- 结构化操作日志
- 完整操作链追踪
- 敏感信息脱敏
- 日志持久化（文件/SQLite）
- SOC 2合规报告
"""

from __future__ import annotations

import gzip
import json
import logging
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 日志级别
# =============================================================================

class OpLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# =============================================================================
# 操作类型
# =============================================================================

class OpType(Enum):
    AGENT_START = "agent_start"
    AGENT_END = "agent_end"
    AGENT_CALL = "agent_call"
    API_REQUEST = "api_request"
    API_RESPONSE = "api_response"
    STATE_CHANGE = "state_change"
    WORKFLOW_START = "workflow_start"
    WORKFLOW_END = "workflow_end"
    EXCEPTION = "exception"
    RETRY = "retry"
    USER_ACTION = "user_action"
    APPROVAL = "approval"


# =============================================================================
# 操作日志条目
# =============================================================================

@dataclass
class OpLogEntry:
    """操作日志条目"""
    timestamp: str
    level: OpLevel
    op_type: OpType
    request_id: str
    trace_id: str = ""
    agent_name: str = ""
    action: str = ""
    duration_ms: float = 0.0

    # 数据
    input_summary: Optional[str] = None   # 输入摘要（脱敏后）
    output_summary: Optional[str] = None  # 输出摘要（脱敏后）
    error_message: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    # 关联
    parent_trace_id: Optional[str] = None
    span_id: str = ""

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "level": self.level.value,
            "op_type": self.op_type.value,
            "request_id": self.request_id,
            "trace_id": self.trace_id,
            "agent_name": self.agent_name,
            "action": self.action,
            "duration_ms": round(self.duration_ms, 2),
            "input_summary": self.input_summary,
            "output_summary": self.output_summary,
            "error_message": self.error_message,
            "metadata": self.metadata,
            "parent_trace_id": self.parent_trace_id,
            "span_id": self.span_id,
        }


# =============================================================================
# 敏感信息脱敏器
# =============================================================================

class PIIRedactor:
    """敏感信息脱敏"""

    PATTERNS = {
        "email": (r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "***@***.***"),
        "phone": (r"1[3-9]\d{9}", "1**********"),
        "id_card": (r"\d{17}[\dXx]", "**************?????"),
        "bank_card": (r"\d{12,19}", "****-****-****-????"),
        "password": (r'"password"\s*:\s*"[^"]*"', '"password": "***"'),
        "api_key": (r'(?:api[_-]?key|apikey)\s*[=:]\s*["\']?[\w-]+["\']?',
                    lambda m: m.group(0).split("=")[0] + '= "***"'),
        "token": (r"Bearer\s+[\w.-]+", "Bearer ***"),
        "amount": (r'(?:金额|amount)\s*[=:]\s*[\d.]+', lambda m: re.sub(r'[\d.]+', '***', m.group(0))),
    }

    @classmethod
    def redact(cls, text: str) -> str:
        """脱敏文本中的敏感信息"""
        result = text
        for name, (pattern, replacement) in cls.PATTERNS.items():
            if callable(replacement):
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
            else:
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result

    @classmethod
    def redact_dict(cls, data: dict) -> dict:
        """脱敏字典中的敏感字段"""
        sensitive_keys = {"password", "api_key", "secret", "token", "credential", "auth"}
        result = {}
        for k, v in data.items():
            if any(sk in k.lower() for sk in sensitive_keys):
                result[k] = "***REDACTED***"
            elif isinstance(v, str):
                result[k] = cls.redact(v)
            elif isinstance(v, dict):
                result[k] = cls.redact_dict(v)
            elif isinstance(v, list):
                result[k] = [cls.redact(vv) if isinstance(vv, str) else vv for vv in v]
            else:
                result[k] = v
        return result


# =============================================================================
# 操作日志器
# =============================================================================

class OperationLogger:
    """
    操作日志记录器

    特性：
    - 结构化日志输出
    - 自动脱敏
    - 多输出目标（控制台/文件/gzip压缩）
    - 日志轮转（按大小/时间）
    - SOC 2合规报告生成
    """

    def __init__(
        self,
        log_dir: str = "logs",
        compress: bool = True,
        max_file_size_mb: float = 50.0,
        max_files: int = 10,
    ):
        self.log_dir = Path(log_dir)
        self.compress = compress
        self.max_file_size = int(max_file_size_mb * 1024 * 1024)
        self.max_files = max_files

        self._entries: list[OpLogEntry] = []
        self._current_file_size = 0
        self._current_log_date: Optional[str] = None
        self._file_handle = None

        self.log_dir.mkdir(parents=True, exist_ok=True)

        # 同时输出到标准日志器
        self._std_logger = logging.getLogger("operation")

    def _get_log_file(self) -> Path:
        """获取当日日志文件路径"""
        today = datetime.now().strftime("%Y%m%d")
        if self._current_log_date != today:
            self._current_log_date = today
            self._current_file_size = 0
            if self._file_handle:
                self._file_handle.close()
                self._file_handle = None
        return self.log_dir / f"oplog_{today}.jsonl.gz"

    def _write_entry(self, entry: OpLogEntry):
        """写入日志条目"""
        line = json.dumps(entry.to_dict(), ensure_ascii=False)

        # 检查是否需要轮转
        log_file = self._get_log_file()
        if self._current_file_size + len(line) > self.max_file_size:
            self._rotate_files()

        # 写入
        if self.compress:
            with gzip.open(log_file, "at", encoding="utf-8") as f:
                f.write(line + "\n")
        else:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(line + "\n")

        self._current_file_size += len(line)

    def _rotate_files(self):
        """日志轮转"""
        self._current_file_size = 0
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None

        # 清理旧文件
        files = sorted(self.log_dir.glob("oplog_*.jsonl.gz"))
        if len(files) > self.max_files:
            for old_file in files[:-self.max_files]:
                old_file.unlink()
                logger.info(f"[日志轮转] 删除旧日志: {old_file.name}")

    def log(
        self,
        level: OpLevel,
        op_type: OpType,
        request_id: str,
        message: str = "",
        **kwargs,
    ) -> OpLogEntry:
        """记录操作日志"""
        entry = OpLogEntry(
            timestamp=datetime.now().isoformat(),
            level=level,
            op_type=op_type,
            request_id=request_id,
            **kwargs,
        )

        # 脱敏
        if entry.input_summary:
            entry.input_summary = PIIRedactor.redact(entry.input_summary)
        if entry.output_summary:
            entry.output_summary = PIIRedactor.redact(entry.output_summary)
        if entry.error_message:
            entry.error_message = PIIRedactor.redact(entry.error_message[:200])

        self._entries.append(entry)
        self._write_entry(entry)

        # 标准日志
        std_level = {
            OpLevel.DEBUG: logger.debug,
            OpLevel.INFO: logger.info,
            OpLevel.WARNING: logger.warning,
            OpLevel.ERROR: logger.error,
            OpLevel.CRITICAL: logger.critical,
        }.get(level, logger.info)
        std_level(f"[{op_type.value}] {request_id[:8]} {message}")

        return entry

    # ================================================================
    # 便捷方法
    # ================================================================

    def agent_start(self, agent_name: str, request_id: str, trace_id: str = "", **kwargs):
        return self.log(OpLevel.INFO, OpType.AGENT_START, request_id,
                        f"{agent_name} 开始执行", agent_name=agent_name, trace_id=trace_id, **kwargs)

    def agent_end(self, agent_name: str, request_id: str, duration_ms: float, success: bool, **kwargs):
        level = OpLevel.INFO if success else OpLevel.ERROR
        return self.log(level, OpType.AGENT_END, request_id,
                        f"{agent_name} 执行结束（{duration_ms:.0f}ms）",
                        agent_name=agent_name, duration_ms=duration_ms, **kwargs)

    def api_call(self, request_id: str, api_name: str, duration_ms: float,
                 success: bool, error: Optional[str] = None, **kwargs):
        level = OpLevel.INFO if success else OpLevel.ERROR
        return self.log(level, OpType.API_REQUEST, request_id,
                        f"API调用 {api_name}（{duration_ms:.0f}ms）{'成功' if success else '失败'}",
                        action=api_name, duration_ms=duration_ms,
                        error_message=error, **kwargs)

    def workflow_start(self, workflow_name: str, request_id: str, trace_id: str, task_count: int, **kwargs):
        return self.log(OpLevel.INFO, OpType.WORKFLOW_START, request_id,
                        f"工作流 {workflow_name} 启动（{task_count}个任务）",
                        action=workflow_name, trace_id=trace_id,
                        metadata={"task_count": task_count}, **kwargs)

    def workflow_end(self, workflow_name: str, request_id: str, duration_ms: float, status: str, **kwargs):
        level = OpLevel.INFO if status == "success" else OpLevel.ERROR
        return self.log(level, OpType.WORKFLOW_END, request_id,
                        f"工作流 {workflow_name} 结束（{duration_ms:.0f}ms，{status}）",
                        action=workflow_name, duration_ms=duration_ms, metadata={"status": status}, **kwargs)

    def exception(self, request_id: str, error_type: str, message: str, **kwargs):
        return self.log(OpLevel.ERROR, OpType.EXCEPTION, request_id,
                        f"异常: {error_type}",
                        error_message=f"{error_type}: {message[:200]}", **kwargs)

    def retry(self, request_id: str, attempt: int, max_attempts: int, error: str, delay: float, **kwargs):
        return self.log(OpLevel.WARNING, OpType.RETRY, request_id,
                        f"重试 {attempt}/{max_attempts}（延迟{delay:.1f}s）: {error[:100]}",
                        metadata={"attempt": attempt, "max_attempts": max_attempts, "delay": delay},
                        error_message=error[:200], **kwargs)

    # ================================================================
    # 查询与分析
    # ================================================================

    def query(
        self,
        request_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        agent_name: Optional[str] = None,
        op_type: Optional[OpType] = None,
        level: Optional[OpLevel] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 100,
    ) -> list[OpLogEntry]:
        """查询日志"""
        results: list[OpLogEntry] = []

        for log_file in sorted(self.log_dir.glob("oplog_*.jsonl.gz"), reverse=True):
            try:
                mode = "rt" if self.compress else "r"
                with gzip.open(log_file, mode, encoding="utf-8") as f:
                    for line in f:
                        try:
                            data = json.loads(line.strip())
                            entry = OpLogEntry(**{k: v for k, v in data.items()
                                                   if k in OpLogEntry.__dataclass_fields__})
                        except Exception:
                            continue

                        # 过滤
                        if request_id and entry.request_id != request_id:
                            continue
                        if trace_id and entry.trace_id != trace_id:
                            continue
                        if agent_name and entry.agent_name != agent_name:
                            continue
                        if op_type and entry.op_type != op_type:
                            continue
                        if level and entry.level != level:
                            continue
                        if start_time and entry.timestamp < start_time:
                            continue
                        if end_time and entry.timestamp > end_time:
                            continue

                        results.append(entry)
                        if len(results) >= limit:
                            break

                if len(results) >= limit:
                    break
            except Exception as e:
                logger.warning(f"读取日志文件失败 {log_file}: {e}")

        return sorted(results, key=lambda e: e.timestamp, reverse=True)

    def generate_report(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> dict:
        """生成操作统计报告"""
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=1)

        entries = self.query(
            start_time=start_date.isoformat(),
            end_time=end_date.isoformat(),
            limit=10000,
        )

        # 统计
        op_counts: dict[str, int] = {}
        agent_counts: dict[str, int] = {}
        error_count = 0
        total_duration = 0.0
        requests: set[str] = set()

        for entry in entries:
            requests.add(entry.request_id)
            op_counts[entry.op_type.value] = op_counts.get(entry.op_type.value, 0) + 1
            if entry.agent_name:
                agent_counts[entry.agent_name] = agent_counts.get(entry.agent_name, 0) + 1
            if entry.level in (OpLevel.ERROR, OpLevel.CRITICAL):
                error_count += 1
            if entry.duration_ms > 0:
                total_duration += entry.duration_ms

        return {
            "report_period": f"{start_date.isoformat()} ~ {end_date.isoformat()}",
            "total_requests": len(requests),
            "total_log_entries": len(entries),
            "error_count": error_count,
            "error_rate": round(error_count / max(len(entries), 1) * 100, 2),
            "avg_duration_ms": round(total_duration / max(len(entries), 1), 2),
            "op_type_distribution": dict(sorted(op_counts.items(), key=lambda x: -x[1])[:10]),
            "agent_distribution": dict(sorted(agent_counts.items(), key=lambda x: -x[1])[:10]),
            "recent_errors": [
                e.error_message for e in entries[-20:]
                if e.level in (OpLevel.ERROR, OpLevel.CRITICAL) and e.error_message
            ],
        }
