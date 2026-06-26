# Douyin Content Tracker

抖音博主内容追踪工具，自动采集视频、提取音频并完成语音转文字。

## 功能概览

- 通过 MediaCrawler 采集抖音博主主页视频元数据
- 使用 ffmpeg 下载并提取音频
- 使用 Whisper 语音识别生成字幕

## 环境要求

- Python 3.9+
- ffmpeg（由 `imageio-ffmpeg` 自动管理）
- [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler)

## 快速开始

### 1. 安装依赖

```bash
pip install -r scripts/requirements.txt
python -m playwright install chromium
```

### 2. 安装 MediaCrawler

```bash
# Windows
git clone https://github.com/NanmiCoder/MediaCrawler D:/MediaCrawler
cd D:/MediaCrawler && pip install -r requirements.txt

# macOS/Linux
git clone https://github.com/NanmiCoder/MediaCrawler ~/MediaCrawler
cd ~/MediaCrawler && pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.template .env
```

编辑 `.env`，至少填写：

```dotenv
MEDIACRAWLER_DIR=D:/MediaCrawler    # MediaCrawler 实际路径（macOS/Linux 可用 ~/MediaCrawler）
```

可选：

```dotenv
# 输出目录根路径，默认：macOS/Linux → ~/DouyinContentTracker，Windows → %USERPROFILE%/DouyinContentTracker
OUTPUT_BASE_DIR=/Users/me/DouyinContentTracker

# 调整 Whisper 模型大小（默认 `medium`）
WHISPER_MODEL=small
```

### 4. 添加追踪账号

编辑 `accounts.txt`，或在运行时通过 `--accounts-file` / `TRACKER_ACCOUNTS_FILE` 指定其他列表，每行一个账号：

```
博主名称 | https://www.douyin.com/user/MS4wLjABAAAA...
```

### 5. 首次登录（生成 Cookie）

```bash
python scripts/scrape_profile.py
```

浏览器会自动打开，扫码登录抖音，Cookie 保存至 `.douyin_cookies.json`。

---

## 日常使用

```bash
# 追踪每个账号最新 3 条视频（默认），main.py 与 track_latest.py 等效
python scripts/track_latest.py
# 或
python scripts/main.py

# 追踪最新 N 条视频
python scripts/track_latest.py --limit 5

# 自定义账号列表文件
python scripts/track_latest.py --accounts-file /path/to/accounts.txt
# 亦可在运行前设置：export TRACKER_ACCOUNTS_FILE=/path/to/accounts.txt

# 仅采集数据，跳过音频下载和转录
python scripts/track_latest.py --no-audio

## Cookie 失效处理

当采集返回 0 条视频，或提示"Cookie 已 N 天未更新"时：

```bash
python scripts/scrape_profile.py    # 打开浏览器，重新扫码登录
```

---

## 流程说明

```
accounts.txt（或 --accounts-file 指定的列表）
    ↓
scripts/scrape_profile.py   → MediaCrawler (CDP) → OUTPUT_BASE_DIR/data/*.csv
    ↓
scripts/clean_data.py       → 标准化数据 → OUTPUT_BASE_DIR/data/cleaned_*.csv
    ↓
scripts/download_video.py   → Playwright + ffmpeg → OUTPUT_BASE_DIR/audio/{blogger}/*.m4a
    ↓
scripts/extract_subtitle.py → Whisper → OUTPUT_BASE_DIR/subtitles/{blogger}/{video_id}.md
```

## 输出目录

所有输出文件统一保存在 `OUTPUT_BASE_DIR`（默认：macOS/Linux → `~/DouyinContentTracker`，Windows → `%USERPROFILE%\DouyinContentTracker`）。

| 子目录 | 内容 |
|--------|------|
| `data/cleaned_*.csv` | 采集并标准化的视频元数据 |
| `audio/{blogger}/{video_id}.m4a` | 提取的音频文件 |
| `subtitles/{blogger}/{video_id}.md` | Whisper 转录文本（首行为标题） |
| `subtitles/{blogger}.md` | 单个博主所有转录文本合并文件 |

## 参考文档

- `references/pipeline.md` — 各脚本技术细节、数据结构、关键函数说明
- `references/troubleshooting.md` — Cookie、MediaCrawler、ffmpeg、Whisper 等常见问题排查
- `SKILL.md` — Claude Code Skill 使用说明
