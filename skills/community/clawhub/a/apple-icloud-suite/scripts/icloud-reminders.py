#!/usr/bin/env python3
"""
iCloud Reminders 访问脚本 (使用 pyicloud)
使用: python icloud-reminders.py [list|add|complete] [参数]

注意: 推荐使用 todoman + vdirsyncer 的 CalDAV 方式访问提醒事项
此脚本提供 Python API 方式的补充访问

环境变量:
  ICLOUD_USERNAME - Apple ID
  ICLOUD_PASSWORD - 应用专用密码
"""

import sys
import os
from datetime import datetime

try:
    from pyicloud import PyiCloudService
except ImportError:
    print("请先安装 pyicloud: pip install pyicloud")
    sys.exit(1)


def get_api():
    """获取 iCloud API 连接"""
    username = os.environ.get('ICLOUD_USERNAME')
    password = os.environ.get('ICLOUD_PASSWORD')
    
    if not username:
        username = input("Apple ID: ")
    if not password:
        password = input("应用专用密码: ")
    
    china_mainland = username.endswith('@icloud.com.cn') or \
                     os.environ.get('ICLOUD_CHINA', '').lower() in ('1', 'true', 'yes')
    
    print(f"正在连接 iCloud... {'(中国大陆)' if china_mainland else ''}")
    api = PyiCloudService(username, password, china_mainland=china_mainland)
    
    if api.requires_2fa:
        print("\n需要双重认证验证")
        code = input("请输入验证码: ")
        result = api.validate_2fa_code(code)
        if not result:
            print("❌ 验证失败!")
            sys.exit(1)
        print("✅ 验证成功!")
    
    return api


def list_reminders(api, show_completed=False):
    """列出提醒事项"""
    print("\n✅ iCloud 提醒事项:\n")
    
    try:
        # 注意: pyicloud 原版可能不支持 reminders
        # 如果不支持，提示使用 CalDAV 方式
        if not hasattr(api, 'reminders'):
            print("❌ 当前版本的 pyicloud 不支持提醒事项 API")
            print("\n💡 推荐使用 CalDAV 方式:")
            print("   1. 配置 vdirsyncer 同步提醒事项")
            print("   2. 使用 todoman 命令行工具管理")
            print("\n   详见 SKILL.md 中的「Part 2: 提醒事项」")
            return
        
        reminders = api.reminders
        
        # 列出提醒列表
        for list_name in reminders.lists:
            print(f"\n📋 {list_name}:")
            
            tasks = reminders.lists[list_name]
            incomplete_count = 0
            
            for task in tasks:
                is_completed = task.get('completed', False)
                
                if is_completed and not show_completed:
                    continue
                
                status = "✅" if is_completed else "⬜"
                title = task.get('title', '未命名')
                due = task.get('dueDate', '')
                
                due_str = ""
                if due:
                    due_str = f" (截止: {due})"
                
                print(f"  {status} {title}{due_str}")
                
                if not is_completed:
                    incomplete_count += 1
            
            if incomplete_count == 0 and not show_completed:
                print("  (没有未完成的任务)")
                
    except AttributeError:
        print("❌ pyicloud 不支持提醒事项")
        print("\n💡 请使用 CalDAV 方式访问提醒事项:")
        print("   - 配置 vdirsyncer + todoman")
        print("   - 或使用 pyicloudreminders 库")
    except Exception as e:
        print(f"❌ 获取提醒事项失败: {e}")


def show_caldav_hint():
    """显示 CalDAV 配置提示"""
    print("""
📋 推荐使用 CalDAV 方式管理提醒事项

CalDAV 方式更稳定可靠，支持完整的任务管理功能。

快速开始:

1. 安装工具:
   pip install vdirsyncer todoman

2. 配置 vdirsyncer (~/.config/vdirsyncer/config):
   
   [pair icloud_reminders]
   a = "icloud_reminders_remote"
   b = "icloud_reminders_local"
   collections = ["from a", "from b"]
   conflict_resolution = "a wins"

   [storage icloud_reminders_remote]
   type = "caldav"
   url = "https://caldav.icloud.com/"
   username = "your@icloud.com"
   password.fetch = ["command", "cat", "~/.config/vdirsyncer/icloud_password"]
   item_types = ["VTODO"]

   [storage icloud_reminders_local]
   type = "filesystem"
   path = "~/.local/share/vdirsyncer/reminders/"
   fileext = ".ics"

3. 配置 todoman (~/.config/todoman/config.py):
   
   path = "~/.local/share/vdirsyncer/reminders/*"
   date_format = "%Y-%m-%d"
   default_list = "Reminders"

4. 同步并使用:
   vdirsyncer discover
   vdirsyncer sync
   todo list
   todo new "新任务"
   todo done 1

详见 SKILL.md 文档获取完整配置。
""")


def show_help():
    """显示帮助信息"""
    print("""
iCloud Reminders 访问脚本

用法:
  python icloud-reminders.py list        列出未完成任务
  python icloud-reminders.py list --all  列出所有任务(含已完成)
  python icloud-reminders.py caldav      显示 CalDAV 配置指南
  python icloud-reminders.py help        显示此帮助

环境变量:
  ICLOUD_USERNAME    Apple ID 邮箱
  ICLOUD_PASSWORD    应用专用密码

⚠️ 重要提示:
  pyicloud 对提醒事项的支持有限。
  强烈推荐使用 CalDAV 方式 (vdirsyncer + todoman):
  
  运行 `python icloud-reminders.py caldav` 查看配置指南
""")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help', 'help'):
        show_help()
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        api = get_api()
        show_all = "--all" in sys.argv
        list_reminders(api, show_completed=show_all)
        
    elif cmd == "caldav":
        show_caldav_hint()
        
    else:
        print(f"❌ 未知命令: {cmd}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
