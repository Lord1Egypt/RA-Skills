# Pipeline Reference

## Module Map

| Script | Entry Point | Called by |
|--------|-------------|-----------|
| `main.py` | CLI wrapper → `track_latest.run_pipeline()` | CLI users |
| `track_latest.py` | `run_pipeline(limit, skip_audio, accounts_file)` | CLI users, `main.py` |
| `scrape_profile.py` | `scrape(url, limit)` async | `scripts/track_latest.py` |
| `clean_data.py` | `clean_csv(filepath)` | `scripts/track_latest.py` |
| `download_video.py` | `download_all(records)` async | `scripts/track_latest.py` |
| `extract_subtitle.py` | `run()` / `process_video(path, title_map, summary_index)` | `scripts/track_latest.py` |
| `run_state.py` | `write_current_run()`, `resolve_cleaned_files()` | all scripts |
| `storage.py` | `OUTPUT_BASE_DIR`, `DATA_DIR`, `AUDIO_DIR`, `SUBTITLE_DIR`, `MODEL_DIR` | all scripts |
| `utils.py` | `video_id_from_url()`, `compute_engagement_rate()` | all scripts |
| `utils_platform.py` | `platform_defaults()` | `scrape_profile.py` |

> All persistent outputs (data/audio/subtitles/models) live under `OUTPUT_BASE_DIR` — defaults to `~/DouyinContentTracker` on macOS/Linux and `%USERPROFILE%\DouyinContentTracker` on Windows unless overridden in `.env`.

---

## track_latest.py & main.py

**Purpose:** end-to-end orchestration for every tracked account (scrape → clean → download audio → Whisper).

**CLI options:**
- `--limit` — videos per account (auto bumps to 10 when no historical `cleaned_*.csv` exists)
- `--no-audio` — run only scrape + clean
- `--accounts-file` / `TRACKER_ACCOUNTS_FILE` — override `accounts.txt` without editing the repo copy

`main.py` simply delegates to `track_latest.parse_args()` + `run_pipeline()` so both entry points stay aligned.

---

## Step 1 — scrape_profile.py

**What it does:** Calls MediaCrawler (subprocess, CDP mode) to scrape a creator's homepage.
Converts the output JSONL to a CSV in `data/`.

**Key logic:**
- `set_mediacrawler_max_count(n)` — temporarily patches `MEDIACRAWLER_CFG` (`config/base_config.py`), restores in `finally`
- `MEDIACRAWLER_CFG = MEDIACRAWLER_DIR / "config" / "base_config.py"` — module-level constant
- Uses `before`/`after` set-difference to identify only new JSONL files from this run
- Trims results to `--limit` after scraping (fetches `limit * 2` to compensate for filtering)

**Output CSV columns:**
`博主昵称, 视频标题, 视频链接, 播放量(空), 点赞数, 评论数, 转发数, 收藏数, 发布时间, 采集时间`

**Note:** `播放量` is empty at this stage — filled in by `download_video.py`.

---

## Step 2 — clean_data.py

**What it does:** Normalizes raw CSVs — column remapping, number parsing, time parsing, dedup.

**Column mapping strategy:**
1. Exact match via `EXACT_COLUMN_MAP` dict
2. Fuzzy keyword match via `FUZZY_COLUMN_MAP` (only for columns not already found)

**`ensure_core_schema(df)`** — raises `ValueError` if `["链接", "标题", "博主", "发布时间"]` are missing. Callers (`track_latest.py`, `run()`) must catch `ValueError`.

**`clean_number(val)`** — handles `1.2万`, `3.4w`, `2k`, `1,234`, `暂无`, `--` etc.

**`parse_publish_time(val)`** — handles relative times (`3分钟前`, `昨天 14:30`), short dates (`03-21`), Chinese dates (`2024年3月21日`).

**Engagement rate formula:**
```python
互动率 = (点赞 + 评论 + 转发) / max(播放, 1) * 100   # rounded to 2dp
```
Computed via `utils.compute_engagement_rate(df)`.

**Output:** `data/cleaned_{original_stem}.csv`

---

## Step 3 — download_video.py

**What it does:** Opens each video page in headless Playwright, intercepts the
`/aweme/v1/web/aweme/detail` API response to get the CDN video URL + real statistics,
then calls `ffmpeg -vn -acodec copy` to extract audio-only `.m4a`.

