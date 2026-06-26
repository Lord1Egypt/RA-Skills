---
name: aliyundrive-uploader
description: 阿里云盘文件上传与管理。使用 refresh_token 认证，支持大文件分片上传、自动创建文件夹、文件搜索、分享链接等。当用户需要上传文件到阿里云盘、创建文件夹、搜索文件、管理分享链接时使用。
---

# 阿里云盘上传技能

使用阿里云盘官方 SDK (`aliyunpan` Python 包) 进行文件操作。

## 前置安装（首次使用）

```bash
python3 -m venv /tmp/venv
/tmp/venv/bin/pip install aliyunpan requests
```

## 环境配置

在 `.env` 文件中配置：

```bash
ALIYUN_DRIVE_REFRESH_TOKEN="your_refresh_token"
```

获取 refresh_token：登录阿里云盘网页版 → F12 → Application → Local Storage → 找 `refreshToken`

## 支持操作

| action | 说明 | 关键参数 |
|--------|------|----------|
| `upload` | 上传文件 | `file_path`, `target_folder` |
| `list` | 列出文件 | `parent_id` (默认 root) |
| `create_folder` | 创建文件夹 | `name`, `parent_id` |
| `search` | 搜索文件 | `name`, `parent_id` |
| `share` | 创建分享链接 | `file_id` |
| `delete` | 删除文件 | `file_id` |
| `download_url` | 获取下载链接 | `file_id` |
| `user_info` | 获取用户信息 | - |

## 使用示例

### 上传文件
```
action: upload
file_path: /path/to/file.png
target_folder: backup
```

### 列出文件夹内容
```
action: list
parent_id: 69f3075d2490bbe147834f8ba84df323453f4d08
```

### 创建文件夹
```
action: create_folder
name: backup
parent_id: root
```

### 搜索文件
```
action: search
name: openclaw.png
```

## 文件路径格式

- `target_folder`: 文件夹名称（如 `openclaw`），在根目录创建/查找
- `parent_id`: 直接指定父文件夹 ID

## 实现说明

- token 刷新后自动保存回 `.env`
- 大文件自动分片上传
- 秒传支持（文件 hash 匹配时直接成功）
- 使用 Python `aliyunpan` SDK (3.0.9)，是唯一能正常工作的 SDK
