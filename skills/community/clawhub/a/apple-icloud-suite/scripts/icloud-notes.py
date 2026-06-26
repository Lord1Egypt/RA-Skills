#!/usr/bin/env python3
"""
iCloud Notes 访问脚本
使用: python icloud-notes.py [list|search] [参数]

环境变量:
  ICLOUD_USERNAME - Apple ID
  ICLOUD_PASSWORD - 应用专用密码
"""

import sys
import os
import json

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
    
    # 检测是否为中国大陆用户
    china_mainland = username.endswith('@icloud.com.cn') or \
                     os.environ.get('ICLOUD_CHINA', '').lower() in ('1', 'true', 'yes')
    
    print(f"正在连接 iCloud... {'(中国大陆)' if china_mainland else ''}")
    api = PyiCloudService(username, password, china_mainland=china_mainland)
    
    # 处理双重认证
    if api.requires_2fa:
        print("\n需要双重认证验证")
        code = input("请输入从受信任设备收到的验证码: ")
        result = api.validate_2fa_code(code)
        if not result:
            print("❌ 验证失败!")
            sys.exit(1)
        print("✅ 验证成功!")
    
    # 处理两步验证 (旧版)
    if api.requires_2sa:
        print("\n需要两步验证")
        devices = api.trusted_devices
        for i, device in enumerate(devices):
            name = device.get('deviceName', f"SMS to {device.get('phoneNumber')}")
            print(f"  {i}: {name}")
        
        device_index = int(input("选择设备编号: "))
        device = devices[device_index]
        
        if not api.send_verification_code(device):
            print("❌ 发送验证码失败!")
            sys.exit(1)
        
        code = input("输入验证码: ")
        if not api.validate_verification_code(device, code):
            print("❌ 验证失败!")
            sys.exit(1)
        print("✅ 验证成功!")
    
    return api


def list_notes(api):
    """列出所有备忘录 (通过 iCloud Drive)"""
    print("\n📝 正在获取备忘录...\n")
    
    try:
        # 尝试通过 iCloud Drive 访问 Notes
        if 'com~apple~Notes' in api.drive.dir():
            notes_folder = api.drive['com~apple~Notes']
            print("=== iCloud 备忘录 ===\n")
            
            items = list(notes_folder.dir())
            if not items:
                print("没有找到备忘录文件")
                return
            
            for i, item in enumerate(items, 1):
                print(f"  {i}. 📄 {item}")
            
            print(f"\n共 {len(items)} 个项目")
        else:
            print("❌ 无法访问 Notes 文件夹")
            print("\n可用的 iCloud Drive 文件夹:")
            for folder in api.drive.dir():
                print(f"  📁 {folder}")
                
    except Exception as e:
        print(f"❌ 访问备忘录时出错: {e}")
        print("\n💡 提示:")
        print("  - Apple Notes 的 API 访问能力有限")
        print("  - 建议使用 iCloud.com 网页版查看完整备忘录")
        print("  - 或者考虑导出备忘录到其他格式")


def show_drive_structure(api):
    """显示 iCloud Drive 结构"""
    print("\n📁 iCloud Drive 结构:\n")
    
    try:
        for item in api.drive.dir():
            print(f"  📁 {item}")
            try:
                folder = api.drive[item]
                sub_items = list(folder.dir())[:5]  # 只显示前5个
                for sub in sub_items:
                    print(f"      └─ {sub}")
                if len(list(folder.dir())) > 5:
                    print(f"      └─ ... (更多)")
            except:
                pass
    except Exception as e:
        print(f"❌ 错误: {e}")


def show_help():
    """显示帮助信息"""
    print("""
iCloud Notes 访问脚本

用法:
  python icloud-notes.py list       列出备忘录
  python icloud-notes.py drive      显示 iCloud Drive 结构
  python icloud-notes.py help       显示此帮助

环境变量:
  ICLOUD_USERNAME    Apple ID 邮箱
  ICLOUD_PASSWORD    应用专用密码 (在 appleid.apple.com 生成)
  ICLOUD_CHINA       设为 1 表示中国大陆用户

示例:
  export ICLOUD_USERNAME="your@icloud.com"
  export ICLOUD_PASSWORD="xxxx-xxxx-xxxx-xxxx"
  python icloud-notes.py list

注意:
  - 必须使用应用专用密码，不要使用 Apple ID 主密码
  - Apple Notes API 功能有限，部分内容可能无法访问
  - 建议配合 iCloud.com 网页版使用
""")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help', 'help'):
        show_help()
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        api = get_api()
        list_notes(api)
    elif cmd == "drive":
        api = get_api()
        show_drive_structure(api)
    else:
        print(f"❌ 未知命令: {cmd}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
