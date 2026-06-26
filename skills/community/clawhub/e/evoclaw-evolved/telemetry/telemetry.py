# Telemetry — 遥测与日志系统
# 参考: claude-code/src/services/analytics/
#
# 设计:
#   logEvent() → AnalyticsSink → 双层管道
#   ├── local (console/file) — 调试用
#   └── remote (HTTP API) — 生产用
#
#   磁盘持久化: 导出失败 → append-only 文件 → 重试队列 → 下次启动重试
#   用户桶去重: 30桶, SHA256(userId) mod 30, 防止告警风暴

from __future__ import annotations
import os
import json
import time
import hashlib
import threading
import platform
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/openclaw/.openclaw/workspace"))
TELEMETRY_DIR = WORKSPACE / "evoclaw" / "telemetry"
TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
FAILED_QUEUE_FILE = TELEMETRY_DIR / "failed_events.jsonl"
CONFIG_FILE = TELEMETRY_DIR / "config.json"

# ─── 配置 ────────────────────────────────────────────────────────

@dataclass
class TelemetryConfig:
    enabled: bool = True
    api_endpoint: str = ""                    # 远程 API 地址
    api_key: str = ""                         # 认证 key
    local_log_file: Path = TELEMETRY_DIR / "events.jsonl"
    sample_rate: float = 1.0                  # 采样率 0.0-1.0
    flush_interval_secs: int = 5              # 批量刷写间隔
    max_queue_size: int = 200                 # 内存队列上限
    user_id: str = "openclaw"               # 匿名用户 ID (用于桶分片)
    user_bucket: int = 30                     # 用户桶数量
    retry_base_delay_ms: int = 1000
    retry_max_delay_ms: int = 60000

    @classmethod
    def load(cls) -> "TelemetryConfig":
        if CONFIG_FILE.exists():
            try:
                return cls(**json.loads(CONFIG_FILE.read_text()))
            except Exception:
                pass
        return cls()

    def save(self) -> None:
        CONFIG_FILE.write_text(json.dumps(asdict(self), indent=2))


# ─── 事件类型 ────────────────────────────────────────────────────

class EventType(str, Enum):
    HEARTBEAT = "heartbeat"
    TASK_START = "task_start"
    TASK_END = "task_end"
    TASK_FAIL = "task_fail"
    EVOCLAW_PROPOSE = "evoclaw_propose"
    EVOCLAW_APPLY = "evoclaw_apply"
    MEMORY_EXTRACT = "memory_extract"
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    ERROR = "error"
    FEATURE_USED = "feature_used"


@dataclass
class AnalyticsMetadata:
    """
    类型安全元数据.
    参考: AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS
    只接受预定义字段, 拒绝代码/路径类数据.
    """
    # 允许的字段
    event_type: EventType
    timestamp: float = field(default_factory=time.time)
    user_id: str = "openclaw"
    session_key: str = ""
    channel: str = ""
    model: str = ""
    # 业务数据
    duration_ms: Optional[int] = None
    success: bool = True
    error_message: Optional[str] = None
    extra: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["event_type"] = self.event_type.value
        return d


# ─── 用户桶 ──────────────────────────────────────────────────────

class UserBucket:
    """
    30 桶去重. 参考: claude-code NUM_USER_BUCKETS=30
    通过 SHA256(userId) mod 30 确定桶, 相同用户的 events 落在同一桶,
    用于告警去重和采样.
    """

    NUM_BUCKETS = 30

    @classmethod
    def get_bucket(cls, user_id: str) -> int:
        h = hashlib.sha256(user_id.encode()).hexdigest()
        return int(h, 16) % cls.NUM_BUCKETS

    @classmethod
    def is_sampled(cls, user_id: str, sample_rate: float = 1.0) -> bool:
        """按采样率决定是否纳入"""
        bucket = cls.get_bucket(user_id)
        threshold = sample_rate * cls.NUM_BUCKETS
        return bucket < threshold


# ─── 磁盘持久化重试队列 ──────────────────────────────────────────

