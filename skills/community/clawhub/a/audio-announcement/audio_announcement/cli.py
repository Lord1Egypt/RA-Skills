#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audio-announcement CLI
提供便捷的命令行接口来测试和管理语音播报
"""

import sys
from pathlib import Path

# 添加包路径
package_dir = Path(__file__).parent
if str(package_dir) not in sys.path:
    sys.path.insert(0, str(package_dir))

from audio_announcement import announce, receive, task, complete, error, AnnouncementHelper, __version__

def print_usage():
    print(f"audio-announcement v{__version__}")
    print("用法:")
    print("  audio-announce <type> <message> [lang]")
    print("  或:")
    print("  audio-announce test             # 测试所有类型")
    print("  audio-announce config [key=value]...  # 查看/设置配置")
    print("  audio-announce stats           # 查看统计")
    print("  audio-announce enable|disable  # 启用/禁用")
    print()
    print("类型:")
    print("  receive   - 收到消息")
    print("  task      - 任务开始")
    print("  complete  - 任务完成")
    print("  error     - 错误警告")
    print()
    print("语言:")
    print("  zh (中文), en (英文), ja (日文), ko (韩文), es (西班牙文), fr (法文), de (德文)")
    print()
    print("示例:")
    print("  audio-announce receive '收到上传指令' zh")
    print("  audio-announce test")

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
    
    elif cmd == "config":
        # 查看/设置配置
        helper = AnnouncementHelper()
        if len(sys.argv) == 2:
            print("当前配置:")
            for k, v in helper.config.__dict__.items():
                print(f"  {k}: {v}")
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
