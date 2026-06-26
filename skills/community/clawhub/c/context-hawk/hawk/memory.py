"""
memory.py — 四层记忆管理器（Working/Short/Long/Archive）

功能：
- Working: 当前会话短期记忆
- Short: 近期重要记忆（带Weibull衰减）
- Long: 长期记忆（高价值）
- Archive: 归档（极少访问）
"""

import os
import time
import json
import hashlib
import threading
from dataclasses import dataclass, asdict
from typing import Optional
from pathlib import Path

# Import tunable constants (see hawk/config.py for documentation)
try:
    from hawk.config import (
        DECAY_RATE, WORKING_TTL_DAYS, SHORT_TTL_DAYS, LONG_TTL_DAYS, ARCHIVE_TTL_DAYS,
        IMPORTANCE_THRESHOLD_LOW, IMPORTANCE_THRESHOLD_HIGH, RECALL_MIN_SCORE,
    )
except ImportError:
    # Fallback if hawk.config not available (standalone use)
    DECAY_RATE = 0.95
    WORKING_TTL_DAYS = 1
    SHORT_TTL_DAYS = 7
    LONG_TTL_DAYS = 90
    ARCHIVE_TTL_DAYS = 180
    IMPORTANCE_THRESHOLD_LOW = 0.3
    IMPORTANCE_THRESHOLD_HIGH = 0.8
    RECALL_MIN_SCORE = 0.6


@dataclass
class MemoryItem:
    id: str
    text: str
    category: str  # fact | preference | decision | entity | other
    importance: float  # 0.0-1.0
    access_count: int
    last_accessed: float
    created_at: float
    layer: str  # working | short | long | archive
    metadata: dict


class MemoryManager:
    """
    四层记忆管理器
    - store(text): 存入对应层
    - recall(query): 检索记忆
    - decay(): 触发衰减，更新层级
    """

    LAYERS = ['working', 'short', 'long', 'archive']
    LAYER_THRESHOLDS = {
        'working': 0,          # always working initially
        'short': 3,            # promote after 3+ accesses
        'long': 10,            # promote after 10+ accesses
        'archive': 100,        # inactive threshold
    }
    DECAY_RATE = DECAY_RATE  # from config.py

    def __init__(self, db_path: str = "~/.hawk/memories.json"):
        self.db_path = os.path.expanduser(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.memories: dict[str, MemoryItem] = {}
        self._lock = threading.RLock()  # protects self.memories during concurrent access
        self._load()

    def _load(self):
        with self._lock:
            self._load_unlocked()

    def _load_unlocked(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path) as f:
                    content = f.read()
                    if not content.strip():
                        return  # 空文件，正常
                    data = json.loads(content)
                    for k, v in data.items():
                        self.memories[k] = MemoryItem(**v)
            except json.JSONDecodeError as e:
                print(f"[MemoryManager] Warning: corrupted db file {self.db_path}, resetting. Error: {e}")
                # 备份损坏文件
                import shutil
                shutil.copy(self.db_path, self.db_path + ".bak")
                self.memories = {}

    def _save(self):
        with self._lock:
            self._save_unlocked()

    def _save_unlocked(self):
        with open(self.db_path, 'w') as f:
            json.dump({k: asdict(v) for k, v in self.memories.items()}, f, ensure_ascii=False)

    def store(self, text: str, category: str = "other", importance: float = 0.5, metadata: dict = None) -> str:
        """存入记忆，自动判断层级（normalize 清理后入库）"""
        from hawk.normalize import normalize
        import hashlib
        text = normalize(text)
        with self._lock:
            id = hashlib.sha256(f"{text[:100]}{time.time()}".encode()).hexdigest()[:16]
            now = time.time()
            layer = self._compute_layer(importance, 0)
            item = MemoryItem(
                id=id, text=text, category=category,
                importance=importance, access_count=0,
                last_accessed=now, created_at=now,
                layer=layer, metadata=metadata or {}
            )
            self.memories[id] = item
            self._save_unlocked()
            return id

    def recall(self, query: str, top_k: int = 5) -> list[MemoryItem]:
        """简单关键词检索记忆（配合VectorRetriever做语义检索）"""
        query_lower = query.lower()
        scored = []
        for m in self.memories.values():
            if m.layer == 'archive':
                continue
            # 简单重叠词打分
            words = set(query_lower.split())
            content_words = set(m.text.lower().split())
            overlap = len(words & content_words)
            if overlap > 0:
                score = overlap / len(words) * m.importance * (self.DECAY_RATE ** max(0, int(time.time() - m.last_accessed) // 86400))
                scored.append((score, -m.created_at, m))
        scored.sort(reverse=True)
        return [m for _, _, m in scored[:top_k]]

    def access(self, id: str) -> Optional[MemoryItem]:
        """访问一条记忆，更新计数器"""
        with self._lock:
            if id not in self.memories:
                return None
            m = self.memories[id]
            m.access_count += 1
            m.last_accessed = time.time()
            # 检查是否需要升级层级
            new_layer = self._compute_layer(m.importance, m.access_count)
            if self.LAYERS.index(new_layer) > self.LAYERS.index(m.layer):
                m.layer = new_layer
            self._save_unlocked()
            return m

    def _compute_layer(self, importance: float, access_count: int) -> str:
        # IMPORTANCE_THRESHOLD_HIGH: promote to long immediately if above this
        # IMPORTANCE_THRESHOLD_LOW: demote to archive if below this
        if access_count >= self.LAYER_THRESHOLDS['long'] or importance >= IMPORTANCE_THRESHOLD_HIGH:
            return 'long'
        elif access_count >= self.LAYER_THRESHOLDS['short'] or importance >= IMPORTANCE_THRESHOLD_HIGH * 0.75:
            # short: moderate importance OR repeated access
            return 'short'
        elif importance < IMPORTANCE_THRESHOLD_LOW:
            return 'archive'
        return 'working'

    def decay(self):
        """所有记忆衰减，更新层级， archive 超过ARCHIVE_TTL_DAYS天删除"""
        with self._lock:
            now = time.time()
            changed = False
            to_delete = []

            for m in self.memories.values():
                if m.layer == 'archive':
                    # ARCHIVE_TTL_DAYS: delete after this long of no access
                    if now - m.last_accessed > ARCHIVE_TTL_DAYS * 86400:
                        to_delete.append(m.id)
                    continue
                # DECAY_RATE: daily decay multiplier applied per idle day
                days_idle = max(0, int(now - m.last_accessed) // 86400)
                m.importance *= (DECAY_RATE ** days_idle)
                changed = True
                # 降级（通过 _compute_layer 统一判断）
                new_layer = self._compute_layer(m.importance, m.access_count)
                if self.LAYERS.index(new_layer) < self.LAYERS.index(m.layer):
                    m.layer = new_layer

            for id in to_delete:
                del self.memories[id]
                changed = True

            if changed:
                self._save_unlocked()

    def count(self) -> dict:
        return {layer: sum(1 for m in self.memories.values() if m.layer == layer) for layer in self.LAYERS}

    def get_stats(self) -> dict:
        counts = self.count()
        total = sum(counts.values())
        avg_importance = sum(m.importance for m in self.memories.values()) / max(1, total)
        return {**counts, "total": total, "avg_importance": round(avg_importance, 3)}