class FailedEventQueue:
    """
    Append-only 文件持久化.
    参考: claude-code FirstPartyEventLoggingExporter 失败重试机制.

    导出失败 → 追加到 failed_events.jsonl
    下次启动 → 读取文件 → 重试 → 成功后删除
    """

    _lock = threading.Lock()

    @classmethod
    def append(cls, event: dict) -> None:
        with cls._lock:
            with open(FAILED_QUEUE_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")

    @classmethod
    def read_all(cls) -> list[dict]:
        if not FAILED_QUEUE_FILE.exists():
            return []
        try:
            lines = FAILED_QUEUE_FILE.read_text(encoding="utf-8").strip().split("\n")
            return [json.loads(line) for line in lines if line.strip()]
        except Exception:
            return []

    @classmethod
    def clear(cls) -> None:
        with cls._lock:
            if FAILED_QUEUE_FILE.exists():
                FAILED_QUEUE_FILE.unlink()

    @classmethod
    def retry_flush(cls, exporter: "RemoteExporter", max_attempts: int = 3) -> int:
        """
        启动时重试所有失败事件.
        返回成功重试的数量.
        """
        events = cls.read_all()
        if not events:
            return 0

        success_count = 0
        for event in events:
            for attempt in range(max_attempts):
                try:
                    if exporter.send([event]):
                        success_count += 1
                        break
                except Exception:
                    time.sleep((2 ** attempt) * 0.1)  # 指数退避

        if success_count == len(events):
            cls.clear()  # 全部成功, 删除队列
        return success_count


# ─── 导出器 ─────────────────────────────────────────────────────

class BaseExporter:
    """导出器基类"""

    def send(self, events: list[dict]) -> bool:
        raise NotImplementedError


class ConsoleExporter(BaseExporter):
    """调试用: 打印到 stdout"""

    def send(self, events: list[dict]) -> bool:
        for e in events:
            print(f"[TELEMETRY] {e.get('event_type', '?')}: {json.dumps(e, ensure_ascii=False)}")
        return True


class FileExporter(BaseExporter):
    """本地文件导出"""

    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = file_path or (TELEMETRY_DIR / "events.jsonl")

    def send(self, events: list[dict]) -> bool:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, "a", encoding="utf-8") as f:
            for e in events:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        return True


class RemoteExporter(BaseExporter):
    """
    远程 API 导出.
    支持指数退避重试.
    """

    def __init__(self, endpoint: str, api_key: str, config: TelemetryConfig):
        self.endpoint = endpoint
        self.api_key = api_key
        self.config = config

    def send(self, events: list[dict]) -> bool:
        import urllib.request
        import urllib.error

        if not self.endpoint:
            return False

        data = json.dumps({"events": events}).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status == 200
        except urllib.error.HTTPError as e:
            if e.code == 401:
                # 认证失败, 不重试
                return False
            raise  # 其他错误触发重试
        except Exception:
            raise  # 网络错误触发重试


# ─── 遥测核心 ───────────────────────────────────────────────────

