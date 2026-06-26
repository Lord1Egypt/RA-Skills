# C17 - 百度网盘

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C17 |
| 连接器名 | baidu-netdisk |
| 显示名 | 百度网盘 |
| 层级 | L2 鉴权便利型 |
| 可替代 | ✅ 可替代（Skill） |
| 分类 | 存储 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 文件上传 | 上传文件到网盘 |
| 文件下载 | 从网盘下载文件 |
| 文件管理 | 创建/删除/移动文件夹 |
| 文件列表 | 列出目录内容 |
| 分享链接 | 生成分享链接 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
├── L2-auth-storage-C17-baidu-list-files.py  # 列出文件
└── L2-auth-storage-C17-baidu-upload.py      # 上传文件
```

### 鉴权方式

**OAuth2**：
1. 在百度网盘开放平台 (https://pan.baidu.com/union) 注册开发者
2. 创建应用并获取 `AppKey` + `SecretKey`
3. 引导用户授权：`https://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id={AppKey}&redirect_uri={redirect_uri}&scope=basic,netdisk`
4. 用授权码换取访问令牌：`POST https://openapi.baidu.com/oauth/2.0/token?grant_type=authorization_code&code={code}&client_id={AppKey}&client_secret={SecretKey}&redirect_uri={redirect_uri}`
5. 获取 `access_token` + `refresh_token`
6. `access_token` 有效期 30 天，用 `refresh_token` 刷新

**环境变量配置**：
```bash
export BAIDU_PAN_APP_KEY="your_app_key"
export BAIDU_PAN_SECRET_KEY="your_secret_key"
export BAIDU_PAN_ACCESS_TOKEN="your_access_token"
```

### 核心脚本示例

**L2-auth-storage-C17-baidu-list-files.py**：
```python
#!/usr/bin/env python3
"""列出百度网盘文件"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://pan.baidu.com/rest/2.0/xpan/file"

def list_files(path: str = "/", order: str = "time", desc: bool = True) -> dict:
    """列出目录内容"""
    access_token = os.environ.get("BAIDU_PAN_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("未设置 BAIDU_PAN_ACCESS_TOKEN 环境变量")
    
    params = {
        "method": "list",
        "access_token": access_token,
        "dir": path,
        "order": order,  # time, name, size
        "desc": 1 if desc else 0,
        "web": 1
    }
    
    resp = requests.get(API_BASE, params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    file_list = data.get("list", [])
    if not file_list:
        return "目录为空"
    
    output = f"## 文件列表（共 {len(file_list)} 个）\n\n"
    output += "| 类型 | 文件名 | 大小 | 修改时间 |\n"
    output += "|------|--------|------|----------|\n"
    
    for item in file_list:
        is_dir = "📁" if item.get("isdir") else "📄"
        name = item.get("server_filename", "-")
        size = item.get("size", 0)
        mtime = item.get("mtime", 0)
        
        # 格式化大小
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024 * 1024:
            size_str = f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            size_str = f"{size / (1024 * 1024):.1f} MB"
        else:
            size_str = f"{size / (1024 * 1024 * 1024):.1f} GB"
        
        # 格式化时间
        from datetime import datetime
        mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M") if mtime else "-"
        
        output += f"| {is_dir} | {name} | {size_str} | {mtime_str} |\n"
    
    return output

def main():
    parser = argparse.ArgumentParser(description="列出百度网盘文件")
    parser.add_argument("--path", default="/", help="目录路径")
    parser.add_argument("--order", choices=["time", "name", "size"], default="time", help="排序方式")
    parser.add_argument("--asc", action="store_true", help="升序排列")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = list_files(args.path, args.order, not args.asc)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"获取失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**L2-auth-storage-C17-baidu-upload.py**：
```python
#!/usr/bin/env python3
"""上传文件到百度网盘"""

import os
import sys
import json
import argparse
import hashlib
import requests
from pathlib import Path

API_BASE = "https://pan.baidu.com/rest/2.0/xpan/file"
UPLOAD_API = "https://d.pcs.baidu.com/rest/2.0/pcs/superfile2"

def upload_file(local_path: str, remote_path: str, rtype: int = 3) -> dict:
    """上传文件（支持分片）"""
    access_token = os.environ.get("BAIDU_PAN_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("未设置 BAIDU_PAN_ACCESS_TOKEN 环境变量")
    
    file_path = Path(local_path)
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在：{local_path}")
    
    file_size = file_path.stat().st_size
    
    # 1. 预上传
    params = {
        "method": "precreate",
        "access_token": access_token,
        "path": remote_path,
        "size": file_size,
        "isdir": 0,
        "autoinit": 1,
        "rtype": rtype  # 1-重命名 2-覆盖 3-覆盖
    }
    
    resp = requests.post(f"{API_BASE}/precreate", params=params)
    resp.raise_for_status()
    pre_data = resp.json()
    
    if pre_data.get("errno") != 0:
        raise Exception(f"预上传失败：{pre_data.get('errmsg')}")
    
    upload_key = pre_data.get("uploadid")
    block_list = pre_data.get("block_list", [])
    
    # 2. 分片上传
    uploaded_blocks = []
    with open(local_path, "rb") as f:
        for i, _ in enumerate(block_list):
            chunk = f.read(4 * 1024 * 1024)  # 4MB 分片
            chunk_md5 = hashlib.md5(chunk).hexdigest()
            
            params = {
                "method": "upload",
                "access_token": access_token,
                "type": "tmpfile",
                "path": remote_path,
                "uploadid": upload_key,
                "partseq": i
            }
            
            resp = requests.post(
                UPLOAD_API,
                params=params,
                files={"file": ("chunk", chunk)}
            )
            resp.raise_for_status()
            uploaded_blocks.append(chunk_md5)
    
    # 3. 创建文件
    params = {
        "method": "create",
        "access_token": access_token,
        "path": remote_path,
        "size": file_size,
        "isdir": 0,
        "rtype": rtype,
        "uploadid": upload_key,
        "block_list": json.dumps(uploaded_blocks)
    }
    
    resp = requests.post(f"{API_BASE}/create", params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    return f"""
上传成功：

| 字段 | 值 |
|------|-----|
| 文件路径 | {data.get('path', '-')} |
| 文件大小 | {data.get('size', '-')} |
| 文件 ID | {data.get('fs_id', '-')} |
| MD5 | {data.get('md5', '-')} |
"""

def main():
    parser = argparse.ArgumentParser(description="上传文件到百度网盘")
    parser.add_argument("local_path", help="本地文件路径")
    parser.add_argument("remote_path", help="网盘目标路径")
    parser.add_argument("--rtype", type=int, choices=[1, 2, 3], default=3, help="重名处理：1-重命名 2-覆盖 3-覆盖")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = upload_file(args.local_path, args.remote_path, args.rtype)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"上传失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 迁移成本

| 项目 | 说明 |
|------|------|
| API 变更 | 改 API 域名即可 |
| 凭证更新 | 重新授权 |
| 工作流 | 无需修改 |

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管 | 用户自管 |
| 功能 | 固定 | 可自定义 |
| 多平台 | 绑定百度 | 可对接其他网盘 |
| 输出格式 | 固定 | 模板化可定制 |
| 迁移 | 重配连接器 | 改 API 地址 |
