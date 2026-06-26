
<p align="center">
  <h1 align="center">🎬 Bilibili All-in-One</h1>
  <p align="center">一站式 B站工具箱 — 热门监控 · 视频下载 · 数据追踪 · 字幕提取 · 视频播放 · 投稿发布</p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-%3E%3D3.8-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
  <img src="https://img.shields.io/badge/version-1.0.9-orange" />
  <img src="https://img.shields.io/badge/platform-Bilibili%20%7C%20YouTube-pink" />
</p>

---

## 📖 简介

**Bilibili All-in-One** 是一个综合性的 B站工具包，将 6 个独立的 B站技能整合为一个统一的 Skill，提供从热门监控到视频投稿的全链路能力。

支持作为 **AI Agent 技能**、**命令行工具** 或 **Python 库** 使用。

## ✨ 功能总览

| 模块 | 功能 | 是否需要登录 |
|:---:|---|:---:|
| 🔥 **热门监控** | 热门视频、热搜话题、每周必看、分区排行榜 | ❌ |
| ⬇️ **视频下载** | 多清晰度下载、批量下载、格式转换、音频提取 | ⚠️ 高清需要 |
| 👀 **数据追踪** | 播放/点赞/收藏统计、数据追踪、多视频对比（支持 YouTube） | ❌ |
| 📝 **字幕提取** | 字幕下载、格式转换（SRT/ASS/VTT/TXT）、多语言、字幕合并 | ❌ |
| ▶️ **视频播放** | 播放地址获取、弹幕抓取、分P/播放列表信息 | ⚠️ 高清需要 |
| 📤 **视频发布** | 上传投稿、定时发布、草稿管理、编辑/删除视频 | ✅ 必须 |

## 🚀 快速开始

### 环境要求

- **Python** >= 3.8
- **ffmpeg**（可选，用于合并视频/音频流）

### 安装依赖

```bash
git clone https://github.com/wscats/bilibili-all-in-one.git
cd bilibili-all-in-one
pip install -r requirements.txt
```

### 30 秒上手

```python
import asyncio
from main import BilibiliAllInOne

app = BilibiliAllInOne()

async def main():
    # 获取 B站热门视频
    hot = await app.execute("hot_monitor", "get_hot", page_size=5)
    print(hot)

asyncio.run(main())
```

## ⚙️ 配置认证

部分功能（高清下载、视频发布等）需要 B站登录凭据。支持三种配置方式：

### 方式一：环境变量（推荐）

```bash
export BILIBILI_SESSDATA="你的_sessdata"
export BILIBILI_BILI_JCT="你的_bili_jct"
export BILIBILI_BUVID3="你的_buvid3"
```

### 方式二：凭据文件

创建 `credentials.json`：

```json
{
  "sessdata": "你的_sessdata",
  "bili_jct": "你的_bili_jct",
  "buvid3": "你的_buvid3"
}
```

### 方式三：代码直接传入

```python
app = BilibiliAllInOne(
    sessdata="你的_sessdata",
    bili_jct="你的_bili_jct",
    buvid3="你的_buvid3",
)
```