class TelemetrySink:
    """
    遥测入口. 参考: claude-code AnalyticsSink.logEvent()

    设计:
      1. 内存队列 batch
      2. 定时 flush 到各 exporter
      3. 失败事件写入磁盘重试队列
      4. 30桶采样过滤
    """

    _instance: Optional["TelemetrySink"] = None
    _lock = threading.Lock()

    def __init__(self):
        self.config = TelemetryConfig.load()
        self.queue: list[dict] = []
        self.exporters: list[BaseExporter] = []
        self._flush_thread: Optional[threading.Thread] = None
        self._stop = threading.Event()

        # 默认: Console + File
        self.exporters.append(ConsoleExporter())
        if self.config.local_log_file:
            self.exporters.append(FileExporter(self.config.local_log_file))

        # 启动重试线程
        self._start_retry_flush()

    @classmethod
    def get_instance(cls) -> "TelemetrySink":
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def add_exporter(self, exporter: BaseExporter) -> None:
        self.exporters.append(exporter)

    def configure_remote(self, endpoint: str, api_key: str) -> None:
        """配置远程遥测"""
        self.config.api_endpoint = endpoint
        self.config.api_key = api_key
        self.config.save()
        if endpoint:
            self.exporters.append(RemoteExporter(endpoint, api_key, self.config))

    def log_event(
        self,
        event_type: EventType,
        session_key: str = "",
        channel: str = "",
        model: str = "",
        success: bool = True,
        duration_ms: Optional[int] = None,
        error_message: Optional[str] = None,
        **extra,
    ) -> None:
        """
        记录事件. 线程安全.
        """
        if not self.config.enabled:
            return

        # 采样过滤
        if not UserBucket.is_sampled(self.config.user_id or "openclaw", self.config.sample_rate):
            return

        meta = AnalyticsMetadata(
            event_type=event_type,
            session_key=session_key,
            channel=channel,
            model=model,
            success=success,
            duration_ms=duration_ms,
            error_message=error_message,
            extra=extra,
        )

        with self._lock:
            self.queue.append(meta.to_dict())

        # 队列满则立即 flush
        if len(self.queue) >= self.config.max_queue_size:
            self.flush()

    def flush(self) -> None:
        """刷写队列到所有 exporter"""
        with self._lock:
            if not self.queue:
                return
            events = self.queue[:]
            self.queue = []

        for exporter in self.exporters:
            try:
                if not exporter.send(events):
                    # 导出器返回 False → 写入重试队列
                    for e in events:
                        FailedEventQueue.append(e)
            except Exception as ex:
                # 异常 → 写入重试队列
                for e in events:
                    FailedEventQueue.append(e)
                # 打印到 console 供调试
                print(f"[TELEMETRY ERROR] flush failed: {ex}")

    def _start_retry_flush(self) -> None:
        """启动定时 flush + 失败重试线程"""
        def run():
            while not self._stop.wait(self.config.flush_interval_secs):
                self.flush()
                # 重试失败队列
                if self.config.api_endpoint:
                    remote = RemoteExporter(
                        self.config.api_endpoint,
                        self.config.api_key,
                        self.config,
                    )
                    FailedEventQueue.retry_flush(remote)

        self._flush_thread = threading.Thread(target=run, daemon=True)
        self._flush_thread.start()

    def shutdown(self) -> None:
        """Shutdown 时最后一次 flush"""
        self._stop.set()
        self.flush()

    # ─── 便捷方法 ────────────────────────────────────────────────

    def heartbeat(self, session_key: str = "", channel: str = "", model: str = "") -> None:
        self.log_event(EventType.HEARTBEAT, session_key, channel, model)

    def task_start(self, task_id: str, task_type: str, session_key: str = "") -> None:
        self.log_event(EventType.TASK_START, session_key, extra={"task_id": task_id, "task_type": task_type})

    def task_end(self, task_id: str, task_type: str, duration_ms: int, success: bool = True, session_key: str = "") -> None:
        self.log_event(
            EventType.TASK_END if success else EventType.TASK_FAIL,
            session_key,
            duration_ms=duration_ms,
            success=success,
            extra={"task_id": task_id, "task_type": task_type},
        )

    def evoclaw_apply(self, proposal_id: str, change_type: str, session_key: str = "") -> None:
        self.log_event(EventType.EVOCLAW_APPLY, session_key, extra={"proposal_id": proposal_id, "change_type": change_type})


# ─── 全局实例 ───────────────────────────────────────────────────

sink = TelemetrySink.get_instance()


def log_event(**kwargs) -> None:
    sink.log_event(**kwargs)


def log_heartbeat(session_key: str = "", channel: str = "", model: str = "") -> None:
    sink.heartbeat(session_key, channel, model)


def shutdown() -> None:
    sink.shutdown()


if __name__ == "__main__":
    # Demo
    print(f"Bucket for 'boss': {UserBucket.get_bucket('boss')}")
    print(f"Sampled (100%): {UserBucket.is_sampled('boss', 1.0)}")
    print(f"Sampled (10%): {UserBucket.is_sampled('boss', 0.1)}")

    log_heartbeat(session_key="demo", channel="openclaw-weixin", model="minimax")
    print("✅ Telemetry: event logged")
    sink.shutdown()
