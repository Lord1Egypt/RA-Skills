---
name: aria2-download
description: 通过 Aria2 RPC 添加下载任务，支持实时进度监控。
homepage: https://github.com
metadata:
  {
    "openclaw": {
      "emoji": "⬇️"
    }
  }
---

# Aria2 Download

通过 Aria2 RPC 添加下载任务，支持实时进度监控。

## 功能

- ✅ 添加下载任务
- ✅ 实时进度监控
- ✅ 下载完成后输出详细信息
- ✅ 支持 HTTP/FTP/M3U8 等协议
- ✅ 多线程高速下载

## 配置

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `ARIA2_RPC_URL` | http://localhost:6800/jsonrpc | RPC 地址 |
| `ARIA2_SECRET` | - | RPC 密钥 |
| `ARIA2_DIR` | - | 下载目录 |

### 配置示例

```bash
export ARIA2_RPC_URL="http://10.0.0.1:6800/jsonrpc"
export ARIA2_SECRET="88888888"
export ARIA2_DIR="/mnt/sda1/download"
```

## 使用方法

### 添加下载

```bash
aria2-download add "https://example.com/video.mp4"
```

### 查询状态

```bash
aria2-download status <gid>
```

### 单次进度

```bash
aria2-download progress <gid>
```

### 实时监控

```bash
aria2-download watch <gid> [间隔秒数]
```

### 等待完成

```bash
aria2-download wait <gid>
```

### 列出活跃任务

```bash
aria2-download list
```

## 输出示例

### 下载完成

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 下载完成！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 文件: video.mp4
📂 路径: /mnt/sda1/download
💾 大小: 100.50 MB (1文件)
📊 状态: 已完成
📈 进度: 100%
📥 下载量: 100.50 MB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 实时监控

```
████████████████████ 100.0% | 10.0MB/s | video.mp4
```

## Aria2 安装

### Docker (推荐)

```bash
docker run -d --name aria2 \
  -p 6800:6800 \
  -v /path/to/downloads:/downloads \
  -e ARIA2_SECRET=88888888 \
  p3terx/aria2-pro
```

### Linux

```bash
# Ubuntu/Debian
apt install aria2

# 启动 RPC
aria2c --enable-rpc --rpc-listen-all=true --rpc-secret=88888888 --dir=/path/to/downloads
```

### macOS

```bash
brew install aria2
```

## 配合 x-media-parser 使用

```bash
# 一键解析+下载
x-aria-download "https://x.com/user/status/123"
```

或手动：

```bash
# 1. 解析帖子
URL=$(x-media-parser "https://x.com/user/status/123" | jq -r '.media.directUrl')

# 2. 添加下载
aria2-download add "$URL"
```
