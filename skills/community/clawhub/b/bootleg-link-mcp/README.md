# 🎵 Bootleg-Link MCP v0.9.0

> AI 助手专属的音乐下载 MCP 服务器 — YouTube、Qobuz、Beatport 一站式下载，CDJ-2000 兼容格式

---

## 功能矩阵

### 🎧 下载与任务管理
| 工具 | 功能 |
|------|------|
| `submit_download_task` | 提交 YouTube 下载（支持频道/播放列表/单视频/搜索） |
| `query_progress` | 查询任务进度（含下载目录、链接、入库数） |
| `list_tasks` | 列出所有任务 |
| `cancel_task` | 取消任务 |
| `clear_completed` / `clear_database` | 清理已完成/清空数据库 |
| `get_queue_status` | 队列状态（并发数、引擎信息） |

### 📺 YouTube
| 工具 | 功能 |
|------|------|
| `youtube_login` | Playwright 隐身登录 Google 账号 |
| `youtube_auth_status` | 检查 cookie 认证状态 |
| `youtube_logout` | 清除登录 |

### 🎹 Qobuz
| 工具 | 功能 |
|------|------|
| `qobuz_login` | 登录 Qobuz |
| `qobuz_search` | 搜索曲目/专辑/艺人 |
| `qobuz_download` | 下载高解析音频（MP3 320 / CD FLAC / Hi-Res 96k / 192k） |
| `qobuz_my_purchases` | 列出已购/收藏曲目 |

### 🎧 Beatport
| 工具 | 功能 |
|------|------|
| `beatport_login` | Playwright 登录 Beatport |
| `beatport_search` | 搜索 Beatport 曲库 |
| `beatport_download` | 下载已购曲目 |

---

## 🎚️ CDJ-2000 兼容格式

每首下载的 MP3 自动处理为老设备兼容格式：

- **48kHz / 320k CBR** 恒定比特率
- **JPEG 封面**嵌入（WebP→JPEG 自动转换）
- **无视频流**（`-vn` 清除）
- **ID3v2.3 标签**（artist、title、BPM、调性等完整元数据）

---

## ⚙️ 核心特性

### 智能下载目录
下载时自动从 URL 提取标签名/频道名在默认目录下建子目录。
```json
// ~/.bootleg-link-mcp/config.json
{
  "paths": { "outputDir": "/mnt/e/music" },
  "download": { "maxConcurrent": 32, "quality": "320" },
  "proxy": { "http": "http://100.64.0.3:1081" }
}
```
不指定 `outputDir` → 自动按 `[Label Name]` 建子目录。

### 断点续传
- SQLite 持久化每个任务的进度
- 重启后自动恢复未完成任务
- `downloaded_videos` 表去重，已下载的自动跳过

### YouTube 隐身登录
- Playwright + Xvfb 非无头 Chromium 绕过反爬检测
- 自动导出 Netscape 格式 cookie 给 yt-dlp 使用

### bgutil PO Token 自动启动
- 服务启动时自动拉起 `bgutil-ytdlp-pot-provider` HTTP 服务（端口 4416）
- Node.js v24+ 路径自动定位（`~/.nvm/versions/node/`）

### 并行分页下载
- 播放列表/频道按 100 条分页拉取（flat-playlist 模式）
- 内层 `ThreadPoolExecutor` 并发下载（最大 32 线程）
- 首映视频自动跳过

### 文件命名规范
```
Artist - Title (Remixer Remix) [LABEL].mp3
```
- 缺艺术家 → YouTube 详情页自动提取 `artist` 字段
- 缺混音标记 → 自动补 `(Original Mix)`
- 多标签自动识别（TECHAWAY RECORDS、NVDRZ、DRUMCODE 等 10+ label）

---

## 🔌 安装

```json
// .mcp.json
{
  "mcpServers": {
    "bootleg-link": {
      "command": "/opt/pyenv/versions/3.11.8/bin/python3",
      "args": ["/path/to/bootleg-link-mcp/src/server.py"],
      "env": {
        "BOOTLEG_DB_PATH": "/path/to/bootleg-link.db",
        "BOOTLEG_HTTP_PROXY": "http://proxy:1081",
        "BOOTLEG_HTTPS_PROXY": "http://proxy:1081"
      }
    }
  }
}
```

### 前置依赖
```bash
pip install yt-dlp mutagen
# YouTube 登录需要: playwright (chromium)
# Qobuz 需要: qobuz-dl
# Node.js ≥24 (配合 bgutil PO Token)
```

---

## 🗂️ 数据库

| 表 | 用途 |
|---|------|
| `tasks` | 任务状态（14 字段：url、outputDir、进度、songsCompleted 等） |
| `downloaded_videos` | 已下载视频去重（task_id + video_id 联合主键） |

---

## 🔧 技术栈

- **yt-dlp** Python API（2026.05.25+）
- **SQLite** 持久化
- **ThreadPoolExecutor** 双层并发
- **Playwright** 隐身浏览器登录
- **bgutil-ytdlp-pot-provider** PO Token 绕过
- **mutagen** ID3 标签处理
- **ffmpeg** 音频提取 + 格式转换 + 封面转换

---

## 🗺️ 路线图

### 🎯 正版优先无缝切换（设计阶段）

核心理念：**Bootleg-Link Flow — Try Before Buy，先听再买**。

```
下载请求
   │
   ▼
┌────────────────────────────────────────────┐
│              ① YouTube 快速下载              │
│  获取完整试听 + ID3 标签 (artist/title/BPM/调性) │
└──────────────────┬─────────────────────────┘
                   │ 试听评估
                   ▼
          ┌────你决定买吗？────┐
          │                    │
          ▼ yes                ▼ no
   ┌──────────────┐     ┌──────────┐
   │ ② 正版替换    │     │ 保留试听版 │
   │ Beatport/Qobuz│     └──────────┘
   │ 下载并覆盖文件  │
   │ 保留全部 ID3   │
   └──────────────┘
          │
          ▼
   ✅ 正版文件已替换，强迫症友好：
   • 正版高分辨率封面替换 YouTube 低清缩略图
   • 曲目命名统一为 Artist - Title (Mix) [LABEL]
   • ID3 标签完整保留（artist/title/BPM/调性/年份/流派）

### 📋 具体计划

| 阶段 | 内容 | 状态 |
|------|------|------|
| 1 | 曲目指纹匹配（artist + title + duration 多维度） | 待开发 |
| 2 | YouTube 批量试听下载 + 完整 ID3 标签 | ✅ 已实现 |
| 3 | 试听后标记"想买"曲目列表 | 待开发 |
| 4 | Beatport/Qobuz 一键正版替换（ID3 + 封面 + 命名全保留） | 已有 API |
| 5 | 按月汇总：试听数 / 购买数 / 待购清单 | 待开发 |
| 6 | 自动生成 Beatport 购物车链接 | 待开发 |

### 💡 使用场景

> "周五晚上刷 YouTube → 下了 500 首 Techaway Records → 周末打碟试听 → 挑了 20 首适合我 set 的 → 一键 Beatport 替换正版 → ID3 完整保留，无缝切换"

---

## 📜 License

MIT
