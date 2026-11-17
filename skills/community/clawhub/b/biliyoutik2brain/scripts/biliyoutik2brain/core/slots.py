"""
BiliYouTik2Brain — 并发槽位管理（双通道）

轻活通道（下载/OCR/BLEEP/保存等 I/O 密集）：
  - 非阻塞，槽位满则排队
重活通道（转录 whisper + LLM 修复，CPU 密集）：
  - 阻塞等待（管线已在跑，不排队）
  - 按模型权重动态分配槽位数

使用 fcntl 文件锁防止竞态（Windows 上采用文件存在性锁降级）。
"""

import os
import sys
import time
import json
import json
import uuid as _uuid

# fcntl is Unix-only; Windows fallback uses file-existence locks
_WINDOWS = sys.platform == "win32"
if not _WINDOWS:
    import fcntl
from typing import Optional, Tuple

# ── 跨平台文件锁（上下文管理器） ──
class _ExclusiveLock:
    """排他文件锁上下文管理器。Unix 用 fcntl.flock，Windows 降级为空操作。"""
    def __init__(self, path: str):
        self._path = path
        self._fh = None
    def __enter__(self):
        if not _WINDOWS:
            import fcntl
            self._fh = open(self._path, "w")
            fcntl.flock(self._fh.fileno(), fcntl.LOCK_EX)
        return self
    def __exit__(self, *args):
        if self._fh is not None:
            fcntl.flock(self._fh.fileno(), fcntl.LOCK_UN)
            self._fh.close()
            self._fh = None

# ── 跨平台文件锁 ──
def _acquire_exclusive_lock(lock_path: str) -> None:
    """获取排他锁。Unix 用 fcntl.flock，Windows 用文件存在性模拟。"""
    if not _WINDOWS:
        import fcntl
        with open(lock_path, "w") as lf:
            fcntl.flock(lf.fileno(), fcntl.LOCK_EX)
    # Windows: no-op, counter reads/writes may race but are best-effort

def _release_lock(lock_path: str) -> None:
    """释放排他锁。Windows 下无操作。"""
    if not _WINDOWS:
        import fcntl
        with open(lock_path, "w") as lf:
            fcntl.flock(lf.fileno(), fcntl.LOCK_UN)

# ── 锁目录 ──
_LOCK_DIR = os.path.expanduser("~/.biliyoutik2brain_run")
os.makedirs(_LOCK_DIR, exist_ok=True)

# ── 锁文件路径 ──
_LIGHT_COUNTER = os.path.join(_LOCK_DIR, "counter_light.pkl")
_LIGHT_LOCK = os.path.join(_LOCK_DIR, "lock_light")
_HEAVY_COUNTER = os.path.join(_LOCK_DIR, "counter_heavy.pkl")
_HEAVY_LOCK = os.path.join(_LOCK_DIR, "lock_heavy")
_QUEUE_FILE = os.path.join(_LOCK_DIR, "queue.json")

_MODEL_WEIGHTS = {"tiny": 0.5, "base": 1.0, "small": 2.0, "medium": 4.0, "large": 8.0}
_HEAVY_TIMEOUT = 600  # 重活槽位阻塞超时（秒）

# ── 运行时状态（初始化时计算） ──
_HEAVY_SLOTS = {}
_LIGHT_SLOTS = 0


# ═══════════════════════════════════════════════════════════════
# 初始化
# ═══════════════════════════════════════════════════════════════

def _get_free_ram_gb() -> float:
    """获取可用内存（GB），跨平台"""
    if not _WINDOWS:
        try:
            with open("/proc/meminfo") as f:
                free = cached = 0
                for line in f:
                    if line.startswith("MemAvailable:"):
                        return int(line.split()[1]) / 1024 / 1024
                    if line.startswith("MemFree:"):
                        free = int(line.split()[1])
                    if line.startswith("Cached:"):
                        cached = int(line.split()[1])
                return (free + cached) / 1024 / 1024
        except Exception:
            pass
    else:
        # Windows: use psutil if available
        try:
            import psutil
            return psutil.virtual_memory().available / (1024 ** 3)
        except ImportError:
            pass
        # Fallback: use subprocess with explicit args (no shell=True)
        try:
            import subprocess, re
            out = subprocess.check_output(
                ["wmic", "OS", "get", "FreePhysicalMemory", "/Value"],
                timeout=5, stderr=subprocess.DEVNULL
            ).decode("utf-8", errors="replace")
            m = re.search(r"FreePhysicalMemory=(\d+)", out)
            if m:
                return int(m.group(1)) / 1024 / 1024  # KB → GB
        except Exception:
            pass
    return 4.0