**`fetch_detail(page, url, expected_video_id)`:**
- Intercepts API response, validates `aweme_id == expected_video_id` to prevent data cross-binding
- Waits up to 10s; if no data, reloads once and waits another 10s
- Returns `(cdn_url, meta_dict)` — meta includes `点赞, 评论, 转发, 收藏, 播放, 发布时间`

**`extract_audio(video_url, save_path, retries=3)`:**
- Uses `ffmpeg -headers ... -i url -vn -acodec copy -y out.m4a`
- Checks **both** `returncode == 0` and file size > 1000 bytes
- Retries up to 3 times with 2s/4s back-off
- **ffmpeg resolution** (`_get_ffmpeg()`): system PATH → imageio-ffmpeg fallback; on Windows copies to plain `ffmpeg.exe`

**Rate limiting:**
- Random 1.5–3.5s per video
- Extra 8–15s pause every 10 videos

**Download log:** `audio/downloaded.txt` — one video ID per line; auto-heals if log says downloaded but file is missing.

**Output:** `audio/{博主}/{video_id}.m4a` + `data/cleaned_combined_{run_id}.csv` for the current run (temporary `cleaned_*.csv` inputs are only deleted when `_current_run.json` still points to them).

---

## Step 4 — extract_subtitle.py

**What it does:** Runs Whisper on every `.m4a` in `audio/`, saves transcriptions as Markdown.
Also builds a per-blogger summary file.

**`load_title_map()`** — vectorized: reads cleaned CSVs, extracts `video_id → (title, blogger)`.

**`process_video(audio_path, title_map, summary_index)`:**
- Derives `video_id = audio_path.stem`
- Looks up `(title, blogger)` from `title_map`
- Output path: `subtitles/{blogger}/{video_id}.md` (title written as first line `# {title}` inside the file)
- Skips if output already exists (incremental)
- Appends `(safe_title, out_path)` to `summary_index[blogger]`

**`write_blogger_summaries(summary_index)`** — writes `subtitles/{blogger}.md` containing all video scripts.

**`sanitize_filename(name)`** — strips `\/:*?"<>|`, collapses whitespace, truncates to 150 chars.

**Model loading:** Singleton `_whisper_model`; downloads to `models/{model}.pt` on first run.

---

## run_state.py — Run Isolation

Prevents cross-run data contamination when multiple runs exist on disk.

**`RUN_ID`** env var — set by `track_latest.py` at pipeline start; format `YYYYMMDD_HHMMSS`.

**`write_current_run(run_id, csv_paths)`** — saves `_current_run.json` in `OUTPUT_BASE_DIR/data/`.
Warns (does not silently drop) if a registered file does not exist.

**`resolve_cleaned_files()`** — returns:
1. Files listed in `_current_run.json` if `RUN_ID` matches, **or**
2. Fallback: all `OUTPUT_BASE_DIR/data/cleaned_*.csv` sorted by mtime (newest first)

## Directory Structure

```
douyin-content-tracker-skill/       ← project root (code + configs)
├── SKILL.md
├── scripts/requirements.txt
├── .env / .env.template
├── .douyin_cookies.json
├── accounts.txt
└── scripts/
    ├── main.py                    # full pipeline (bulk / first run)
    ├── track_latest.py            # incremental tracking (daily use)
    ├── scrape_profile.py
    ├── clean_data.py
    ├── download_video.py
    ├── extract_subtitle.py
    ├── run_state.py
    ├── storage.py
    ├── utils.py
    └── utils_platform.py

OUTPUT_BASE_DIR/                ← configurable output root (default: ~/DouyinContentTracker)
├── data/
│   ├── {博主}_{ts}.csv        # raw scrape output
│   ├── cleaned_{stem}.csv     # after clean_data.py
│   ├── cleaned_combined_{ts}.csv  # merged after download_video.py (multi-account)
│   └── _current_run.json      # run-state file
├── audio/
│   ├── {博主}/{video_id}.m4a
│   └── downloaded.txt
├── subtitles/
│   ├── {博主}/{video_id}.md   # transcript; first line is "# {title}"
│   └── {博主}.md              # per-blogger summary (all videos merged)
└── models/
    └── medium.pt              # Whisper model cache
```
