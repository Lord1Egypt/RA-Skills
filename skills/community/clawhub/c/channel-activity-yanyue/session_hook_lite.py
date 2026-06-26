#!/usr/bin/env python3
"""
短期记忆集成 Hook - 精简版
解决输入超限问题，智能截断和摘要
"""
import sys
sys.path.insert(0, '/Users/kunpeng.zhu/.openclaw/workspace/skills/short-term-memory')

from channel_activity import ChannelActivity

def get_session_context(current_channel: str, max_chars: int = 2000) -> str:
    """
    获取精简版会话上下文
    
    Args:
        current_channel: 当前通道（feishu/qq）
        max_chars: 最大字符数（默认 2000）
    
    Returns:
        精简的上下文字符串
    """
    ca = ChannelActivity()
    
    # 获取其他通道的活动
    summary = ca.get_context_summary(channel=current_channel)
    
    if not summary:
        return ""
    
    # 截断到最大字符数
    if len(summary) > max_chars:
        summary = summary[:max_chars] + "...[内容截断]"
    
    return f"\n{summary}\n"

def get_memory_summary(memory_path: str = "/Users/kunpeng.zhu/.openclaw/workspace/MEMORY.md", 
                       max_chars: int = 10000) -> str:
    """
    获取长期记忆摘要（精简版）
    
    Args:
        memory_path: MEMORY.md 路径
        max_chars: 最大字符数（默认 10000）
    
    Returns:
        精简的长期记忆
    """
    try:
        with open(memory_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 如果内容太长，只取最近的部分
        if len(content) > max_chars:
            # 取最后 max_chars 个字符
            content = "...[早期内容已截断]\n" + content[-max_chars:]
        
        return content
    except:
        return ""

# 使用示例
if __name__ == "__main__":
    # 模拟飞书会话
    print("=== 飞书会话（精简版）===")
    ctx = get_session_context("feishu")
    print(ctx or "无其他通道活动")
    
    # 获取精简版 MEMORY.md
    print("\n=== 长期记忆摘要 ===")
    memory = get_memory_summary()
    print(f"长度：{len(memory)} 字符")
    print(memory[:200] + "..." if len(memory) > 200 else memory)