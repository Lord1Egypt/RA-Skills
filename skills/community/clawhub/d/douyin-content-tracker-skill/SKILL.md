---
name: douyin-content-tracker
description: This skill should be used when the user wants to scrape Douyin (TikTok China) creator content, download audio, and transcribe it with Whisper. Covers first-time setup, daily incremental tracking, cookie refresh, and debugging. All pipeline scripts are bundled in this skill directory and can be run directly without any extra installation beyond pip and MediaCrawler.
---

# Douyin Content Tracker

Scrapes Douyin creator videos via MediaCrawler, downloads audio with ffmpeg, and transcribes speech with Whisper.

## Finding the Skill Base Directory

All commands must run from this skill's directory. To locate it, run:

```bash
python -c "import pathlib; print([p for p in pathlib.Path.home().rglob('douyin-content-tracker-skill/SKILL.md')])"
```

Or check common locations:
- `~/.claude/skills/douyin-content-tracker-skill/`
- The path shown when the skill was installed

Set it as a variable for convenience:
```bash
SKILL_DIR="~/.claude/skills/douyin-content-tracker-skill"   # adjust to actual path
cd "$SKILL_DIR"
```

---

## First-Time Setup

Run these steps once on a new machine.

### 1. Install Python dependencies

```bash
cd $SKILL_DIR
pip install -r scripts/requirements.txt
python -m playwright install chromium
```

### 2. Install MediaCrawler

```bash
# Windows
git clone https://github.com/NanmiCoder/MediaCrawler D:/MediaCrawler
cd D:/MediaCrawler && pip install -r requirements.txt

# macOS/Linux
git clone https://github.com/NanmiCoder/MediaCrawler ~/MediaCrawler
cd ~/MediaCrawler && pip install -r requirements.txt
```

### 3. Configure `.env`

```bash
cd $SKILL_DIR
cp .env.template .env
```

Edit `.env` — required field:
```dotenv
MEDIACRAWLER_DIR=D:/MediaCrawler    # adjust to actual MediaCrawler path (use ~/MediaCrawler on macOS/Linux)
```

Optional overrides:
```dotenv
# Where to store data/audio/subtitles/models (default: ~/DouyinContentTracker or %USERPROFILE%\DouyinContentTracker)
OUTPUT_BASE_DIR=/Users/me/DouyinContentTracker

# Whisper model size (default: medium)
WHISPER_MODEL=small
```

### 4. Add target accounts

Edit `accounts.txt` (or set `TRACKER_ACCOUNTS_FILE` / pass `--accounts-file` when running):
```
博主名称 | https://www.douyin.com/user/MS4wLjABAAAA...
```

### 5. First login (generates cookie)

```bash
cd $SKILL_DIR
python scripts/scrape_profile.py
```

A browser opens — scan the Douyin QR code to log in. Cookie is saved to `.douyin_cookies.json`.

---

## Daily Usage

```bash
cd $SKILL_DIR

# Track latest 3 videos per account (default). main.py mirrors track_latest.py
python scripts/track_latest.py
# or
python scripts/main.py

# Track latest N videos
python scripts/track_latest.py --limit 5

# Use a custom account list (also works via env TRACKER_ACCOUNTS_FILE)
python scripts/track_latest.py --accounts-file /path/to/accounts.txt

# Skip audio download and transcription (data only)
python scripts/track_latest.py --no-audio
```

---

## Cookie Refresh

When scraping returns 0 videos or warns "Cookie 已 N 天未更新":

```bash
cd $SKILL_DIR
python scripts/scrape_profile.py    # opens browser, scan QR
```

---

## Pipeline Flow

```
accounts.txt (or the list pointed by --accounts-file / TRACKER_ACCOUNTS_FILE)
    ↓
scripts/scrape_profile.py   → MediaCrawler (CDP) → OUTPUT_BASE_DIR/data/*.csv
    ↓
scripts/clean_data.py       → normalized OUTPUT_BASE_DIR/data/cleaned_*.csv
    ↓
scripts/download_video.py   → Playwright + ffmpeg → OUTPUT_BASE_DIR/audio/{blogger}/*.m4a
    ↓
scripts/extract_subtitle.py → Whisper → OUTPUT_BASE_DIR/subtitles/{blogger}/{video_id}.md
```

## Output Locations

All generated files live under `OUTPUT_BASE_DIR` (defaults to `~/DouyinContentTracker` on macOS/Linux, `%USERPROFILE%\DouyinContentTracker` on Windows).

| Subdir | Contents |
|--------|----------|
| `data/cleaned_*.csv` | Scraped + normalized video metadata |
| `audio/{blogger}/{video_id}.m4a` | Extracted audio |
| `subtitles/{blogger}/{video_id}.md` | Whisper transcript (title as first line) |
| `subtitles/{blogger}.md` | All transcripts for one blogger merged |

---

## Execution Logging Guide

When running the pipeline, report progress to the user after each step completes. Do not wait until the entire pipeline finishes.

**Step-by-step reporting template:**

After each Bash tool call returns, immediately tell the user:

| Step | What to report |
|------|---------------|
| 采集（scrape） | 博主名称、采集到的视频条数，若失败注明原因 |
| 清洗（clean） | 清洗后有效条数 |
| 音频下载（download） | 成功下载的音频数 / 总数，跳过的条数 |
| 语音识别（whisper） | 生成的字幕文件数，输出路径 |
| 完成 | 汇总：共处理博主数、视频数、生成字幕数，以及输出目录路径 |

**If a step fails**, stop the pipeline, report the error output verbatim, and suggest the matching fix from `references/troubleshooting.md` before asking the user whether to continue.

**Example output style:**

```
[步骤 1/4 采集] 博主「某某」— 采集完成，共 10 条视频
[步骤 2/4 清洗] 有效数据 10 条 → data/cleaned_profile_xxx.csv
[步骤 3/4 音频] 下载完成 8/10（2 条无音频流，已跳过）
[步骤 4/4 字幕] 生成 8 个字幕文件 → subtitles/某某/
[完成] 1 位博主 · 10 条视频 · 8 个字幕，输出目录：~/DouyinContentTracker
```

---

## References

Load these files into context when debugging or extending the pipeline:

- `references/pipeline.md` — per-script technical breakdown, data schemas, key function signatures
- `references/troubleshooting.md` — fixes for cookie, MediaCrawler, ffmpeg, Whisper, and data errors
