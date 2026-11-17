#!/usr/bin/env python3
"""
ClawAPI Manager - 智能入口
自动检测环境并选择合适的界面
"""

import sys
import os

def is_interactive_terminal():
    """检测是否在交互式终端"""
    return sys.stdin.isatty() and sys.stdout.isatty()

def has_full_tty():
    """检测是否支持完整 TTY（Textual 需要）"""
    try:
        import termios
        termios.tcgetattr(sys.stdin)
        return True
    except:
        return False

def main():
    # 检测环境
    if len(sys.argv) > 1:
        # 有命令行参数：使用 CLI 模式
        print("Using CLI mode...")
        from clawapi import main as cli_main
        cli_main()
    
    elif has_full_tty():
        # 完整 TTY：使用 Textual TUI
        print("Starting Textual TUI...")
        import time
        time.sleep(0.5)
        from clawapi_tui import ClawAPITUI
        app = ClawAPITUI()
        app.run()
    
    elif is_interactive_terminal():
        # 受限终端：使用 Rich 菜单
        print("Starting Rich TUI...")
        import time
        time.sleep(0.5)
        from clawapi_rich import ClawAPIRichTUI
        tui = ClawAPIRichTUI()
        tui.run()
    
    else:
        # 非交互环境（QQ/飞书）：对话式接口
        # 这个模式下，应该由 AI 助手调用，而不是用户直接运行
        # 返回一个提示，告诉 AI 如何使用
        print("""
ClawAPI Manager - Conversational Interface

This tool is designed to be called by AI assistants in chat environments (QQ/Feishu).

For AI assistants:
  Use the Python API directly:
  
  from lib.config_manager import ClawAPIConfigManager
  manager = ClawAPIConfigManager()
  
  # List providers
  providers = manager.list_providers()
  
  # List channels
  channels = manager.list_channels()
  
  # Add provider
  manager.add_provider(name, url, key)
  
  # Set primary model
  manager.set_primary_model(model_id)

For interactive UI, run from SSH terminal:
  python3 clawapi-tui.py
""")

if __name__ == "__main__":
    main()
