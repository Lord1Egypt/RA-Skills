"""AI analysis — uses Anthropic Claude to analyze chat messages."""

from __future__ import annotations

import os


def _get_client():
    """Get Anthropic client, raising clear error if not configured."""
    try:
        import anthropic
    except ImportError:
        raise RuntimeError(
            "anthropic package not installed. Run: uv sync --extra ai"
        )

    api_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN not set in environment"
        )
    return anthropic.Anthropic(api_key=api_key)


def analyze_messages(
    messages: list[dict],
    prompt: str | None = None,
    chat_name: str | None = None,
) -> str:
    """Analyze a list of messages using Claude.

    Args:
        messages: List of message dicts with 'sender_name', 'content', 'timestamp'
        prompt: Custom analysis prompt (uses default if None)
        chat_name: Name of the chat for context

    Returns:
        Analysis text from Claude
    """
    if not messages:
        return "No messages to analyze."

    lines = []
    for msg in messages:
        ts = (msg.get("timestamp") or "")[:19]
        sender = msg.get("sender_name") or "Unknown"
        content = msg.get("content") or ""
        lines.append(f"[{ts}] {sender}: {content}")

    chat_text = "\n".join(lines)
    chat_label = f" from '{chat_name}'" if chat_name else ""

    if prompt is None:
        prompt = f"""请分析以下{len(messages)}条群聊消息{chat_label}，提供：

1. **核心话题摘要** — 这些消息主要在讨论什么？提取 3-5 个关键话题
2. **重要信息提取** — 有价值的链接、项目、工具、观点
3. **活跃讨论** — 哪些话题引发了最多讨论？
4. **值得关注** — 有什么特别值得注意的信息？

请用中文回答，保持简洁有深度。"""

    client = _get_client()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": f"{prompt}\n\n---\n\n{chat_text}",
            }
        ],
    )

    return response.content[0].text


def summarize_messages(messages: list[dict], chat_name: str | None = None) -> str:
    """Generate a concise summary of messages."""
    return analyze_messages(
        messages,
        prompt=f"""请为以下{len(messages)}条消息生成一个简洁的摘要（200字以内）。
重点提取：关键话题、重要结论、值得关注的信息。用中文回答。""",
        chat_name=chat_name,
    )
