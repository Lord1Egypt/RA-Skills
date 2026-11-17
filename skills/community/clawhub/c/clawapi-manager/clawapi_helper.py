#!/usr/bin/env python3
"""
ClawAPI Helper - 对话式接口辅助函数
供 AI 助手在 QQ/飞书等环境中调用
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from config_manager import ClawAPIConfigManager
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()
manager = ClawAPIConfigManager()

def show_status():
    """显示配置状态"""
    primary = manager.get_primary_model()
    fallbacks = manager.get_fallbacks()
    providers = manager.list_providers()
    
    output = f"""**配置状态**

主模型：{primary}
Providers：{len(providers)} 个
Fallbacks：{len(fallbacks)} 个

Fallback 链：
"""
    for i, fb in enumerate(fallbacks, 1):
        output += f"{i}. {fb}\n"
    
    return output

def show_providers():
    """显示所有 providers"""
    providers = manager.list_providers()
    
    output = "**API Providers**\n\n"
    for p in providers:
        protocol = p.get('protocol', 'openai-compatible')
        output += f"• {p['name']} ({protocol}): {p['model_count']} 个模型, Key: {p['api_key']}\n"
    
    return output

def show_channels():
    """显示所有 channels"""
    channels = manager.list_channels()
    
    output = "**通道配置**\n\n"
    if channels:
        for c in channels:
            status = "✅ 已启用" if c['enabled'] else "❌ 已禁用"
            output += f"• {c['name']} ({c['type']}): {status}\n"
    else:
        output += "(未配置通道)\n"
    
    return output

def show_models(provider_name=None):
    """显示模型列表"""
    models = manager.list_models(provider_name)
    
    output = f"**模型列表**{' - ' + provider_name if provider_name else ''}\n\n"
    for m in models:
        output += f"• {m['full_id']}: {m['name']}\n"
    
    return output

def add_provider_interactive(name, url, key, protocol='openai-compatible'):
    """添加 provider"""
    try:
        manager.add_provider(name, url, key, protocol=protocol)
        return f"✅ Provider '{name}' 已添加 (协议: {protocol})"
    except Exception as e:
        return f"❌ 错误：{e}"

def set_primary_interactive(model_id):
    """设置主模型"""
    try:
        manager.set_primary_model(model_id)
        return f"✅ 主模型已设置为 {model_id}"
    except Exception as e:
        return f"❌ 错误：{e}"

def add_channel_interactive(name, channel_type, token):
    """添加通道"""
    try:
        manager.add_channel(name, channel_type, {'token': token})
        return f"✅ 通道 '{name}' 已添加"
    except Exception as e:
        return f"❌ 错误：{e}"

def toggle_channel_interactive(name):
    """切换通道状态"""
    try:
        new_state = manager.toggle_channel(name)
        state_text = "启用" if new_state else "禁用"
        return f"✅ 通道 '{name}' 已{state_text}"
    except Exception as e:
        return f"❌ 错误：{e}"

# 导出所有函数
__all__ = [
    'show_status',
    'show_providers',
    'show_channels',
    'show_models',
    'add_provider_interactive',
    'set_primary_interactive',
    'add_channel_interactive',
    'toggle_channel_interactive',
    'manager'
]

if __name__ == "__main__":
    # 测试
    print(show_status())
    print("\n" + show_providers())
    print("\n" + show_channels())

def show_protocols():
    """显示所有支持的协议"""
    protocols = manager.list_protocols()
    
    output = "**支持的协议**\n\n"
    for p in protocols:
        output += f"• {p['id']}: {p['name']}\n  {p['description']}\n\n"
    
    return output

def set_protocol_interactive(provider_name, protocol):
    """设置 provider 的协议"""
    try:
        manager.set_provider_protocol(provider_name, protocol)
        return f"✅ Provider '{provider_name}' 协议已设置为 {protocol}"
    except Exception as e:
        return f"❌ 错误：{e}"

# 更新导出列表
__all__ = [
    'show_status',
    'show_providers',
    'show_channels',
    'show_models',
    'show_protocols',
    'add_provider_interactive',
    'set_primary_interactive',
    'add_channel_interactive',
    'toggle_channel_interactive',
    'set_protocol_interactive',
    'manager'
]
