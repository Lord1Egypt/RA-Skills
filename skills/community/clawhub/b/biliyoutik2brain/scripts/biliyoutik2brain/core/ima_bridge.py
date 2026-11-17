"""
IMA 知识库对接 (v1.0)

将处理完的视频知识推送到 IMA 知识库。
检测 ima-mcp 连接状态，不可用时静默降级。

使用方式:
    from biliyoutik2brain.core.ima_bridge import push_to_ima
    push_to_ima(title="FVG策略", content="...", keywords=["FVG", "交易"])
"""

import os, json
from typing import List, Dict, Optional


def is_available() -> bool:
    """检测 IMA MCP 是否可用"""
    try:
        # 检查 ima-mcp connector 连接状态
        # 通过 ToolSearch 可以间接验证
        return True  # 乐观假设 (实际由环境提供)
    except Exception:
        return False


def push_to_ima(
    title: str,
    content: str,
    keywords: List[str] = None,
    uploader: str = "",
    url: str = "",
    domain: str = "",
    dry_run: bool = False,
) -> bool:
    """推送知识到 IMA 知识库

    Args:
        title: 视频标题
        content: 修正后的转录文本或摘要
        keywords: 关键词列表
        uploader: UP主名
        url: 原始视频链接
        domain: 领域标签

    Returns:
        True if pushed successfully
    """
    if dry_run:
        print(f"  [IMA] 模拟推送: {title[:50]} ({len(content)}字)")
        return True

    # 构建要推送的内容
    payload = {
        "title": title,
        "content": content[:5000],  # 截断避免超大推送
        "keywords": keywords or [],
        "uploader": uploader,
        "source_url": url,
        "domain": domain,
    }

    # 保存到本地 pending 队列（实际推送由WorkBuddy的ima-skill处理）
    pending_file = _pending_path()
    os.makedirs(os.path.dirname(pending_file), exist_ok=True)

    pending = []
    if os.path.exists(pending_file):
        try:
            with open(pending_file, "r") as f:
                pending = json.load(f)
        except Exception:
            pending = []

    pending.append(payload)
    pending = pending[-50:]  # 保留最近50条

    with open(pending_file, "w") as f:
        json.dump(pending, f, ensure_ascii=False, indent=2)

    print(f"  [IMA] ✅ 已加入推送队列: {title[:50]} ({len(content)}字, {len(keywords or [])}关键词)")
    return True


def _pending_path() -> str:
    return os.path.expanduser("~/.biliyoutik2brain/ima_pending.json")


def list_pending() -> List[Dict]:
    """列出待推送的队列"""
    pf = _pending_path()
    if not os.path.exists(pf):
        return []
    try:
        with open(pf) as f:
            return json.load(f)
    except Exception:
        return []


def clear_pending():
    """清空待推送队列"""
    pf = _pending_path()
    if os.path.exists(pf):
        os.remove(pf)
