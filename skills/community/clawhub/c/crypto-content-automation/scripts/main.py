#!/usr/bin/env python3
"""
Crypto Content Automation - Main Entry
热点扫描 + 内容策划 + 发布自动化
"""

import sys
import os
from datetime import datetime

# 添加scripts目录到路径
SCRIPT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts')
sys.path.insert(0, SCRIPT_DIR)

def run_hot_topic_scan():
    """运行热点扫描"""
    print("🔥 开始热点扫描...")
    from hot_topic_scanner import scan_all_topics
    scan_all_topics()
    print("✅ 热点扫描完成")
    return True

def run_content_planning():
    """运行内容策划"""
    print("📝 开始内容策划...")
    from content_planning import generate_planning
    generate_planning()
    print("✅ 内容策划完成")
    return True

def show_help():
    """显示帮助"""
    print("""
╔══════════════════════════════════════════════════════╗
║   Crypto Content Automation - 使用指南               ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  使用方法:                                           ║
║                                                      ║
║  1. 热点扫描:                                        ║
║     python3 main.py scan                             ║
║                                                      ║
║  2. 内容策划:                                        ║
║     python3 main.py plan                             ║
║                                                      ║
║  3. 完整流程 (扫描+策划):                            ║
║     python3 main.py all                              ║
║                                                      ║
║  4. 帮助:                                            ║
║     python3 main.py help                              ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
    """)

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == 'scan':
        run_hot_topic_scan()
    elif command == 'plan':
        run_content_planning()
    elif command == 'all':
        run_hot_topic_scan()
        run_content_planning()
    elif command == 'help':
        show_help()
    else:
        print(f"未知命令: {command}")
        show_help()

if __name__ == '__main__':
    main()
