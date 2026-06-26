## 🔧 完整 Python 脚本

### icloud_tool.py

```python
#!/usr/bin/env python3
"""
Apple iCloud 命令行工具
用法: python icloud_tool.py [photos|drive|devices] [子命令]
"""

import sys
import os

os.environ['icloud_china'] = '1'

from pyicloud import PyiCloudService

def get_api():
    """连接 iCloud"""
    username = os.environ.get('ICLOUD_USERNAME') or input("Apple ID: ")
    password = os.environ.get('ICLOUD_PASSWORD') or input("密码: ")
    
    api = PyiCloudService(username, password, china_mainland=True)
    
    if api.requires_2fa:
        print("\n🔐 需要双重认证")
        print("请查看 iPhone 上的验证码")
        code = input("验证码: ")
        if not api.validate_2fa_code(code):
            print("❌ 验证失败")
            sys.exit(1)
        print("✅ 验证成功!\n")
    
    return api

def cmd_photos(api, args):
    """照片命令"""
    photos = api.photos
    
    if not args or args[0] == 'albums':
        print('📷 相册列表:')
        for name in photos.albums:
            print(f'  📁 {name}')
    
    elif args[0] == 'list':
        limit = int(args[1]) if len(args) > 1 else 10
        library = photos.albums['Library']
        print(f'📷 最近 {limit} 张照片:')
        for i, p in enumerate(library.photos):
            if i >= limit: break
            print(f'  {i+1}. {p.filename} | {p.created}')
    
    elif args[0] == 'download':
        index = int(args[1]) - 1 if len(args) > 1 else 0
        library = photos.albums['Library']
        for i, p in enumerate(library.photos):
            if i == index:
                print(f'正在下载: {p.filename}')
                dl = p.download()
                with open(p.filename, 'wb') as f:
                    f.write(dl.raw.read())
                print(f'✅ 已保存: {p.filename}')
                break

def cmd_drive(api, args):
    """iCloud Drive 命令"""
    drive = api.drive
    
    if not args or args[0] == 'list':
        print('💾 iCloud Drive:')
        for item in drive.dir():
            print(f'  📂 {item}')
    
    elif args[0] == 'cd' and len(args) > 1:
        folder = drive[args[1]]
        print(f'📂 {args[1]}:')
        for item in folder.dir():
            print(f'  📄 {item}')

def cmd_devices(api, args):
    """设备命令"""
    print('📱 我的设备:')
    for d in api.devices:
        print(f'  - {d}')

def main():
    if len(sys.argv) < 2:
        print("""
🍎 Apple iCloud 命令行工具

用法: python icloud_tool.py <命令> [参数]

命令:
  photos albums          列出相册
  photos list [N]        列出最近 N 张照片
  photos download N      下载第 N 张照片
  
  drive list             列出 iCloud Drive
  drive cd <文件夹>      进入文件夹
  
  devices                列出设备

环境变量:
  ICLOUD_USERNAME        Apple ID
  ICLOUD_PASSWORD        密码
        """)
        sys.exit(0)
    
    api = get_api()
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    if cmd == 'photos':
        cmd_photos(api, args)
    elif cmd == 'drive':
        cmd_drive(api, args)
    elif cmd == 'devices':
        cmd_devices(api, args)
    else:
        print(f'未知命令: {cmd}')

if __name__ == '__main__':
    main()
```

---

