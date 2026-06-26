---
name: aliyun-codeup
description: 阿里云云效 Codeup 代码仓库管理 - 查询项目、分支、提交记录等
metadata: {"version":"1.0.0","author":"Hank"}
---

# 阿里云云效 Codeup 技能

通过个人访问令牌访问阿里云云效 Codeup 代码仓库。

## 🔑 配置要求

### 1. 环境变量

在 `~/.zshrc` 或 Gateway 环境变量中配置：

```bash
export YUNXIAO_PERSONAL_TOKEN="pt-xxx"  # 云效个人访问令牌
```

### 2. 令牌获取

1. 访问 https://codeup.aliyun.com/
2. 右上角头像 → 个人设置 → 个人访问令牌
3. 创建令牌，勾选权限：
   - `read_api` - 读取代码库
   - `read_repository` - 读取仓库

## 🛠️ 功能

### 查询项目分支

**输入：** 项目 URL 或路径
**输出：** 分支列表、统计信息

**示例：**
```
查看云效项目 https://codeup.aliyun.com/flashexpress/ard/be/tools/data-admin-api 的分支
```

### 查询项目信息

**输入：** 项目 URL
**输出：** 项目名称、描述、成员数、最近活动

### 查询提交记录

**输入：** 项目 URL + 分支名
**输出：** 最近提交记录、提交者、时间

### 分析分支活跃度

**输入：** 项目 URL
**输出：** 各分支最后提交时间、活跃度排名

## 📋 使用方式

### 方式 1：Git Clone（推荐）

```bash
# 临时克隆查询
git clone --quiet "https://oauth2:$YUNXIAO_PERSONAL_TOKEN@codeup.aliyun.com/<path>.git"
cd <repo> && git branch -a
cd /tmp && rm -rf <repo>
```

**优点：**
- ✅ 稳定可靠
- ✅ 支持所有 Git 操作
- ✅ 无需处理 API 分页

**缺点：**
- ⚠️ 需要临时克隆（小项目很快）

### 方式 2：HTTP API

```bash
# 查询分支
curl -s "https://codeup.aliyun.com/api/v3/projects/<id>/repository/branches" \
  -H "Private-Token: $YUNXIAO_PERSONAL_TOKEN"

# 查询项目
curl -s "https://codeup.aliyun.com/api/v3/projects?search=<name>" \
  -H "Private-Token: $YUNXIAO_PERSONAL_TOKEN"
```

**优点：**
- ✅ 快速（无需克隆）
- ✅ 节省带宽

**缺点：**
- ⚠️ API 地址可能变化
- ⚠️ 需要处理认证重定向

## 🔧 核心脚本

### codeup_cli.py

```python
#!/usr/bin/env python3
"""
阿里云云效 Codeup CLI 工具
"""

import subprocess
import sys
import os
import tempfile
import shutil
from urllib.parse import urlparse

def get_token():
    """从环境变量获取令牌"""
    token = os.getenv('YUNXIAO_PERSONAL_TOKEN')
    if not token:
        print("❌ 错误：未配置 YUNXIAO_PERSONAL_TOKEN 环境变量")
        sys.exit(1)
    return token

def parse_project_url(url):
    """解析项目 URL"""
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    # 移除末尾的 /branches, /commits 等
    if '/' in path:
        parts = path.split('/')
        if parts[-1] in ['branches', 'commits', 'tree', 'blob']:
            path = '/'.join(parts[:-1])
    return path

def clone_and_query(url):
    """临时克隆并查询分支"""
    token = get_token()
    project_path = parse_project_url(url)
    
    # 创建临时目录
    tmp_dir = tempfile.mkdtemp(prefix='codeup_')
    repo_name = project_path.split('/')[-1]
    repo_path = os.path.join(tmp_dir, repo_name)
    
    try:
        # 克隆仓库
        git_url = f"https://oauth2:{token}@codeup.aliyun.com/{project_path}.git"
        subprocess.run(
            ['git', 'clone', '--quiet', '--depth=1', git_url, repo_path],
            check=True,
            capture_output=True
        )
        
        # 查询分支
        result = subprocess.run(
            ['git', 'branch', '-a'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        
        # 解析分支列表
        branches = []
        for line in result.stdout.strip().split('\n'):
            if line.strip() and 'HEAD' not in line:
                branch = line.replace('*', '').replace('remotes/origin/', '').strip()
                if branch:
                    branches.append(branch)
        
        return {
            'success': True,
            'project': repo_name,
            'branches': sorted(branches),
            'total': len(branches)
        }
        
    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'error': f'Git 操作失败：{e.stderr.decode() if e.stderr else str(e)}'
        }
    finally:
        # 清理临时目录
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)

def main():
    if len(sys.argv) < 2:
        print("用法：codeup_cli.py <项目 URL>")
        print("示例：codeup_cli.py https://codeup.aliyun.com/flashexpress/ard/be/tools/data-admin-api")
        sys.exit(1)
    
    url = sys.argv[1]
    result = clone_and_query(url)
    
    if result['success']:
        print(f"✅ 项目：{result['project']}")
        print(f"📊 分支总数：{result['total']}")
        print("\n分支列表:")
        for branch in result['branches']:
            print(f"  - {branch}")
    else:
        print(f"❌ 错误：{result['error']}")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

## 📖 使用示例

### 示例 1：查询分支

**用户：** 查看云效项目 https://codeup.aliyun.com/flashexpress/ard/be/tools/data-admin-api 的分支

**执行：**
```bash
cd /tmp && rm -rf data-admin-api
git clone --quiet "https://oauth2:$YUNXIAO_PERSONAL_TOKEN@codeup.aliyun.com/flashexpress/ard/be/tools/data-admin-api.git"
cd data-admin-api && git branch -a | grep -v HEAD | sed 's/remotes\/origin\///' | sort
cd /tmp && rm -rf data-admin-api
```

**输出：**
```
📊 项目：data-admin-api
📊 分支总数：62

主分支:
  - master

功能分支 (45):
  - feature/common.20251211
  - feature/common.20251105
  - feature/20250730.geminifile
  ...

热修复分支 (15):
  - hotfix/myj.250723
  - hotfix/myj.batch
  ...
```

### 示例 2：分析分支活跃度

**用户：** 分析这个项目哪些分支最近有更新

**执行：**
```bash
cd /tmp/data-admin-api
git branch -a --sort=-committerdate | head -20
```

**输出：**
```
📈 最近活跃的分支（按最后提交时间）:

1. master - 2 小时前
2. feature/common.20251211 - 1 天前
3. hotfix/myj.250723 - 3 天前
...
```

## ⚠️ 注意事项

### 安全

- ✅ 令牌存储在环境变量，不写入代码
- ✅ 临时克隆后自动清理
- ❌ 不要将令牌写入文档或日志

### 性能

- 小项目（<100MB）：克隆约 5-10 秒
- 中项目（100-500MB）：克隆约 10-30 秒
- 大项目（>500MB）：建议使用 API 或浅克隆（--depth=1）

### 权限

令牌需要以下权限：
- `read_api` - 读取项目信息
- `read_repository` - 克隆仓库

## 🔗 相关资源

- [云效 Codeup 文档](https://help.aliyun.com/product/44893.html)
- [GitLab API 文档](https://docs.gitlab.com/ee/api/)（云效基于 GitLab）
- [个人访问令牌管理](https://codeup.aliyun.com/settings/tokens)

---

**版本：** 1.0.0  
**创建时间：** 2026-03-06  
**维护者：** 汉克 (Hank)
