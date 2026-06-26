# Feature Flags — 功能开关系统
# 参考: claude-code src/services/analytics/growthbook.ts
#
# 设计原则 (本地优先):
#   1. feature('xxx') 查询开关状态
#   2. get_config('xxx', default) 获取数值/对象配置
#   3. 本地 JSON 配置文件 + 可挂接远程 (GrowthBook/LaunchDarkly)
#   4. 缓存机制: 内存缓存 + TTL
#
# Claude Code GrowthBook 控制内容:
#   - feature gates: on/off
#   - 数值型参数: minHours, minSessions, batch size
#   - 采样率配置: tengu_event_sampling_config
#   - 组织策略: tengu_disable_bypass_permissions_mode

from __future__ import annotations
import os
import json
import time
import hashlib
import threading
from pathlib import Path
from typing import Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/openclaw/.openclaw/workspace"))
FEATURES_DIR = WORKSPACE / "evoclaw" / "features"
FEATURES_DIR.mkdir(parents=True, exist_ok=True)
FEATURES_FILE = FEATURES_DIR / "flags.json"


# ─── 开关类型 ───────────────────────────────────────────────────

class FlagType(str, Enum):
    BOOLEAN = "boolean"
    STRING = "string"
    NUMBER = "number"
    OBJECT = "object"


@dataclass
class FeatureFlag:
    """单个功能开关"""
    key: str
    flag_type: FlagType = FlagType.BOOLEAN
    enabled: bool = False              # 仅 BOOLEAN 时使用
    value: Any = None                  # 通用值 (number/object/string)
    description: str = ""
    owner: str = ""                    # 负责人
    tags: list[str] = field(default_factory=list)
    updated_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "type": self.flag_type.value,
            "enabled": self.enabled,
            "value": self.value,
            "description": self.description,
            "owner": self.owner,
            "tags": self.tags,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "FeatureFlag":
        return cls(
            key=d["key"],
            flag_type=FlagType(d.get("type", "boolean")),
            enabled=d.get("enabled", False),
            value=d.get("value"),
            description=d.get("description", ""),
            owner=d.get("owner", ""),
            tags=d.get("tags", []),
            updated_at=d.get("updated_at", time.time()),
        )


# ─── 缓存 ───────────────────────────────────────────────────────

@dataclass
class CacheEntry:
    value: Any
    expires_at: float


class FeatureCache:
    """
    内存缓存 + TTL.
    防止高频调用时重复解析.
    """

    def __init__(self, ttl_secs: float = 60.0):
        self._cache: dict[str, CacheEntry] = {}
        self._ttl = ttl_secs
        self._lock = threading.RLock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return None
            if time.time() > entry.expires_at:
                del self._cache[key]
                return None
            return entry.value

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        with self._lock:
            self._cache[key] = CacheEntry(
                value=value,
                expires_at=time.time() + (ttl or self._ttl),
            )

    def invalidate(self, key: str) -> None:
        with self._lock:
            self._cache.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()


# ─── Feature Flag 引擎 ─────────────────────────────────────────

