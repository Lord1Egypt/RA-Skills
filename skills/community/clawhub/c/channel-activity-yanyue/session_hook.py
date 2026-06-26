#!/usr/bin/env python3
"""
短期记忆集成 Hook - 每次会话自动调用
在炎月回复前自动获取其他通道的临时记忆
"""
import sys
sys.path.insert(0, '/Users/kunpeng.zhu/.openclaw/workspace/skills/short-term-memory')

from channel_activity import ChannelActivity

def get_session_context(current_channel: str) -> str:
    """
    获取当前会话的完整上下文
    
    Args:
        current_channel: 当前通道（feishu/qq）
    
    Returns:
        格式化的上下文字符串
    """
    ca = ChannelActivity()
    
    # 获取其他通道的活动
    summary = ca.get_context_summary(channel=current_channel)
    
    if not summary:
        return ""
    
    # 返回格式化的上下文
    return f"\n{summary}\n"

# 使用示例
if __name__ == "__main__":
    # 模拟在飞书会话中
    print("=== 飞书会话上下文 ===")
    ctx = get_session_context("feishu")
    print(ctx or "无其他通道活动")
    
    # 模拟在 QQ 会话中
    print("\n=== QQ 会话上下文 ===")
    ctx = get_session_context("qq")
    print(ctx or "无其他通道活动")