> 💡 **如何获取 Cookie？** 登录 [bilibili.com](https://www.bilibili.com) → 按 F12 打开开发者工具 → Application → Cookies → 复制 `SESSDATA`、`bili_jct`、`buvid3` 的值。

---

## 📚 使用方式

### 命令行（CLI）

```bash
python main.py <模块名> <操作> [参数JSON]
```

### Python API

```python
import asyncio
from main import BilibiliAllInOne

app = BilibiliAllInOne()
result = asyncio.run(app.execute("模块名", "操作", 参数=值))
```

---

## 🔥 模块详解

### 1. 热门监控 (`hot_monitor`)

实时监控 B站热门视频与话题趋势。

| 操作 | 说明 | 参数 |
|---|---|---|
| `get_hot` | 获取热门视频列表 | `page`, `page_size` |
| `get_trending` | 获取热搜话题 | `limit` |
| `get_weekly` | 获取每周必看榜 | `number`（期数，可选） |
| `get_rank` | 获取分区排行榜 | `category`, `limit` |

**支持的分区：** `all`、`anime`、`music`、`dance`、`game`、`tech`、`life`、`food`、`car`、`fashion`、`entertainment`、`movie`、`tv`

```bash
# 获取前10个热门视频
python main.py hot_monitor get_hot '{"page_size": 10}'

# 获取游戏区排行榜
python main.py hot_monitor get_rank '{"category": "game", "limit": 10}'

# 获取本周必看
python main.py hot_monitor get_weekly

# 获取热搜话题
python main.py hot_monitor get_trending '{"limit": 5}'
```

```python
# Python API
result = await app.execute("hot_monitor", "get_hot", page_size=10)
result = await app.execute("hot_monitor", "get_rank", category="game", limit=10)
result = await app.execute("hot_monitor", "get_weekly")
result = await app.execute("hot_monitor", "get_trending", limit=5)
```

---

### 2. 视频下载 (`downloader`)

支持多清晰度、多格式下载，可批量操作。

| 操作 | 说明 | 参数 |
|---|---|---|
| `get_info` | 获取视频信息 | `url` |
| `get_formats` | 列出可用画质/格式 | `url` |
| `download` | 下载单个视频 | `url`, `quality`, `output_dir`, `format`, `page` |
| `batch_download` | 批量下载多个视频 | `urls`, `quality`, `output_dir`, `format` |

**清晰度选项：** `360p` · `480p` · `720p` · `1080p`（默认）· `1080p+` · `4k`

**格式选项：** `mp4`（默认）· `flv` · `mp3`（仅音频）

```bash
# 获取视频信息
python main.py downloader get_info '{"url": "BV1xx411c7mD"}'

# 下载 1080p MP4
python main.py downloader download '{"url": "BV1xx411c7mD", "quality": "1080p"}'

# 提取音频
python main.py downloader download '{"url": "BV1xx411c7mD", "format": "mp3"}'

# 批量下载
python main.py downloader batch_download '{"urls": ["BV1xx411c7mD", "BV1yy411c8nE"], "quality": "720p"}'
```

```python
# Python API
info = await app.execute("downloader", "get_info", url="BV1xx411c7mD")
result = await app.execute("downloader", "download", url="BV1xx411c7mD", quality="1080p")
result = await app.execute("downloader", "batch_download", urls=["BV1xx411c7mD", "BV1yy411c8nE"])
```

---

### 3. 数据追踪 (`watcher`)

追踪 B站和 YouTube 视频的互动数据，支持多视频对比。

| 操作 | 说明 | 参数 |
|---|---|---|
| `watch` | 获取视频详细信息 | `url` |
| `get_stats` | 获取当前互动数据 | `url` |
| `track` | 持续追踪数据变化 | `url`, `interval`（分钟）, `duration`（小时） |
| `compare` | 对比多个视频数据 | `urls` |

**支持平台：**
- **B站**：`https://www.bilibili.com/video/BVxxxxxx` 或 `BVxxxxxx`
- **YouTube**：`https://www.youtube.com/watch?v=xxxxx` 或 `https://youtu.be/xxxxx`

```bash
# 查看视频详情
python main.py watcher watch '{"url": "BV1xx411c7mD"}'

# 获取互动数据
python main.py watcher get_stats '{"url": "BV1xx411c7mD"}'

# 每30分钟追踪一次，持续12小时
python main.py watcher track '{"url": "BV1xx411c7mD", "interval": 30, "duration": 12}'

# 对比多个视频
python main.py watcher compare '{"urls": ["BV1xx411c7mD", "BV1yy411c8nE"]}'

# YouTube 视频也支持
python main.py watcher watch '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

```python
# Python API
stats = await app.execute("watcher", "get_stats", url="BV1xx411c7mD")
comparison = await app.execute("watcher", "compare", urls=["BV1xx411c7mD", "BV1yy411c8nE"])
youtube_info = await app.execute("watcher", "watch", url="https://youtu.be/dQw4w9WgXcQ")
```

---

### 4. 字幕提取 (`subtitle`)

下载和处理 B站视频字幕，支持多语言和多格式。

| 操作 | 说明 | 参数 |
|---|---|---|
| `list` | 列出可用字幕 | `url` |
| `download` | 下载字幕 | `url`, `language`, `format`, `output_dir` |
| `convert` | 转换字幕格式 | `input_path`, `output_format`, `output_dir` |
| `merge` | 合并多个字幕文件 | `input_paths`, `output_path`, `output_format` |

**支持格式：** `srt`（默认）· `ass` · `vtt` · `txt` · `json`

**支持语言：** `zh-CN`（默认）· `en` · `ja` 以及视频提供的其他语言

```bash
# 列出可用字幕
python main.py subtitle list '{"url": "BV1xx411c7mD"}'

# 下载中文字幕（SRT格式）
python main.py subtitle download '{"url": "BV1xx411c7mD", "language": "zh-CN", "format": "srt"}'

# 下载英文字幕（ASS格式）
python main.py subtitle download '{"url": "BV1xx411c7mD", "language": "en", "format": "ass"}'

# 格式转换：SRT → VTT
python main.py subtitle convert '{"input_path": "./subtitles/video.srt", "output_format": "vtt"}'

# 合并多个字幕
python main.py subtitle merge '{"input_paths": ["part1.srt", "part2.srt"], "output_path": "merged.srt"}'
```

```python
# Python API
subs = await app.execute("subtitle", "list", url="BV1xx411c7mD")
result = await app.execute("subtitle", "download", url="BV1xx411c7mD", language="zh-CN", format="srt")
result = await app.execute("subtitle", "convert", input_path="video.srt", output_format="vtt")
```

---

### 5. 视频播放 (`player`)

获取播放地址、弹幕数据和播放列表信息。

| 操作 | 说明 | 参数 |
|---|---|---|
| `play` | 获取完整播放信息 | `url`, `quality`, `page` |
| `get_playurl` | 获取直接播放地址 | `url`, `quality`, `page` |
| `get_danmaku` | 获取弹幕数据 | `url`, `page`, `segment` |
| `get_playlist` | 获取分P/播放列表信息 | `url` |

**弹幕类型：**

| 模式 | 说明 |
|:---:|---|
| 1 | 滚动弹幕（从右到左） |
| 4 | 底部固定弹幕 |
| 5 | 顶部固定弹幕 |

```bash
# 获取播放信息
python main.py player play '{"url": "BV1xx411c7mD", "quality": "1080p"}'

# 获取播放地址
python main.py player get_playurl '{"url": "BV1xx411c7mD", "quality": "720p"}'

# 获取弹幕
python main.py player get_danmaku '{"url": "BV1xx411c7mD"}'

# 获取分P列表
python main.py player get_playlist '{"url": "BV1xx411c7mD"}'

# 播放多P视频的第3P
python main.py player play '{"url": "BV1xx411c7mD", "quality": "1080p", "page": 3}'
```

```python
# Python API
play_info = await app.execute("player", "play", url="BV1xx411c7mD", quality="1080p")
danmaku = await app.execute("player", "get_danmaku", url="BV1xx411c7mD")
playlist = await app.execute("player", "get_playlist", url="BV1xx411c7mD")
```

---

### 6. 视频发布 (`publisher`)

上传视频到 B站，支持定时发布和草稿管理。

> ⚠️ **此模块所有操作均需要登录认证**

| 操作 | 说明 | 参数 |
|---|---|---|
| `upload` | 上传并发布视频 | `file_path`, `title`, `description`, `tags`, `category`, `cover_path` |
| `draft` | 保存为草稿 | `file_path`, `title`, `description`, `tags`, `category` |
| `schedule` | 定时发布 | `file_path`, `title`, `schedule_time`, `description`, `tags` |
| `edit` | 编辑已发布视频 | `bvid`, `title`, `description`, `tags`, `cover_path` |
| `delete` | 删除视频 | `bvid` |

**上传参数说明：**

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `file_path` | string | *必填* | 视频文件路径 |
| `title` | string | *必填* | 视频标题（最长 80 字） |
| `description` | string | `""` | 视频简介（最长 2000 字） |
| `tags` | string[] | `["bilibili"]` | 标签（最多 12 个，每个最长 20 字） |
| `category` | string | `"171"` | 分区 TID |
| `cover_path` | string | `null` | 封面图片路径（JPG/PNG） |
| `no_reprint` | int | `1` | 1=自制，0=转载 |
| `open_elec` | int | `0` | 1=开启充电，0=关闭 |

```bash
# 上传并发布
python main.py publisher upload '{"file_path": "./video.mp4", "title": "我的视频", "description": "Hello World", "tags": ["测试", "演示"]}'

# 保存为草稿
python main.py publisher draft '{"file_path": "./video.mp4", "title": "草稿视频"}'

# 定时发布
python main.py publisher schedule '{"file_path": "./video.mp4", "title": "定时视频", "schedule_time": "2025-12-31T20:00:00+08:00"}'

# 编辑视频信息
python main.py publisher edit '{"bvid": "BV1xx411c7mD", "title": "新标题", "tags": ["更新"]}'

# 删除视频
python main.py publisher delete '{"bvid": "BV1xx411c7mD"}'
```

```python
# Python API（需要认证）
app = BilibiliAllInOne(sessdata="xxx", bili_jct="xxx", buvid3="xxx")

result = await app.execute("publisher", "upload",
    file_path="./video.mp4",
    title="我的视频",
    description="通过 bilibili-all-in-one 发布",
    tags=["python", "bilibili"],
)
```

---

## 🔒 安全说明

### 凭据处理

| 关注点 | 说明 |
|---|---|
| **需要哪些凭据？** | `SESSDATA`、`bili_jct`、`buvid3` — B站浏览器 Cookie |
| **哪些功能需要认证？** | 视频发布（上传/编辑/删除/定时/草稿）、1080p+/4K 下载 |
| **哪些功能无需认证？** | 热门监控、标准画质下载、字幕获取、弹幕抓取、数据查看 |
| **凭据发送到哪里？** | **仅限** B站官方 API（`api.bilibili.com`、`member.bilibili.com`），全部 HTTPS |
| **是否持久化到磁盘？** | **否** — 除非你主动调用 `auth.save_to_file()`，凭据默认仅存在于内存 |
| **保存文件权限** | `0600`（仅所有者可读写） |

### 网络端点

| 域名 | 用途 |
|---|---|
| `api.bilibili.com` | 视频信息、统计、热门、字幕、弹幕、播放地址 |
| `member.bilibili.com` | 视频发布（上传、编辑、删除） |
| `upos-sz-upcdnbda2.bilivideo.com` | 视频文件上传 CDN |
| `www.bilibili.com` | 网页数据抓取备用 |
| `www.youtube.com` | YouTube 视频元数据获取（oEmbed API，无需认证） |

### 安全建议

1. 🧪 **使用测试账号** — 请勿使用主账号 Cookie 进行测试
2. 🔒 **优先使用内存凭据** — 通过环境变量或代码参数传入，避免保存到文件
3. 📁 **如需保存凭据** — 使用 `auth.save_to_file()`（自动设置 0600 权限），用完后及时删除
4. 🐳 **隔离运行** — 建议在容器/虚拟环境中运行，并监控网络流量
5. 🌐 **所有请求仅发往 B站官方域名**，无第三方遥测或数据收集
6. ❌ **本工具不会将你的凭据发送至任何非 B站的第三方服务**

---

## 📁 项目结构

```
bilibili-all-in-one/
├── skill.json                      # Skill 配置与参数 Schema
├── skill.md                        # Skill 英文文档
├── README.md                       # 中文说明文档（本文件）
├── requirements.txt                # Python 依赖
├── main.py                         # 入口文件，统一的 BilibiliAllInOne 类
├── src/
│   ├── __init__.py                 # 包导出
│   ├── auth.py                     # 认证与凭据管理
│   ├── utils.py                    # 共享工具函数、API 常量
│   ├── hot_monitor.py              # 🔥 热门监控模块
│   ├── downloader.py               # ⬇️ 视频下载模块
│   ├── watcher.py                  # 👀 数据追踪模块
│   ├── subtitle.py                 # 📝 字幕提取模块
│   ├── player.py                   # ▶️ 视频播放模块
│   └── publisher.py                # 📤 视频发布模块
└── tests/
    ├── __init__.py
    └── test_all_skill_examples.py  # 27 个完整测试用例
```

## 🧬 技能来源

本项目整合了以下 6 个独立 Skill 的功能：

| 原始 Skill | 来源 | 整合为 |
|---|---|---|
| bilibili-hot-monitor | [Jacobzwj/bilibili-hot-monitor](https://clawhub.ai/Jacobzwj/bilibili-hot-monitor) | `hot_monitor` |
| bililidownloader | [caiyundc880518/bililidownloader](https://clawhub.ai/caiyundc880518/bililidownloader) | `downloader` |
| bilibili-youtube-watcher | [donnycui/bilibili-youtube-watcher](https://clawhub.ai/donnycui/bilibili-youtube-watcher) | `watcher` |
| bilibili-subtitle-download-skill | [DavinciEvans/bilibili-subtitle-download-skill](https://clawhub.ai/DavinciEvans/bilibili-subtitle-download-skill) | `subtitle` |
| bilibili-player | [e421083458/bilibili-player](https://clawhub.ai/e421083458/bilibili-player) | `player` |
| bilibili-video-publish | [Johnnyxu820/bilibili-video-publish](https://clawhub.ai/Johnnyxu820/bilibili-video-publish) | `publisher` |

## 📦 统一返回格式

所有操作返回统一的 JSON 结构：

**成功：**

```json
{
  "success": true,
  "...": "操作相关的数据字段"
}
```

**失败：**

```json
{
  "success": false,
  "message": "错误描述信息"
}
```

## 🧪 运行测试

```bash
# 运行全部 27 个测试
python -m unittest tests.test_all_skill_examples -v
```

## 📄 许可证

[MIT](LICENSE)
