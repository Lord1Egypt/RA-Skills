#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Beep · 小喇叭 CLI
提供便捷的命令行接口来测试和管理语音播报

命令名：beep（推荐）或 audio-announce（向后兼容）
"""

import sys
from pathlib import Path

# 添加包路径（beep-skills 父目录，使 audio_announcement 包可导入）
_skill_root = Path(__file__).parent.parent
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

from audio_announcement import announce, receive, task, complete, error, AnnouncementHelper, __version__

# 检测命令名（用于显示和兼容性）
PROG_NAME = Path(sys.argv[0]).name if sys.argv else "beep"

def print_usage():
    print(f"Beep · 小喇叭 v{__version__}")
    print(f"Command: {PROG_NAME}")
    print()
    print("Usage:")
    print(f"  {PROG_NAME} <type> <message> [lang]")
    print(f"  {PROG_NAME} test                   # Test all announcement types")
    print(f"  {PROG_NAME} verify-integration      # One-click integration verify (NEW!)")
    print(f"  {PROG_NAME} config [key=value]      # View/set configuration")
    print(f"  {PROG_NAME} config reload           # Hot-reload config file")
    print(f"  {PROG_NAME} stats                   # Show runtime statistics")
    print(f"  {PROG_NAME} enable|disable          # Enable/disable announcements")
    print(f"  {PROG_NAME} check                   # Run environment self-check")
    print(f"  {PROG_NAME} version                 # Show version")
    print()
    print("Types:")
    print("  receive   - Message received")
    print("  task      - Task started")
    print("  complete  - Task completed")
    print("  error     - Error warning")
    print()
    print("Languages:")
    print("  zh (Chinese), en (English), ja (Japanese), ko (Korean), es (Spanish), fr (French), de (German)")
    print()
    print("Examples:")
    print(f"  {PROG_NAME} receive '收到上传指令' zh")
    print(f"  {PROG_NAME} test")
    print(f"  {PROG_NAME} verify-integration")

def main():
    if len(sys.argv) < 2:
        print_usage()
        return 1
    
    cmd = sys.argv[1].lower()
    
    if cmd == "test":
        # 测试所有类型
        print("正在测试所有播报类型...")
        receive("收到测试指令")
        task("正在执行测试任务")
        complete("测试任务已完成")
        error("检测到测试异常")
        print("\n测试完成！")
        return 0
    
    elif cmd == "verify-integration":
        # 🎉 新增：一键集成验证
        from audio_announcement.announce_helper import verify_integration
        success = verify_integration()
        return 0 if success else 1
    
    elif cmd == "config":
        # 查看/设置配置
        helper = AnnouncementHelper()
        if len(sys.argv) == 2:
            print("当前配置:")
            for k, v in helper.config.__dict__.items():
                print(f"  {k}: {v}")
            return 0
        elif sys.argv[2] == "reload":
            # 热重载配置
            helper.reload_config()
            print("配置已热重载")
            return 0
        else:
            # 设置配置 key=value
            updates = {}
            for arg in sys.argv[2:]:
                if "=" in arg:
                    k, v = arg.split("=", 1)
                    # 类型转换
                    if v.lower() in ("true", "false"):
                        v = v.lower() == "true"
                    elif v.replace(".", "", 1).isdigit():
                        v = float(v) if "." in v else int(v)
                    updates[k] = v
            for k, v in updates.items():
                if hasattr(helper.config, k):
                    setattr(helper.config, k, v)
                else:
                    print(f"警告: 未知配置项 '{k}'")
            helper.config.save()
            print("配置已更新:")
            for k, v in updates.items():
                print(f"  {k}: {v}")
            return 0
    
    elif cmd in ("enable", "disable"):
        helper = AnnouncementHelper()
        if cmd == "enable":
            helper.enable()
            print("语音播报已启用")
        else:
            helper.disable()
            print("语音播报已禁用")
        return 0
    
    elif cmd == "check":
        # 运行环境自检
        helper = AnnouncementHelper()
        print("环境自检完成（结果已在上方输出）")
        return 0
    
    elif cmd == "version" or cmd == "--version":
        print(f"Beep · 小喇叭 v{__version__}")
        return 0
    
    elif cmd == "stats":
        helper = AnnouncementHelper()
        stats = helper.get_stats()
        print("使用统计:")
        for k, v in stats.items():
            print(f"  {k}: {v}")
        return 0
    
    elif cmd in ("receive", "task", "complete", "error"):
        # 播报命令
        if len(sys.argv) < 3:
            print(f"错误: {cmd} 类型需要提供消息内容")
            return 1
        message = sys.argv[2]
        lang = sys.argv[3] if len(sys.argv) > 3 else None
        success = announce(cmd, message, lang=lang)
        return 0 if success else 1
    
    else:
        print(f"错误: 未知命令 '{cmd}'")
        print_usage()
        return 1

if __name__ == "__main__":
    sys.exit(main())
