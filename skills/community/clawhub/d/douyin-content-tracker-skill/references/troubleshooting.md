# Troubleshooting Reference

## Cookie Issues

### Symptom: "未找到 Cookie 文件，将使用扫码登录"
Cookie file `.douyin_cookies.json` does not exist.
```bash
# Run once interactively to scan QR and save cookie
python scripts/scrape_profile.py
```

### Symptom: "Cookie 已 N 天未更新"
Cookie is older than 20 days (valid ~7–30 days).
```bash
python scripts/scrape_profile.py   # browser pops up, scan QR
```

### Symptom: Scrape returns 0 videos / empty JSONL
Cookie has expired silently. Re-login:
```bash
python scripts/scrape_profile.py
```
Then re-run the pipeline.

---

## MediaCrawler Issues

### Symptom: `FileNotFoundError: MediaCrawler 路径无效`
MediaCrawler is not installed or `MEDIACRAWLER_DIR` points to the wrong path.

**Fix:**
1. Install MediaCrawler: `git clone https://github.com/NanmiCoder/MediaCrawler D:/MediaCrawler`
2. Install its deps: `cd D:/MediaCrawler && pip install -r requirements.txt`
3. Set path in `.env`: `MEDIACRAWLER_DIR=D:/MediaCrawler`

On macOS/Linux the default path is `~/MediaCrawler`. Override via `.env` if installed elsewhere.

### Symptom: MediaCrawler exits non-zero / prints errors
Check the last 15 lines printed by the pipeline — `scrape_profile.py` captures and prints them.

Common causes:
- Python version mismatch (MediaCrawler requires Python 3.9+)
- Missing MediaCrawler dependencies
- Anti-bot detection triggered (try adding `--limit` to reduce scrape volume)

---

## ffmpeg Issues

### Symptom: `ffmpeg 退出码 1` or audio file missing
- CDN URL may have expired (Douyin URLs have short TTLs)
- Network timeout — `extract_audio` retries 3× automatically
- If persistent: check that ffmpeg is callable (`ffmpeg -version` in terminal)

### Symptom: ffmpeg not found
The pipeline resolves ffmpeg in this order:
1. System `PATH` (`shutil.which("ffmpeg")`)
2. `imageio-ffmpeg` bundled binary (auto-copied to `ffmpeg.exe` on Windows)

To install system ffmpeg:
- Windows: `winget install ffmpeg` or download from ffmpeg.org
- macOS: `brew install ffmpeg`
- Linux: `apt install ffmpeg`

---

## Whisper Issues

### Symptom: `Whisper 加载失败` / model won't load
Model file may be corrupted (partial download). Delete and re-download:
```bash
del "models\medium.pt"     # Windows
rm models/medium.pt        # macOS/Linux
python scripts/extract_subtitle.py   # re-downloads automatically
```

### Symptom: Transcription is very slow
Switch to the smaller model in `.env`:
```dotenv
WHISPER_MODEL=small   # 461MB vs 1.5GB, faster but less accurate
```

### Symptom: `fp16=False` warning on CPU
Expected — Whisper defaults to float16 (GPU), code sets `fp16=False` for CPU compatibility. Not an error.

---

## Data / Pipeline Issues

### Symptom: `缺少关键字段` ValueError from clean_data.py
The CSV is missing `链接`, `标题`, `博主`, or `发布时间`.
- Check column names in raw CSV against `EXACT_COLUMN_MAP` in `clean_data.py`
- Add the missing mapping to `EXACT_COLUMN_MAP` or `FUZZY_COLUMN_MAP`

### Symptom: 播放量 stays 0 after pipeline
`download_video.py` fills in `播放量`. If skipped (`--no-audio`) or all videos failed API interception, it stays 0.
- Check `audio/downloaded.txt` — if video IDs are there, audio was fetched
- A 0 play count means the API response was not captured; try re-running `download_video.py` standalone

### Symptom: Results from old runs appear in new report
The `run_state.py` module isolates runs via `RUN_ID`. If `_current_run.json` is stale or `RUN_ID` env var is unset, `resolve_cleaned_files()` falls back to all `cleaned_*.csv` files sorted by mtime.

Fix: delete old `cleaned_*.csv` files in `data/`, or re-run `track_latest.py` (sets `RUN_ID` automatically).

### Symptom: `subtitles/` files from this run are skipped
`extract_subtitle.py` skips files that already exist on disk.
To re-transcribe: delete the relevant `.md` file in `subtitles/{blogger}/`.

---

## Environment Setup Checklist

```bash
# 1. Python deps
cd {skill_base_dir}
pip install -r scripts/requirements.txt
python -m playwright install chromium

# 2. .env
cp .env.template .env
# Edit .env:
#   MEDIACRAWLER_DIR=D:/MediaCrawler           # adjust to actual path
#   OUTPUT_BASE_DIR=/Users/me/DouyinContentTracker  # optional storage root
#   WHISPER_MODEL=small                        # optional override (default: medium)

# 3. MediaCrawler
git clone https://github.com/NanmiCoder/MediaCrawler D:/MediaCrawler
cd D:/MediaCrawler && pip install -r requirements.txt

# 4. First login (generates .douyin_cookies.json)
cd {skill_base_dir}
python scripts/scrape_profile.py   # scan QR in browser

# 5. Add accounts
# Edit accounts.txt:
#   博主名 | https://www.douyin.com/user/...

# 6. Run
python scripts/track_latest.py
```
