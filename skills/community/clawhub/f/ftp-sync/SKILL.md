---
name: ftp-sync
version: 1.0.0
description: FTP/SFTP 同步工具。本地与远程服务器文件同步，支持增量备份。适合网站维护和服务器管理。
author: 你的名字
triggers:
  - "FTP同步"
  - "文件同步"
  - "服务器同步"
  - "SFTP"
---

# FTP/SFTP Sync 🔄

本地与远程服务器文件同步。

## 功能

- 📤 SFTP 上传/下载
- 🔄 增量同步
- 📊 同步报告
- 🔒 支持密钥认证

## 使用方法

### 上传同步

```bash
python3 scripts/ftp_sync.py upload ./local_folder/ --host 192.168.1.1 --user root --password xxx
```

### 下载同步

```bash
python3 scripts/ftp_sync.py download /remote/folder/ --host 192.168.1.1 --user root
```

### 对比差异

```bash
python3 scripts/ftp_sync.py diff ./local/ /remote/ --host xxx
```

## 示例

```bash
# 上传网站文件
python3 scripts/ftp_sync.py upload ./dist/ --host example.com --user ftpuser --password pass123 --remote /var/www/html/

# 增量同步
python3 scripts/ftp_sync.py upload ./data/ --host example.com --user user --password pass --sync
```
