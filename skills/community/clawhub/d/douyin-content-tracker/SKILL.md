---
name: douyin-content-tracker
description: Scrapes Douyin creator videos, downloads audio (Playwright+ffmpeg with yt-dlp fallback), and transcribes with Whisper. Covers setup, daily tracking, cookie management, and troubleshooting.
---

# Douyin Content Tracker

通过 MediaCrawler 爬取抖音创作者视频，用 Playwright+ffmpeg 下载音频（被封锁时自动切换 yt-dlp），用 Whisper 进行语音识别转写。

## 快速开始

### 一键完整流程（推荐）

```bash
SKILL_DIR=$(python -c "import pathlib; print(pathlib.Path.home().rglob('douyin-content-tracker-skill/SKILL.md').__next__().parent)")
cd "$SKILL_DIR"

# 1. 采集最新 3 条视频
python scripts/track_latest.py --limit 3

# 2. 下载音频并转写（macOS）
export KMP_DUPLICATE_LIB_OK=TRUE
WHISPER_MODEL=small python scripts/extract_subtitle.py
```

---

## 首次设置

### 1. 安装 Python 依赖

```bash
cd $SKILL_DIR
pip install -r scripts/requirements.txt
pip install openai-whisper
python -m playwright install chromium

# yt-dlp（音频下载备用方案）
pip install yt-dlp
# 或
brew install yt-dlp
```

### 2. 安装 MediaCrawler

```bash
# macOS/Linux
git clone https://github.com/NanmiCoder/MediaCrawler ~/MediaCrawler
cd ~/MediaCrawler && pip install -r requirements.txt

# Windows
git clone https://github.com/NanmiCoder/MediaCrawler D:/MediaCrawler
cd D:/MediaCrawler && pip install -r requirements.txt
```

### 3. 配置 `.env`

```bash
cd $SKILL_DIR
cp .env.template .env
```

编辑 `.env`：
```dotenv
# 必填：MediaCrawler 路径
MEDIACRAWLER_DIR=~/MediaCrawler

# 可选：输出目录（默认 ~/DouyinContentTracker）
OUTPUT_BASE_DIR=~/DouyinContentTracker

# 可选：Whisper 模型（推荐 small，更快更稳定）
WHISPER_MODEL=small
```

### 4. 添加目标账号

编辑 `accounts.txt`：
```
博主名称 | https://www.douyin.com/user/MS4wLjABAAAA...
```

### 5. 获取 Cookie（三选一）

**方法 A：扫码登录（生成新 Cookie）**
```bash
cd $SKILL_DIR
python scripts/scrape_profile.py
```

**方法 B：复制微信 Cookie（macOS）**
```bash
cp ~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/*/msg/file/*/.douyin_cookies.json \
   $SKILL_DIR/.douyin_cookies.json
chmod 600 $SKILL_DIR/.douyin_cookies.json
```

**方法 C：使用已有 Cookie**
确保 `.douyin_cookies.json` 在 skill 目录下。

---

## 日常使用

### 采集 + 转写（标准流程）

```bash
cd $SKILL_DIR

# 1. 采集（默认 3 条）
python scripts/track_latest.py

# 2. 清洗数据
python scripts/clean_data.py

# 3. 下载音频
python scripts/download_video.py

# 4. 语音识别（macOS 需要设置环境变量）
export KMP_DUPLICATE_LIB_OK=TRUE
python scripts/extract_subtitle.py
```

### 常用命令

```bash
# 采集指定数量
python scripts/track_latest.py --limit 5

# 使用自定义账号列表
python scripts/track_latest.py --accounts-file /path/to/accounts.txt

# 仅采集数据（不下载音频）
python scripts/track_latest.py --no-audio

# 仅转写（跳过下载）
export KMP_DUPLICATE_LIB_OK=TRUE
python scripts/extract_subtitle.py
```

---

## 故障排查

### ❌ 0 视频提取 / "未获取到视频 URL"

**原因：** Cookie 过期或无效，或抖音 API 封锁了 Playwright 请求

**解决：**
```bash
# 1. 检查 Cookie 文件
ls -la .douyin_cookies.json

# 2. 复制新 Cookie（方法 B）
cp ~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/*/msg/file/*/.douyin_cookies.json \
   $SKILL_DIR/.douyin_cookies.json

# 3. 或重新扫码
python scripts/scrape_profile.py

# 4. 重试下载（Playwright 失败时自动切换 yt-dlp）
python scripts/download_video.py
```

### ❌ yt-dlp 也被拦截

```bash
# 带浏览器 Cookie 重试
yt-dlp -x --audio-format m4a --cookies-from-browser chrome <视频链接>
```

