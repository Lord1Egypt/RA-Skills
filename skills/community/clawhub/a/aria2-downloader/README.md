# aria2-downloader

通过 aria2 JSON-RPC API 远程控制 aria2 下载服务。

## 功能

- 📥 添加下载（磁力链接、HTTP/FTP 直链）
- 📋 查看任务列表和进度
- ⏸️ 暂停 / ▶️ 恢复 / 🗑️ 删除任务
- 📄 批量下载（文本解析）

## 配置

在 workspace 根目录创建 `.aria2-config.json`：

```json
{
  "url": "https://your-server.com/jsonrpc",
  "token": "your-secret-token"
}
```

## 使用

```bash
# 添加下载
node scripts/aria2.js add "magnet:?xt=urn:btih:..."

# 查看任务
node scripts/aria2.js list

# 暂停
node scripts/aria2.js pause <gid>

# 恢复
node scripts/aria2.js unpause <gid>

# 删除
node scripts/aria2.js remove <gid>

# 批量下载（stdin）
echo -e "magnet:?xt=...\nhttps://..." | node scripts/aria2.js batch
```

## 无外部依赖

使用 Node.js 原生 `http`/`https` 模块，无需 `npm install`。