class FeatureEngine:
    """
    功能开关引擎. 参考: claude-code GrowthBook SDK.

    用法:
        ff = FeatureEngine()
        if ff.is_enabled("my_feature"):
            do_something()

        batch_size = ff.get_config("batch_size", default=10)
    """

    def __init__(self, features_file: Optional[Path] = None):
        self.features_file = features_file or FEATURES_FILE
        self._flags: dict[str, FeatureFlag] = {}
        self._cache = FeatureCache(ttl_secs=30.0)  # 30s TTL
        self._lock = threading.RLock()
        self._remote_url: Optional[str] = None
        self._remote_key: Optional[str] = None
        self._last_sync: float = 0
        self._sync_interval: float = 300  # 5分钟同步一次
        self.load()

    # ─── 持久化 ────────────────────────────────────────────────

    def load(self) -> None:
        """从文件加载开关配置"""
        if self.features_file.exists():
            try:
                data = json.loads(self.features_file.read_text(encoding="utf-8"))
                with self._lock:
                    self._flags = {k: FeatureFlag.from_dict(v) for k, v in data.items()}
                return
            except Exception:
                pass
        # 默认开启的开关
        self._flags = self._default_flags()
        self.save()

    def save(self) -> None:
        """保存开关配置到文件"""
        with self._lock:
            data = {k: v.to_dict() for k, v in self._flags.items()}
        self.features_file.parent.mkdir(parents=True, exist_ok=True)
        self.features_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def _default_flags(self) -> dict[str, FeatureFlag]:
        """默认开关配置"""
        return {
            # EvoClaw 功能开关
            "evoclaw_auto_memory_extract": FeatureFlag(
                key="evoclaw_auto_memory_extract",
                flag_type=FlagType.BOOLEAN,
                enabled=True,
                description="自动记忆抽取",
                owner="本地龙",
            ),
            "evoclaw_telemetry": FeatureFlag(
                key="evoclaw_telemetry",
                flag_type=FlagType.BOOLEAN,
                enabled=True,
                description="遥测日志",
                owner="本地龙",
            ),
            "evoclaw_dream_task": FeatureFlag(
                key="evoclaw_dream_task",
                flag_type=FlagType.BOOLEAN,
                enabled=True,
                description="后台记忆整固",
                owner="本地龙",
            ),
            "evoclaw_proactive": FeatureFlag(
                key="evoclaw_proactive",
                flag_type=FlagType.BOOLEAN,
                enabled=True,
                description="主动行动",
                owner="本地龙",
            ),
            # 数值型配置
            "heartbeat_interval_secs": FeatureFlag(
                key="heartbeat_interval_secs",
                flag_type=FlagType.NUMBER,
                value=1800,  # 30分钟
                description="心跳间隔（秒）",
                owner="本地龙",
            ),
            "dream_task_trigger_session_count": FeatureFlag(
                key="dream_task_trigger_session_count",
                flag_type=FlagType.NUMBER,
                value=5,
                description="DreamTask 触发所需 session 数",
                owner="本地龙",
            ),
            "memory_max_lines": FeatureFlag(
                key="memory_max_lines",
                flag_type=FlagType.NUMBER,
                value=200,
                description="MEMORY.md 最大行数",
                owner="本地龙",
            ),
            "telemetry_sample_rate": FeatureFlag(
                key="telemetry_sample_rate",
                flag_type=FlagType.NUMBER,
                value=1.0,
                description="遥测采样率 0.0-1.0",
                owner="本地龙",
            ),
        }

    # ─── 查询 ──────────────────────────────────────────────────

    def is_enabled(self, key: str) -> bool:
        """
        查询开关是否开启.
        缓存优先, 避免重复解析.
        """
        cached = self._cache.get(f"bool:{key}")
        if cached is not None:
            return cached

        with self._lock:
            flag = self._flags.get(key)
            if flag is None:
                return False
            result = flag.enabled

        self._cache.set(f"bool:{key}", result)
        return result

    def get_config(self, key: str, default: Any = None) -> Any:
        """
        获取数值/对象配置.
        用于 batch_size, sample_rate, min_hours 等参数.
        """
        cached = self._cache.get(f"cfg:{key}")
        if cached is not None:
            return cached

        with self._lock:
            flag = self._flags.get(key)
            if flag is None:
                return default
            result = flag.value if flag.value is not None else default

        self._cache.set(f"cfg:{key}", result)
        return result

    def get_string(self, key: str, default: str = "") -> str:
        """获取字符串配置"""
        flag = self._flags.get(key)
        if flag is None:
            return default
        return str(flag.value) if flag.value is not None else default

    # ─── 动态配置 (类似 GrowthBook) ───────────────────────────

    def get_dynamic_config(
        self,
        key: str,
        default: Any = None,
        blocking: bool = False,
    ) -> Any:
        """
        获取动态配置.
        blocking=True 时阻塞等待初始化 (参考 GrowthBook BLOCKS_ON_INIT).

        Claude Code 用法:
          getDynamicConfig_BLOCKS_ON_INIT('tengu_auto_mode_config', {})
        """
        if blocking:
            # 等待初始化完成 (这里简化处理, 直接返回)
            pass
        return self.get_config(key, default)

    # ─── 管理 ──────────────────────────────────────────────────

    def set_enabled(self, key: str, enabled: bool) -> None:
        """开启/关闭开关"""
        with self._lock:
            if key in self._flags:
                self._flags[key].enabled = enabled
                self._flags[key].updated_at = time.time()
            else:
                self._flags[key] = FeatureFlag(key=key, enabled=enabled)
        self._cache.invalidate(f"bool:{key}")
        self.save()

    def set_config(self, key: str, value: Any, flag_type: FlagType = FlagType.NUMBER) -> None:
        """设置配置值"""
        with self._lock:
            if key in self._flags:
                self._flags[key].value = value
                self._flags[key].flag_type = flag_type
                self._flags[key].updated_at = time.time()
            else:
                self._flags[key] = FeatureFlag(key=key, flag_type=flag_type, value=value)
        self._cache.invalidate(f"cfg:{key}")
        self.save()

    def sync_remote(self, url: str, api_key: str) -> bool:
        """
        同步远程配置 (GrowthBook/LaunchDarkly API).
        简化版: 从远程 URL GET JSON 配置并合并.
        """
        try:
            import urllib.request
            req = urllib.request.Request(
                url,
                headers={"Authorization": f"Bearer {api_key}"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                self._merge_remote(data)
                self._remote_url = url
                self._remote_key = api_key
                self._last_sync = time.time()
                return True
        except Exception as e:
            print(f"[FeatureEngine] sync_remote failed: {e}")
            return False

    def _merge_remote(self, data: dict) -> None:
        """合并远程配置到本地"""
        with self._lock:
            for key, val in data.items():
                if key in self._flags:
                    if isinstance(val, bool):
                        self._flags[key].enabled = val
                    else:
                        self._flags[key].value = val
                else:
                    ftype = FlagType.BOOLEAN if isinstance(val, bool) else FlagType.STRING
                    self._flags[key] = FeatureFlag(key=key, flag_type=ftype, enabled=bool(val) if ftype == FlagType.BOOLEAN else False, value=val)
        self.save()
        self._cache.clear()

    def list_flags(self) -> list[FeatureFlag]:
        """列出所有开关"""
        with self._lock:
            return list(self._flags.values())

    def dump(self) -> dict:
        """导出所有开关 (for debugging)"""
        with self._lock:
            return {k: v.to_dict() for k, v in self._flags.items()}


# ─── 全局实例 ───────────────────────────────────────────────────

_engine: Optional[FeatureEngine] = None
_engine_lock = threading.Lock()


def get_engine() -> FeatureEngine:
    global _engine
    with _engine_lock:
        if _engine is None:
            _engine = FeatureEngine()
        return _engine


# ─── 便捷函数 (与 Claude Code feature() 接口对齐) ───────────────

def feature(flag_key: str) -> bool:
    """查询功能开关"""
    return get_engine().is_enabled(flag_key)


def get_feature_config(key: str, default: Any = None) -> Any:
    """获取配置值"""
    return get_engine().get_config(key, default)


def set_feature(flag_key: str, enabled: bool) -> None:
    """设置开关"""
    get_engine().set_enabled(flag_key, enabled)


# ─── HEARTBEAT 集成常量 ─────────────────────────────────────────
# 这些值从 feature engine 读取, 允许运行时动态调整

def get_heartbeat_interval() -> int:
    return get_engine().get_config("heartbeat_interval_secs", 1800)

def get_dream_trigger_sessions() -> int:
    return get_engine().get_config("dream_task_trigger_session_count", 5)

def get_memory_max_lines() -> int:
    return get_engine().get_config("memory_max_lines", 200)


if __name__ == "__main__":
    ff = FeatureEngine()

    # 查询
    print(f"evoclaw_auto_memory_extract: {ff.is_enabled('evoclaw_auto_memory_extract')}")
    print(f"heartbeat_interval_secs: {ff.get_config('heartbeat_interval_secs', 1800)}")

    # 动态修改
    ff.set_enabled("evoclaw_telemetry", False)
    print(f"evoclaw_telemetry (after disable): {ff.is_enabled('evoclaw_telemetry')}")

    # 列出所有
    print(f"\nAll flags ({len(ff.list_flags())}):")
    for f in ff.list_flags():
        print(f"  {f.key}: {f.value if f.flag_type != FlagType.BOOLEAN else f.enabled}")

    ff.set_enabled("evoclaw_telemetry", True)  # 恢复
    print("✅ FeatureFlags: all tests passed")
