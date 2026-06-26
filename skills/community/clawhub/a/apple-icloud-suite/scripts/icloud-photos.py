#!/usr/bin/env python3
"""
iCloud Photos 访问脚本
使用: python icloud-photos.py [albums|list|download|info] [参数]

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


def list_albums(api):
    """列出所有相册"""
    print("\n📁 iCloud 相册:\n")
    
    try:
        albums = api.photos.albums
        for name in albums:
            album = albums[name]
            # 尝试获取照片数量
            try:
                count = len(list(album.photos))
                print(f"  📷 {name} ({count} 张)")
            except:
                print(f"  📷 {name}")
    except Exception as e:
        print(f"❌ 获取相册失败: {e}")


def list_photos(api, album_name="All Photos", limit=20):
    """列出照片"""
    print(f"\n📷 {album_name} (前 {limit} 张):\n")
    
    try:
        albums = api.photos.albums
        
        if album_name not in albums:
            print(f"❌ 相册 '{album_name}' 不存在")
            print("\n可用相册:")
            for name in albums:
                print(f"  - {name}")
            return
        
        album = albums[album_name]
        photos = album.photos
        
        for i, photo in enumerate(photos):
            if i >= limit:
                print(f"\n... 还有更多照片")
                break
            
            created = photo.created.strftime("%Y-%m-%d %H:%M") if photo.created else "未知"
            size = f"{photo.size / 1024 / 1024:.1f}MB" if hasattr(photo, 'size') and photo.size else ""
            
            print(f"  {i+1:3}. 📷 {photo.filename:30} | {created} {size}")
            
    except Exception as e:
        print(f"❌ 获取照片列表失败: {e}")


def download_photo(api, index, album_name="All Photos", output_dir="./downloads"):
    """下载单张照片"""
    print(f"\n⬇️ 正在下载第 {index} 张照片...\n")
    
    try:
        albums = api.photos.albums
        album = albums.get(album_name, albums["All Photos"])
        photos = list(album.photos)
        
        if index < 1 or index > len(photos):
            print(f"❌ 照片索引超出范围 (1-{len(photos)})")
            return
        
        photo = photos[index - 1]  # 用户输入从1开始
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 下载照片
        print(f"📷 文件名: {photo.filename}")
        print(f"📅 创建时间: {photo.created}")
        
        # 获取下载链接
        download = photo.download()
        
        output_path = os.path.join(output_dir, photo.filename)
        
        with open(output_path, 'wb') as f:
            f.write(download.raw.read())
        
        file_size = os.path.getsize(output_path) / 1024 / 1024
        print(f"\n✅ 已下载: {output_path} ({file_size:.1f}MB)")
        
    except Exception as e:
        print(f"❌ 下载失败: {e}")


def photo_info(api, index, album_name="All Photos"):
    """显示照片详细信息"""
    try:
        albums = api.photos.albums
        album = albums.get(album_name, albums["All Photos"])
        photos = list(album.photos)
        
        if index < 1 or index > len(photos):
            print(f"❌ 照片索引超出范围 (1-{len(photos)})")
            return
        
        photo = photos[index - 1]
        
        print(f"\n📷 照片信息:\n")
        print(f"  文件名:   {photo.filename}")
        print(f"  创建时间: {photo.created}")
        print(f"  添加时间: {photo.added_date if hasattr(photo, 'added_date') else 'N/A'}")
        print(f"  尺寸:     {photo.dimensions if hasattr(photo, 'dimensions') else 'N/A'}")
        print(f"  大小:     {photo.size / 1024 / 1024:.2f}MB" if hasattr(photo, 'size') and photo.size else "")
        
        # 显示可用版本
        if hasattr(photo, 'versions'):
            print(f"\n  可用版本:")
            for version_name, version in photo.versions.items():
                print(f"    - {version_name}: {version.get('width', '?')}x{version.get('height', '?')}")
        
    except Exception as e:
        print(f"❌ 获取信息失败: {e}")


def show_help():
    """显示帮助信息"""
    print("""
iCloud Photos 访问脚本

用法:
  python icloud-photos.py albums              列出所有相册
  python icloud-photos.py list [N]            列出前N张照片 (默认20)
  python icloud-photos.py list -a ALBUM [N]   列出特定相册的照片
  python icloud-photos.py download N          下载第N张照片
  python icloud-photos.py info N              显示第N张照片信息
  python icloud-photos.py help                显示此帮助

环境变量:
  ICLOUD_USERNAME    Apple ID 邮箱
  ICLOUD_PASSWORD    应用专用密码
  ICLOUD_CHINA       设为 1 表示中国大陆用户

示例:
  export ICLOUD_USERNAME="your@icloud.com"
  export ICLOUD_PASSWORD="xxxx-xxxx-xxxx-xxxx"
  
  python icloud-photos.py albums
  python icloud-photos.py list 50
  python icloud-photos.py download 1

注意:
  - 下载大量照片请使用 icloudpd 工具
  - 此脚本适合查看和下载单张照片
  - 照片编号从 1 开始
""")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help', 'help'):
        show_help()
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "albums":
        api = get_api()
        list_albums(api)
        
    elif cmd == "list":
        api = get_api()
        # 解析参数
        album = "All Photos"
        limit = 20
        
        args = sys.argv[2:]
        i = 0
        while i < len(args):
            if args[i] == "-a" and i + 1 < len(args):
                album = args[i + 1]
                i += 2
            elif args[i].isdigit():
                limit = int(args[i])
                i += 1
            else:
                i += 1
        
        list_photos(api, album, limit)
        
    elif cmd == "download":
        if len(sys.argv) < 3:
            print("❌ 请指定照片编号")
            print("用法: python icloud-photos.py download N")
            sys.exit(1)
        
        api = get_api()
        index = int(sys.argv[2])
        download_photo(api, index)
        
    elif cmd == "info":
        if len(sys.argv) < 3:
            print("❌ 请指定照片编号")
            sys.exit(1)
        
        api = get_api()
        index = int(sys.argv[2])
        photo_info(api, index)
        
    else:
        print(f"❌ 未知命令: {cmd}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
