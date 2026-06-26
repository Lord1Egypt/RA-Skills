"""
compression.py — 5种记忆压缩策略

策略说明：
1. summarize  - 将长记忆压缩成摘要，保留核心意思
2. extract   - 从记忆中提取关键事实/实体
3. delete    - 删除低价值记忆（importance < 0.3）
4. promote   - 将短记忆升级为长期记忆（高重要度+高访问）
5. archive   - 将超时记忆归档到archive层

用法：
    from hawk.compression import MemoryCompressor
    mc = MemoryCompressor()
    mc.compress_all("summarize")
"""

import os
import time
import json
from typing import TypedDict

try:
    from .memory import MemoryManager, MemoryItem
    from .extractor import extract_memories
    from .config import (
        IMPORTANCE_THRESHOLD_LOW, SUMMARY_MAX_CHARS, WORKING_TTL_DAYS,
        SHORT_TTL_DAYS, LONG_TTL_DAYS, COMPRESS_RATIO_THRESHOLD,
    )
except ImportError:
    from memory import MemoryManager, MemoryItem
    from extractor import extract_memories
    # Fallback defaults (must match hawk/config.py)
    IMPORTANCE_THRESHOLD_LOW = 0.3
    SUMMARY_MAX_CHARS = 200
    WORKING_TTL_DAYS = 1
    SHORT_TTL_DAYS = 7
    LONG_TTL_DAYS = 90
    COMPRESS_RATIO_THRESHOLD = 0.5


class CompressionResult(TypedDict):
    action: str
    processed: int
    affected: list[str]
    details: dict


