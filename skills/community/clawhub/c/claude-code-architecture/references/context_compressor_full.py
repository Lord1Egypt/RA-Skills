#!/usr/bin/env python3
"""
五级上下文压缩完整实现

压缩级别：
1. Prune   — 删除低价值消息（系统提示重复、空消息）
2. Micro   — 精简长消息（截断过长的工具输出）
3. Fold    — 折叠摘要（将连续同类消息替换为摘要）
4. Auto    — AI 自动总结（调用模型对历史做摘要）
5. Hard    — 强制保留关键信息（只保留系统提示 + 最新 N 轮）

使用场景：当上下文接近 token 限制时，逐级压缩以腾出空间。
"""

from typing import Optional, Callable
from dataclasses import dataclass, field
import re


@dataclass
class CompressionStats:
    original_tokens: int
    compressed_tokens: int
    level_applied: int
    messages_removed: int = 0
    messages_trimmed: int = 0


class ContextCompressor:
    """五级上下文压缩器"""

    LEVELS: dict[int, str] = {
        1: "prune",
        2: "micro",
        3: "fold",
        4: "auto",
        5: "hard",
    }

    def __init__(self, token_counter: Optional[Callable[[str], int]] = None):
        self._token_counter = token_counter or (lambda s: len(s) // 4)
        self._stats: list[CompressionStats] = []

    # ── 入口 ──────────────────────────────────────

    def compress(self, messages: list[dict], max_tokens: int, level: int = 1) -> list[dict]:
        """按指定级别压缩消息列表"""
        current_tokens = self._count_messages(messages)

        if level >= 1:
            messages = self._prune(messages)
        if level >= 2 and self._count_messages(messages) > max_tokens:
            messages = self._micro(messages, max_tokens)
        if level >= 3 and self._count_messages(messages) > max_tokens:
            messages = self._fold(messages)
        if level >= 4 and self._count_messages(messages) > max_tokens:
            messages = self._auto_summarize(messages, max_tokens)
        if level >= 5 and self._count_messages(messages) > max_tokens:
            messages = self._hard_retain(messages, max_tokens)

        new_tokens = self._count_messages(messages)
        self._stats.append(CompressionStats(
            original_tokens=current_tokens,
            compressed_tokens=new_tokens,
            level_applied=level,
        ))

        return messages

    # ── Level 1: Prune ────────────────────────────

    def _prune(self, messages: list[dict]) -> list[dict]:
        """删除低价值消息"""
        kept = []
        for msg in messages:
            content = msg.get("content", "")
            # 跳过空消息
            if not content.strip():
                continue
            # 跳过重复的系统提示
            if msg.get("role") == "system" and kept and kept[-1].get("role") == "system":
                continue
            kept.append(msg)
        return kept

    # ── Level 2: Micro ────────────────────────────

    def _micro(self, messages: list[dict], max_tokens: int) -> list[dict]:
        """精简长消息（工具输出截断）"""
        result = []
        for msg in messages:
            content = msg.get("content", "")
            if msg.get("role") == "tool" and len(content) > 2000:
                msg = {**msg, "content": content[:1000] + f"\n... [截断，原 {len(content)} 字符]"}
            result.append(msg)
        return result

    # ── Level 3: Fold ─────────────────────────────

    def _fold(self, messages: list[dict]) -> list[dict]:
        """折叠连续同类消息"""
        result = []
        i = 0
        while i < len(messages):
            msg = messages[i]
            role = msg.get("role", "")
            if role in ("tool",):
                # 连续工具输出折叠为一个摘要
                group = [msg]
                j = i + 1
                while j < len(messages) and messages[j].get("role") == role:
                    group.append(messages[j])
                    j += 1
                if len(group) > 1:
                    result.append({
                        "role": "system",
                        "content": f"[{len(group)} 条工具输出已折叠]",
                    })
                else:
                    result.append(msg)
                i = j
            else:
                result.append(msg)
                i += 1
        return result

    # ── Level 4: Auto ─────────────────────────────

    def _auto_summarize(self, messages: list[dict], max_tokens: int) -> list[dict]:
        """AI 自动总结 — 保留 system prompt + 最新对话 + 历史摘要"""
        system_msgs = [m for m in messages if m.get("role") == "system"]
        other_msgs = [m for m in messages if m.get("role") != "system"]

        if len(other_msgs) <= 4:
            return messages

        # 取后 4 轮 + 前面的做摘要
        recent = other_msgs[-4:]
        older = other_msgs[:-4]

        summary = self._generate_summary(older)
        return system_msgs + [{
            "role": "assistant",
            "content": f"[历史摘要] {summary}",
        }] + recent

    def _generate_summary(self, messages: list[dict]) -> str:
        """生成历史摘要（模板方法，实际应调用模型）"""
        topics = set()
        for msg in messages:
            content = msg.get("content", "")
            # 简单提取关键词作为占位实现
            words = re.findall(r'[\u4e00-\u9fff]{2,}', content)
            topics.update(words[:3])
        return f"之前讨论了: {', '.join(list(topics)[:5]) or '通用话题'}"

    # ── Level 5: Hard ─────────────────────────────

    def _hard_retain(self, messages: list[dict], max_tokens: int) -> list[dict]:
        """强制保留：系统提示 + 最新 N 轮"""
        system_msgs = [m for m in messages if m.get("role") == "system"]
        other_msgs = [m for m in messages if m.get("role") != "system"]

        result = list(system_msgs)
        current = self._count_messages(result)

        # 从后往前取，直到接近限制
        for msg in reversed(other_msgs):
            tokens = self._count_tokens(msg.get("content", ""))
            if current + tokens > max_tokens * 0.9:
                break
            result.insert(len(system_msgs), msg)
            current += tokens

        return result

    # ── 工具方法 ──────────────────────────────────

    def _count_messages(self, messages: list[dict]) -> int:
        return sum(self._count_tokens(m.get("content", "")) for m in messages)

    def _count_tokens(self, text: str) -> int:
        return self._token_counter(text)

    @property
    def stats(self) -> list[CompressionStats]:
        return list(self._stats)

    def auto_level(self, messages: list[dict], max_tokens: int) -> int:
        """根据当前使用率自动推荐压缩级别"""
        current = self._count_messages(messages)
        ratio = current / max_tokens if max_tokens else 0

        if ratio < 0.7:
            return 0
        elif ratio < 0.8:
            return 1
        elif ratio < 0.9:
            return 2
        elif ratio < 0.95:
            return 3
        elif ratio < 1.0:
            return 4
        else:
            return 5


# ── 使用示例 ──────────────────────────────────────

if __name__ == "__main__":
    compressor = ContextCompressor()

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
        {"role": "tool", "content": "x" * 3000},
        {"role": "tool", "content": "y" * 2500},
        {"role": "user", "content": "Do something"},
    ]

    level = compressor.auto_level(messages, max_tokens=2000)
    print(f"Auto level: {level}")

    compressed = compressor.compress(messages, max_tokens=2000, level=level)
    print(f"Messages: {len(messages)} → {len(compressed)}")
    for s in compressor.stats:
        print(f"  L{s.level_applied}: {s.original_tokens} → {s.compressed_tokens} tokens")
