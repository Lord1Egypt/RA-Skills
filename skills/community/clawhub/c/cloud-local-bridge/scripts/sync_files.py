#!/usr/bin/env python3
"""
文件同步脚本
在云端和本地之间同步文件/目录
"""

import os
import json
import argparse
from pathlib import Path
import hashlib
import pickle
from datetime import datetime

try:
    import requests
except ImportError:
    print("请安装 requests: pip install requests")
    exit(1)


class FileSync:
    def __init__(self, server_url, token, sync_file='.sync_cache.pkl'):
        self.server_url = server_url.rstrip('/')
        self.token = token
        self.sync_cache_file = sync_file
        self.cache = self.load_cache()
    
    def load_cache(self):
        """加载同步缓存"""
        if os.path.exists(self.sync_cache_file):
            with open(self.sync_cache_file, 'rb') as f:
                return pickle.load(f)
        return {}
    
    def save_cache(self):
        """保存同步缓存"""
        with open(self.sync_cache_file, 'wb') as f:
            pickle.dump(self.cache, f)
    
    def get_file_hash(self, filepath):
        """计算文件哈希"""
        if not os.path.isfile(filepath):
            return None
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()
    
    def sync_to_remote(self, local_dir, remote_base):
        """同步本地目录到远程"""
        import base64
        
        local_path = Path(local_dir)
        if not local_path.exists():
            print(f"❌ 本地目录不存在: {local_dir}")
            return
        
        changes = []
        
        for root, dirs, files in os.walk(local_path):
            rel_dir = os.path.relpath(root, local_path)
            
            for file in files:
                local_file = os.path.join(root, file)
                remote_file = os.path.join(remote_base, rel_dir, file) if rel_dir != '.' else os.path.join(remote_base, file)
                
                # 检查是否有变化
                file_hash = self.get_file_hash(local_file)
                cache_key = remote_file
                
                if self.cache.get(cache_key) != file_hash:
                    changes.append((local_file, remote_file))
        
        if not changes:
            print("✅ 没有需要同步的文件")
            return
        
        print(f"📤 准备同步 {len(changes)} 个文件...")
        
        for local_file, remote_file in changes:
            try:
                # 读取并编码文件
                with open(local_file, 'rb') as f:
                    content = base64.b64encode(f.read()).decode('utf-8')
                
                # 上传
                response = requests.post(
                    f"{self.server_url}/file",
                    json={
                        "action": "upload",
                        "path": remote_file,
                        "base64_content": content
                    },
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                
                if response.status_code == 200:
                    # 更新缓存
                    self.cache[remote_file] = self.get_file_hash(local_file)
                    print(f"  ✅ {remote_file}")
                else:
                    print(f"  ❌ {remote_file}: {response.text}")
                    
            except Exception as e:
                print(f"  ❌ {remote_file}: {e}")
        
        self.save_cache()
        print(f"✅ 完成! 同步了 {len(changes)} 个文件")
    
    def sync_from_remote(self, remote_dir, local_base):
        """从远程同步到本地"""
        response = requests.post(
            f"{self.server_url}/file",
            json={
                "action": "list",
                "path": remote_dir
            },
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        if response.status_code != 200:
            print(f"❌ 获取文件列表失败: {response.text}")
            return
        
        files = response.json().get('files', [])
        
        for remote_file in files:
            local_file = os.path.join(local_base, os.path.relpath(remote_file, remote_dir))
            
            # 下载文件
            response = requests.post(
                f"{self.server_url}/file",
                json={
                    "action": "download",
                    "path": remote_file
                },
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'base64_content' in result:
                    import base64
                    os.makedirs(os.path.dirname(local_file), exist_ok=True)
                    content = base64.b64decode(result['base64_content'])
                    with open(local_file, 'wb') as f:
                        f.write(content)
                    print(f"  ✅ {local_file}")


def main():
    parser = argparse.ArgumentParser(description='文件同步工具')
    parser.add_argument('--server', required=True, help='Bridge 服务器地址')
    parser.add_argument('--token', required=True, help='认证 token')
    parser.add_argument('--local', required=True, help='本地目录')
    parser.add_argument('--remote', required=True, help='远程路径')
    parser.add_argument('--direction', choices=['upload', 'download', 'sync'], 
                        default='sync', help='同步方向')
    
    args = parser.parse_args()
    
    sync = FileSync(args.server, args.token)
    
    if args.direction in ['upload', 'sync']:
        print(f"📤 同步到远程: {args.remote}")
        sync.sync_to_remote(args.local, args.remote)
    
    if args.direction in ['download', 'sync']:
        print(f"📥 从远程同步: {args.remote}")
        sync.sync_from_remote(args.remote, args.local)


if __name__ == '__main__':
    main()