class MemoryCompressor:
    """
    5种记忆压缩策略
    配合 MemoryManager 使用，对记忆进行压缩/提升/删除/归档
    """

    # Thresholds (imported from hawk/config.py with docstrings)
    # PROMOTE_IMPORTANCE_THRESHOLD: importance >= this → promote to long
    # DELETE_IMPORTANCE_THRESHOLD: importance < this AND old → delete
    # ARCHIVE_SHORT_DAYS: short-layer memories older than this → archive
    # ARCHIVE_LONG_DAYS: long-layer memories older than this → archive
    # ARCHIVE_WORKING_HOURS: working-layer memories older than this → demote
    PROMOTE_IMPORTANCE_THRESHOLD = 0.7   # tune via HAWK_IMPORTANCE_HIGH
    PROMOTE_ACCESS_COUNT_THRESHOLD = 5     # promote after 5+ accesses
    DELETE_IMPORTANCE_THRESHOLD = IMPORTANCE_THRESHOLD_LOW  # from config.py
    DELETE_MAX_AGE_DAYS = 7               # days before eligible for deletion
    ARCHIVE_SHORT_DAYS = SHORT_TTL_DAYS * 4    # ~4× short TTL
    ARCHIVE_LONG_DAYS = LONG_TTL_DAYS           # match long TTL
    ARCHIVE_WORKING_HOURS = WORKING_TTL_DAYS * 24  # convert days to hours

    # 摘要长度限制 (from config.py)
    SUMMARY_MAX_CHARS = SUMMARY_MAX_CHARS

    def __init__(self, db_path: str = "~/.hawk/memories.json"):
        self.db_path = os.path.expanduser(db_path)
        # 尝试复用已有 MemoryManager 实例
        try:
            self.mm = MemoryManager(db_path=self.db_path)
        except Exception:
            self.mm = None

    # ───────────────────────────────────────────────
    # 策略1: summarize
    # ───────────────────────────────────────────────
    def summarize(self, memory_id: str, api_key: str = "", model: str = "gpt-4o-mini") -> dict:
        """
        将长记忆内容压缩成简洁摘要
        - 原文超过 500 字符才处理
        - 摘要保留核心信息，不超过 200 字符
        """
        if not self.mm or memory_id not in self.mm.memories:
            return {"ok": False, "reason": "memory not found"}

        m = self.mm.memories[memory_id]

        if len(m.text) <= 500:
            return {"ok": False, "reason": "memory too short to summarize", "id": memory_id}

        prompt = f"""将以下记忆压缩成简洁摘要，不超过200字，保留核心信息：

原文：
{m.text}

摘要："""

        try:
            results = extract_memories(
                conversation_text=f"[用户]: {prompt}",
                api_key=api_key or os.environ.get("OPENAI_API_KEY", ""),
                model=model,
                provider="openai"
            )
            if results and len(results) > 0:
                summary_text = results[0].get("abstract") or results[0].get("text", "")[:200]
                original_text = m.text
                m.text = summary_text
                m.importance = max(m.importance, 0.5)  # 摘要略微提升重要性
                self.mm._save()
                return {
                    "ok": True,
                    "action": "summarize",
                    "id": memory_id,
                    "original_chars": len(original_text),
                    "summary_chars": len(summary_text),
                }
        except Exception as e:
            return {"ok": False, "reason": f"summarize failed: {e}"}

        return {"ok": False, "reason": "no summary generated"}

    # ───────────────────────────────────────────────
    # 策略2: extract
    # ───────────────────────────────────────────────
    def extract(self, memory_id: str, api_key: str = "", model: str = "gpt-4o-mini") -> dict:
        """
        从记忆中提取关键实体和事实
        - 生成结构化的记忆条目
        - 保留原文同时创建提炼版本
        """
        if not self.mm or memory_id not in self.mm.memories:
            return {"ok": False, "reason": "memory not found"}

        m = self.mm.memories[memory_id]

        prompt = f"""从以下记忆内容中提取关键实体和事实，生成结构化记忆：

原文：
{m.text}

提取格式（JSON）：
{{
  "entities": ["实体1", "实体2"],
  "facts": ["事实1", "事实2"],
  "decisions": ["决定1"],
  "preferences": ["偏好1"]
}}"""

        try:
            results = extract_memories(
                conversation_text=f"[用户]: {prompt}",
                api_key=api_key or os.environ.get("OPENAI_API_KEY", ""),
                model=model,
                provider="openai"
            )
            if results:
                # 用提取的信息更新记忆
                extracted = results[0]
                new_text = f"[提取] {extracted.get('abstract', m.text[:100])}"
                new_text += f"\n原文: {m.text[:300]}"
                m.text = new_text
                m.importance = max(m.importance, 0.6)
                self.mm._save()
                return {
                    "ok": True,
                    "action": "extract",
                    "id": memory_id,
                    "extracted": extracted,
                }
        except Exception as e:
            return {"ok": False, "reason": f"extract failed: {e}"}

        return {"ok": False, "reason": "no extraction generated"}

    # ───────────────────────────────────────────────
    # 策略3: delete
    # ───────────────────────────────────────────────
    def delete(self, memory_id: str) -> dict:
        """
        删除低价值记忆
        - importance < 0.3 且 超过 DELETE_MAX_AGE_DAYS 无访问
        """
        if not self.mm or memory_id not in self.mm.memories:
            return {"ok": False, "reason": "memory not found"}

        m = self.mm.memories[memory_id]
        days_old = (time.time() - m.last_accessed) / 86400

        if m.importance >= self.DELETE_IMPORTANCE_THRESHOLD:
            return {"ok": False, "reason": "importance above threshold", "id": memory_id}

        if days_old < self.DELETE_MAX_AGE_DAYS:
            return {"ok": False, "reason": "not old enough to delete", "id": memory_id}

        deleted_text = m.text[:50]
        del self.mm.memories[memory_id]
        self.mm._save()
        return {
            "ok": True,
            "action": "delete",
            "id": memory_id,
            "deleted_preview": deleted_text,
            "importance": m.importance,
            "days_old": round(days_old, 1),
        }

    # ───────────────────────────────────────────────
    # 策略4: promote
    # ───────────────────────────────────────────────
    def promote(self, memory_id: str) -> dict:
        """
        将记忆从 short 层升级到 long 层
        - importance >= 0.7
        - access_count >= 5
        """
        if not self.mm or memory_id not in self.mm.memories:
            return {"ok": False, "reason": "memory not found"}

        m = self.mm.memories[memory_id]

        if m.layer not in ("working", "short"):
            return {"ok": False, "reason": f"memory in {m.layer}, not eligible", "id": memory_id}

        if m.importance < self.PROMOTE_IMPORTANCE_THRESHOLD:
            return {
                "ok": False,
                "reason": f"importance {m.importance} below {self.PROMOTE_IMPORTANCE_THRESHOLD}",
                "id": memory_id,
            }

        if m.access_count < self.PROMOTE_ACCESS_COUNT_THRESHOLD:
            return {
                "ok": False,
                "reason": f"access_count {m.access_count} below {self.PROMOTE_ACCESS_COUNT_THRESHOLD}",
                "id": memory_id,
            }

        old_layer = m.layer
        m.layer = "long"
        m.importance = min(1.0, m.importance * 1.1)  # 轻微提升
        self.mm._save()
        return {
            "ok": True,
            "action": "promote",
            "id": memory_id,
            "from_layer": old_layer,
            "to_layer": "long",
            "importance": m.importance,
            "access_count": m.access_count,
        }

    # ───────────────────────────────────────────────
    # 策略5: archive
    # ───────────────────────────────────────────────
    def archive(self, memory_id: str) -> dict:
        """
        将超时记忆归档到 archive 层
        - working > 24小时
        - short > 30天
        - long > 90天
        """
        if not self.mm or memory_id not in self.mm.memories:
            return {"ok": False, "reason": "memory not found"}

        m = self.mm.memories[memory_id]

        if m.layer == "archive":
            return {"ok": False, "reason": "already archived", "id": memory_id}

        now = time.time()
        should_archive = False
        days_idle = (now - m.last_accessed) / 86400

        if m.layer == "working" and days_idle * 24 > self.ARCHIVE_WORKING_HOURS:
            should_archive = True
        elif m.layer == "short" and days_idle > self.ARCHIVE_SHORT_DAYS:
            should_archive = True
        elif m.layer == "long" and days_idle > self.ARCHIVE_LONG_DAYS:
            should_archive = True

        if not should_archive:
            return {"ok": False, "reason": f"memory in {m.layer}, not timed out yet", "id": memory_id}

        old_layer = m.layer
        m.layer = "archive"
        # 归档后降低重要性，避免挤占活跃记忆空间
        m.importance = max(0.2, m.importance * 0.7)
        self.mm._save()
        return {
            "ok": True,
            "action": "archive",
            "id": memory_id,
            "from_layer": old_layer,
            "to_layer": "archive",
            "days_idle": round(days_idle, 1),
        }

    # ───────────────────────────────────────────────
    # 批量执行
    # ───────────────────────────────────────────────
    def compress_all(self, strategy: str, dry_run: bool = False) -> CompressionResult:
        """
        对所有记忆应用指定压缩策略

        Args:
            strategy: "summarize" | "extract" | "delete" | "promote" | "archive"
            dry_run: True 则只报告不实际执行
        """
        if not self.mm:
            return {"action": strategy, "processed": 0, "affected": [], "details": {"error": "MemoryManager not initialized"}}

        strategies_map = {
            "summarize": self.summarize,
            "extract": self.extract,
            "delete": self.delete,
            "promote": self.promote,
            "archive": self.archive,
        }

        if strategy not in strategies_map:
            return {"action": strategy, "processed": 0, "affected": [], "details": {"error": f"unknown strategy: {strategy}"}}

        fn = strategies_map[strategy]
        affected = []
        details = {"summaries": [], "errors": []}

        for mem_id, m in list(self.mm.memories.items()):
            # 对于 summarize/extract，跳过太短的
            if strategy in ("summarize", "extract") and len(m.text) <= 500:
                continue

            if dry_run:
                # 预检
                result = fn(mem_id)
                result["dry_run"] = True
            else:
                result = fn(mem_id)

            if result.get("ok", False):
                affected.append(mem_id)
                if "summaries" in details:
                    details["summaries"].append(result)

        return {
            "action": strategy,
            "processed": len(affected),
            "affected": affected,
            "details": details,
        }

    # ───────────────────────────────────────────────
    # 诊断报告
    # ───────────────────────────────────────────────
    def audit(self) -> dict:
        """
        生成记忆库健康报告
        列出各类问题记忆
        """
        if not self.mm:
            return {"error": "MemoryManager not initialized"}

        report = {
            "total": len(self.mm.memories),
            "by_layer": self.mm.count(),
            "candidates": {
                "to_summarize": [],   # 超过500字符
                "to_delete": [],      # 低价值+过期
                "to_promote": [],     # 满足升级条件
                "to_archive": [],     # 超时待归档
            },
            "avg_importance": 0,
        }

        total_imp = 0
        now = time.time()

        for mem_id, m in self.mm.memories.items():
            total_imp += m.importance
            days_idle = (now - m.last_accessed) / 86400

            if len(m.text) > 500:
                report["candidates"]["to_summarize"].append(mem_id)

            if m.importance < self.DELETE_IMPORTANCE_THRESHOLD and days_idle > self.DELETE_MAX_AGE_DAYS:
                report["candidates"]["to_delete"].append(mem_id)

            if m.layer in ("working", "short") and m.importance >= self.PROMOTE_IMPORTANCE_THRESHOLD and m.access_count >= self.PROMOTE_ACCESS_COUNT_THRESHOLD:
                report["candidates"]["to_promote"].append(mem_id)

            if m.layer != "archive":
                if m.layer == "working" and days_idle * 24 > self.ARCHIVE_WORKING_HOURS:
                    report["candidates"]["to_archive"].append(mem_id)
                elif m.layer == "short" and days_idle > self.ARCHIVE_SHORT_DAYS:
                    report["candidates"]["to_archive"].append(mem_id)
                elif m.layer == "long" and days_idle > self.ARCHIVE_LONG_DAYS:
                    report["candidates"]["to_archive"].append(mem_id)

        report["avg_importance"] = round(total_imp / max(1, len(self.mm.memories)), 3)
        return report