如果 Chrome Cookie 有效，在 `download_video.py` 的 `ytdlp_download_audio` 函数中的 `cmd` 列表里加入：
```python
"--cookies-from-browser", "chrome",
```

### ❌ Whisper 崩溃（SIGSEGV / OpenMP 错误）

**原因：** macOS OpenMP 运行时冲突

**解决：**
```bash
export KMP_DUPLICATE_LIB_OK=TRUE
WHISPER_MODEL=small python scripts/extract_subtitle.py
```

**永久解决：** 在 `.env` 中设置 `WHISPER_MODEL=small`

### ❌ Playwright 浏览器缺失

```bash
python -m playwright install chromium
```

### ❌ Cookie 警告 "已 N 天未更新"

```bash
python scripts/scrape_profile.py  # 重新扫码
```

---

## 输出目录结构

```
~/DouyinContentTracker/
├── data/                           # 采集数据
│   ├── 周凯谈烘焙_20260321_083047.csv
│   └── cleaned_周凯谈烘焙_20260321_083047.csv
├── audio/                          # 音频文件
│   └── 周凯谈烘焙/
│       ├── 7559900409483300105.m4a    (96 KB)
│       ├── 7491508890513886505.m4a    (584 KB)
│       └── 7446734179963866379.m4a    (1,775 KB)
├── subtitles/                      # 语音转写文稿
│   └── 周凯谈烘焙/
│       ├── 7559900409483300105.md
│       ├── 7491508890513886505.md
│       └── 7446734179963866379.md
└── models/                         # Whisper 模型
    └── small.pt
```

---

## 执行报告模板

每一步完成后向用户报告进度：

| 步骤 | 报告内容 |
|------|----------|
| 采集 | 博主名称、采集条数、失败原因 |
| 清洗 | 有效数据条数、输出文件 |
| 音频 | 成功数/总数、跳过条数 |
| 转写 | 生成字幕数、输出路径 |
| 完成 | 博主数、视频数、字幕数、输出目录 |

**示例：**
```
[步骤 1/4 采集] 博主「周凯谈烘焙」— 采集完成，共 345 条视频
[步骤 2/4 清洗] 有效数据 115 条 → data/cleaned_周凯谈烘焙_20260321_083047.csv
[步骤 3/4 音频] 下载完成 3/3 → audio/周凯谈烘焙/
[步骤 4/4 字幕] 生成 3 个字幕文件 → subtitles/周凯谈烘焙/
[完成] 1 位博主 · 3 条视频 · 3 个字幕，输出目录：~/DouyinContentTracker
```

---

## 技术细节

### 管道流程

```
accounts.txt
    ↓
scrape_profile.py → MediaCrawler (CDP) → data/*.csv
    ↓
clean_data.py → cleaned_*.csv
    ↓
download_video.py → Playwright + ffmpeg → audio/{blogger}/*.m4a
                 ↘ (Playwright 失败) yt-dlp ↗
    ↓
extract_subtitle.py → Whisper → subtitles/{blogger}/{video_id}.md
```

**音频下载双重策略：**
- **主路径**：Playwright 打开视频页拦截 aweme API 拿真实 URL → ffmpeg 提取 `.m4a`
- **备用路径**：Playwright 拿不到 URL 时，自动调用 `yt-dlp -x --audio-format m4a`，输出同样是 `.m4a`，Whisper 无需适配

### Whisper 模型选择

| 模型 | 大小 | 速度 | 准确度 | 推荐场景 |
|------|------|------|--------|----------|
| tiny | 75MB | 最快 | 一般 | 测试/快速预览 |
| small | 461MB | 快 | 好 | **日常使用（推荐）** |
| medium | 1.5GB | 慢 | 很好 | 高准确度需求 |
| large | 3GB | 最慢 | 最佳 | 专业转写 |

---

## 参考文件

调试或扩展时加载：

- `references/pipeline.md` — 脚本技术细节、数据格式、关键函数
- `references/troubleshooting.md` — Cookie、MediaCrawler、ffmpeg、Whisper、数据错误修复

---

## 更新日志

**2026-03-21（二次更新）**
- ✅ 新增 yt-dlp 作为音频下载备用方案（Playwright 被封锁时自动切换）
- ✅ yt-dlp 输出保持 `.m4a` 格式，Whisper 管道无需改动
- ✅ 新增 `--cookies-from-browser chrome` 故障排查说明

**2026-03-21**
- ✅ 新增 macOS 微信 Cookie 复制方法
- ✅ 新增 OpenMP 冲突解决方案（`KMP_DUPLICATE_LIB_OK=TRUE`）
- ✅ 推荐使用 `small` 模型（更快更稳定）
- ✅ 新增一键完整流程示例
- ✅ 新增输出目录结构示例
- ✅ 新增执行报告模板
