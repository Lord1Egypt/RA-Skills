---
name: aria2-downloader
version: 1.0.0
description: "Remote control aria2 via JSON-RPC API. Add downloads (magnet/HTTP/FTP), check progress, pause/resume/remove tasks, batch download from text. NOT for local aria2c CLI."
---

# aria2 Downloader

通过 aria2 JSON-RPC API 远程控制 aria2 下载服务。

## 首次配置

在 workspace 根目录创建 `.aria2-config.json`：

```json
{
  "url": "https://your-server.com/jsonrpc",
  "token": "your-secret-token"
}
```

> ⚠️ 此文件包含敏感信息，已在 `.gitignore` 中排除。

## 功能

| 功能 | 说明 |
|------|------|
| 📥 添加下载 | 支持磁力链接、HTTP/FTP 直链 |
| 📋 查看任务 | 查看所有活跃/等待/已完成的任务 |
| ⏸️ 暂停任务 | 暂停指定下载 |
| ▶️ 恢复任务 | 恢复暂停的下载 |
| 🗑️ 删除任务 | 删除指定下载任务 |
| 📄 批量下载 | 发送文本（每行一个链接），逐个添加 |

## 使用方式

### 添加下载

用户说：
- "下载这个 magnet:?xt=urn:btih:..."
- "下载 https://example.com/file.zip"
- "添加下载：magnet:?xt=..."

→ 调用 `scripts/aria2.js add <url>`

### 查看任务

用户说：
- "查看下载进度"
- "aria2 状态"
- "下载到哪了"

→ 调用 `scripts/aria2.js list`

### 暂停任务

用户说：
- "暂停下载 xxx"
- "暂停 GID abc123"

→ 调用 `scripts/aria2.js pause <gid>`

### 恢复任务

用户说：
- "恢复下载 xxx"
- "继续下载 GID abc123"

→ 调用 `scripts/aria2.js unpause <gid>`

### 删除任务

用户说：
- "取消下载 xxx"
- "删除 GID abc123"

→ 调用 `scripts/aria2.js remove <gid>`

### 批量下载

用户发送一段文本（每行一个链接）：
```
magnet:?xt=urn:btih:aaa...
magnet:?xt=urn:btih:bbb...
https://example.com/file1.zip
https://example.com/file2.zip
```

→ 调用 `scripts/aria2.js batch` 并通过 stdin 传入链接

## 脚本说明

所有操作通过 `scripts/aria2.js` 执行：

```bash
# 查看帮助
node scripts/aria2.js help

# 添加下载
node scripts/aria2.js add "magnet:?xt=urn:btih:..."

# 查看所有任务
node scripts/aria2.js list

# 暂停
node scripts/aria2.js pause <gid>

# 恢复
node scripts/aria2.js unpause <gid>

# 删除
node scripts/aria2.js remove <gid>

# 批量下载（stdin 传入链接，每行一个）
echo -e "magnet:?xt=...\nhttps://..." | node scripts/aria2.js batch
```

## 配置文件

读取 workspace 根目录的 `.aria2-config.json`：

```json
{
  "url": "https://your-server.com/jsonrpc",
  "token": "your-secret-token"
}
```

如果配置文件不存在，提示用户创建。

## 输出格式

### 任务列表
```
📋 活跃任务 (3):
  [abc123] ▓▓▓▓▓▓▓▓░░ 78.5% | 12.3 MB/s | Ubuntu-22.04.iso
  [def456] ▓▓░░░░░░░░ 15.2% | 5.6 MB/s  | movie.mkv
  [ghi789] ▓▓▓▓▓▓▓▓▓▓ 100%  | 完成       | file.zip

⏳ 等待中 (1):
  [jkl012] 等待中 | BigFile.tar.gz

✅ 已完成 (2):
  [mno345] 100% | archive.rar
  [pqr678] 100% | document.pdf
```

### 添加下载
```
✅ 已添加下载
GID: abc123
文件: Ubuntu-22.04.iso
```

### 批量下载
```
📥 批量下载 (4 个链接):
  ✅ [1] magnet:?xt=... → GID: abc123
  ✅ [2] magnet:?xt=... → GID: def456
  ✅ [3] https://example.com/file1.zip → GID: ghi789
  ❌ [4] invalid-url → 失败: 无效链接
```

## 注意事项

- **不轮询**：只在用户请求时查看进度
- **不硬编码**：URL 和 Token 由用户配置
- **链接类型**：支持 magnet、http、https、ftp
- **依赖**：Node.js（无需额外 npm 包，使用原生 fetch）
