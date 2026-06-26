# Prompt Builder — System Prompt Priority Chain
# 参考: claude-code/src/core/prompt.ts buildEffectiveSystemPrompt()
#
# 优先级 (从高到低):
#   1. overrideSystemPrompt     → 完全替换, 最高优先
#   2. customSystemPrompt      → 用户自定义 prompt
#   3. agentSystemPrompt       → Agent 定义自带的 prompt
#   4. defaultSystemPrompt     → 默认 system prompt
#   + appendSystemPrompt       → 始终追加在末尾 (不受优先级影响)
#
# Channel Injection:
#   微信 → 注入简洁风格 + 中文友好 prompt 片段
#   飞书 → 注入正式风格 prompt 片段

from __future__ import annotations
import os
import hashlib
from pathlib import Path
from typing import Optional

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/openclaw/.openclaw/workspace"))
PROMPTS_DIR = WORKSPACE / "evoclaw" / "prompts"
PROMPTS_DIR.mkdir(parents=True, exist_ok=True)


# ─── Channel 风格片段 ────────────────────────────────────────────

CHANNEL_STYLES = {
    "openclaw-weixin": {
        "name": "微信",
        "inject": (
            "## 微信风格\n"
            "- 回复简洁, 一句话能说完别用三段\n"
            "- 允许 emoji 调节气氛\n"
            "- 避免营销腔, 像朋友聊天\n"
            "- 长内容用换行分隔, 不要堆一整段\n"
        ),
    },
    "feishu": {
        "name": "飞书",
        "inject": (
            "## 飞书风格\n"
            "- 正式但不死板\n"
            "- 结论先行, 然后分点说明\n"
            "- 可以用 Markdown 结构化\n"
        ),
    },
    "default": {
        "name": "默认",
        "inject": (
            "## 通用风格\n"
            "- 直球, 不绕弯\n"
            "- 有话就说, 不废话\n"
        ),
    },
}


def get_channel_style(channel: str) -> dict:
    return CHANNEL_STYLES.get(channel, CHANNEL_STYLES["default"])


# ─── Prompt 优先级链 ──────────────────────────────────────────────

class PromptSource:
    """单个 prompt 源头"""

    def __init__(
        self,
        name: str,
        content: str,
        priority: int = 50,
        volatile: bool = False,   # volatile=True 时禁用缓存
        append: bool = False,      # True = 追加模式 (无视优先级, 始终在末尾)
    ):
        self.name = name
        self.content = content
        self.priority = priority
        self.volatile = volatile
        self.append = append

    def is_empty(self) -> bool:
        return not self.content.strip()


class SystemPromptBuilder:
    """
    System Prompt 优先级链组装器.

    参考 claude-code buildEffectiveSystemPrompt():
      override > custom > agent > default
      + append 始终追加在末尾
    """

    CACHE: dict[str, str] = {}
    CACHE_BREAK_KEY = "__cache_break__"

    def __init__(self):
        self.sources: list[PromptSource] = []
        self.channel: Optional[str] = None

    def set_channel(self, channel: str) -> "SystemPromptBuilder":
        self.channel = channel
        return self

    def add_source(
        self,
        name: str,
        content: str,
        priority: int = 50,
        volatile: bool = False,
        append: bool = False,
    ) -> "SystemPromptBuilder":
        if content.strip():
            self.sources.append(
                PromptSource(name, content, priority, volatile, append)
            )
        return self

    def add_file(self, name: str, file_path: str | Path,
                 priority: int = 50, volatile: bool = False) -> "SystemPromptBuilder":
        """从文件加载 prompt"""
        path = Path(file_path)
        if path.exists():
            content = path.read_text(encoding="utf-8")
            return self.add_source(name, content, priority, volatile)
        return self

    def build(self) -> str:
        """
        组装最终 system prompt.
        流程:
          1. 找最高优先级的非-append 源 → 主 prompt
          2. 收集所有 append 源 → 追加到末尾
          3. 注入 channel 风格片段
          4. 缓存 (非 volatile 源)
        """
        if not self.sources:
            return ""

        # 分离 append 和主 prompt 源
        main_sources = [s for s in self.sources if not s.append]
        append_sources = [s for s in self.sources if s.append]

        # 按优先级排序主源 (高的在前)
        main_sources.sort(key=lambda s: s.priority, reverse=True)

        # 找主 prompt (最高优先级)
        primary = main_sources[0].content if main_sources else ""

        # 收集 append 片段
        append_parts = [s.content for s in append_sources if not s.is_empty()]

        # Channel 注入
        channel_part = ""
        if self.channel:
            style = get_channel_style(self.channel)
            channel_part = f"\n\n### {style['name']} 风格注入\n{style['inject']}"

        # 组装
        parts = [primary]
        if append_parts:
            parts.append("\n\n" + "\n\n".join(append_parts))
        if channel_part:
            parts.append(channel_part)

        result = "".join(parts).strip()

        # 缓存 (如果有 volatile 源则不用缓存)
        has_volatile = any(s.volatile for s in self.sources)
        if not has_volatile and result:
            cache_key = self._cache_key()
            self.CACHE[cache_key] = result

        return result

    def _cache_key(self) -> str:
        """生成缓存 key"""
        elements = "|".join(
            f"{s.name}:{hashlib.md5(s.content.encode()).hexdigest()[:8]}:{s.priority}"
            for s in self.sources
        )
        return hashlib.md5(elements.encode()).hexdigest()

    @classmethod
    def clear_cache(cls) -> None:
        """清除缓存 (在 /clear 或 /compact 时调用)"""
        cls.CACHE.clear()

    @classmethod
    def invalidate(cls, name: str) -> None:
        """使包含指定 source name 的缓存失效"""
        cls.CACHE.clear()


# ─── 便捷函数 ────────────────────────────────────────────────────

def build_system_prompt(
    channel: Optional[str] = None,
    override: str = "",
    custom: str = "",
    agent: str = "",
    default: str = "",
    append: str = "",
) -> str:
    """
    快速组装 system prompt.

    Priority: override > custom > agent > default
    + append 始终追加
    """
    builder = SystemPromptBuilder().set_channel(channel) if channel else SystemPromptBuilder()

    if override:
        builder.add_source("override", override, priority=100)
    if custom:
        builder.add_source("custom", custom, priority=80)
    if agent:
        builder.add_source("agent", agent, priority=60)
    if default:
        builder.add_source("default", default, priority=40)
    if append:
        builder.add_source("append", append, priority=0, append=True)

    return builder.build()


if __name__ == "__main__":
    # Demo
    result = build_system_prompt(
        channel="openclaw-weixin",
        default="你是一个 AI 助手。",
        agent="你是本地龙, 一个调皮的 AI。",
        append="记住: 简洁是必须的。",
    )
    print(result)