def _compute_slots() -> Tuple[int, dict]:
    """启动时一次性计算轻活/重活槽位数"""
    cpu_count = max(1, os.cpu_count() or 2)
    free_ram = _get_free_ram_gb()
    max_by_cpu = max(1, cpu_count // 2)

    heavy = {}
    for model, weight in _MODEL_WEIGHTS.items():
        max_by_ram = max(1, int(free_ram / (2.0 * weight)))
        heavy[model] = min(max_by_cpu, max_by_ram)

    light = max(2, heavy.get("base", 1) * 2)

    print(f"  [并发] 轻活={light}, 重活={heavy} (CPU={cpu_count}, RAM={free_ram:.1f}GB)")
    return light, heavy


def init_concurrency():
    """模块显式初始化（启动时自动调用）"""
    global _LIGHT_SLOTS, _HEAVY_SLOTS
    _LIGHT_SLOTS, _HEAVY_SLOTS = _compute_slots()
    _reset_stale_counters()

def _reset_stale_counters():
    """启动时重置所有计数器（防止被异常终止的进程留下残值）"""
    import os, pickle
    for counter in [_LIGHT_COUNTER, _HEAVY_COUNTER]:
        try:
            with _ExclusiveLock(_LIGHT_LOCK):
                with open(counter, "wb") as cf:
                    json.dump(0, cf)
        except Exception:
            pass


# 模块加载时自动初始化
init_concurrency()


# ═══════════════════════════════════════════════════════════════
# 轻活通道
# ═══════════════════════════════════════════════════════════════

def acquire_light_slot() -> bool:
    """获取轻活槽位（非阻塞）。False=排队"""
    return _acquire_slot(_LIGHT_LOCK, _LIGHT_COUNTER, _LIGHT_SLOTS)

def release_light_slot():
    """释放轻活槽位"""
    _release_slot(_LIGHT_LOCK, _LIGHT_COUNTER, _LIGHT_SLOTS)

def queue_light(url: str) -> str:
    """将URL加入轻活队列（槽位满时）"""
    return _queue_url(url, "等待轻活槽位")

def dequeue_light() -> Optional[str]:
    """从轻活队列取出下一个URL"""
    return _dequeue_next()


# ═══════════════════════════════════════════════════════════════
# 重活通道
# ═══════════════════════════════════════════════════════════════

def acquire_heavy_slot(model: str = "base") -> bool:
    """获取重活槽位（阻塞，等不到超时返回False）"""
    max_conc = _HEAVY_SLOTS.get(model, _HEAVY_SLOTS.get("base", 1))
    start = time.time()
    while time.time() - start < _HEAVY_TIMEOUT:
        if _acquire_slot_inner(_HEAVY_LOCK, _HEAVY_COUNTER, max_conc):
            print(f"  [并发-重] 获得槽位({model})")
            return True
        time.sleep(2)
    print(f"  ⚠️ [并发-重] 超时({_HEAVY_TIMEOUT}s)，无法获取{model}槽位")
    return False

def release_heavy_slot():
    """释放重活槽位"""
    _release_slot(_HEAVY_LOCK, _HEAVY_COUNTER, _HEAVY_SLOTS.get("base", 1))


# ═══════════════════════════════════════════════════════════════
# 底层槽位操作（fcntl 文件锁防 race）
# ═══════════════════════════════════════════════════════════════

def _acquire_slot_inner(lock_path: str, counter_path: str, max_conc: int) -> bool:
    """一次尝试获取槽位，不重试"""
    try:
        with _ExclusiveLock(lock_path):
            count = 0
            if os.path.exists(counter_path):
                try:
                    with open(counter_path, "rb") as cf:
                        count = json.load(cf)
                except Exception:
                    count = 0
            if count < max_conc:
                count += 1
                with open(counter_path, "wb") as cf:
                    json.dump(count, cf)
                return True
    except Exception:
        pass
    return False


def _acquire_slot(lock_path: str, counter_path: str, max_conc: int) -> bool:
    """获取槽位（外部调用入口）"""
    return _acquire_slot_inner(lock_path, counter_path, max_conc)


def _release_slot(lock_path: str, counter_path: str, max_conc: int):
    """释放槽位"""
    try:
        with _ExclusiveLock(lock_path):
            count = 0
            if os.path.exists(counter_path):
                try:
                    with open(counter_path, "rb") as cf:
                        count = json.load(cf)
                except Exception:
                    count = 0
            if count > 0:
                count -= 1
            with open(counter_path, "wb") as cf:
                json.dump(count, cf)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# 排队系统
# ═══════════════════════════════════════════════════════════════

def _queue_url(url: str, reason: str) -> str:
    """将URL加入队列"""
    qid = f"q_{_uuid.uuid4().hex[:8]}"
    queue = []
    if os.path.exists(_QUEUE_FILE):
        try:
            with open(_QUEUE_FILE) as f:
                queue = json.load(f)
        except Exception:
            queue = []
    entry = {
        "id": qid,
        "url": url,
        "reason": reason,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    queue.append(entry)
    try:
        with open(_QUEUE_FILE, "w") as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    print(f"  [排队] {url[:60]}... ({reason})")
    return qid


def _dequeue_next() -> Optional[str]:
    """从队列取出下一个URL"""
    try:
        with open(_QUEUE_FILE) as f:
            queue = json.load(f)
        if not queue:
            return None
        entry = queue.pop(0)
        with open(_QUEUE_FILE, "w") as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
        return entry.get("url")
    except Exception:
        return None
