---
name: bilibili-video-search-and-download
description: >
  Search and download Bilibili videos using yt-dlp and httpx.
  Use this skill whenever the user wants to search Bilibili for videos by keyword,
  retrieve video metadata (title, author, play count, duration, BV号),
  download Bilibili videos, or save search results to a JSON file.
  Also triggers when the user mentions "bilibili search", "bilibili download",
  "B站搜索", "b站视频搜索", "b站下载",
  or wants to find/download Bilibili content programmatically via Python.
---

# Bilibili Video Search

Use the `bilibili-api-python` library to search Bilibili videos by keyword and save results to `search.json`.

## Environment Checks (Prerequisites)

Before running any search script, perform these checks:

### 1. Python availability
```bash
python3 --version
```

### 2. Virtual environment & dependencies

macOS may block system-wide `pip install` due to PEP 668. Always use a venv:

```bash
# Create venv if it doesn't exist
python3 -m venv /tmp/bilibili_venv

# Install dependencies (search)
/tmp/bilibili_venv/bin/pip install bilibili-api-python httpx

# Install dependencies (download)
/tmp/bilibili_venv/bin/pip install yt-dlp

# Fallback: if lxml download fails (common on slow networks), use douban mirror
/tmp/bilibili_venv/bin/pip install yt-dlp -i https://pypi.doubanio.com/simple/
```

Also ensure `ffmpeg` is installed (required for merging audio/video streams):

```bash
ffmpeg -version
# If not installed: brew install ffmpeg
```

### 3. Import check

Verify the library works:

```bash
/tmp/bilibili_venv/bin/python3 -c "import httpx; print('httpx OK')"
```

If `bilibili_api` is also available:
```bash
/tmp/bilibili_venv/bin/python3 -c "from bilibili_api import search; print('bilibili_api OK')"
```

### 4. Network check

Ensure Bilibili API is reachable:

```bash
curl -s -o /dev/null -w "%{http_code}" "https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword=test"
```

Expected: `200`

> **Note**: If `bilibili-api-python` is unavailable (e.g. `lxml` fails to download), fall back to calling the Bilibili REST API directly with `httpx` — see the example script below.

## Core API

```python
from bilibili_api import search

results = await search.search_by_type(
    keyword="关键词",
    search_type=search.SearchObjectType.VIDEO,
    page=1,
    page_size=20,
)
```

The response is a dict with a `"result"` key containing a list of video dicts.

## Key Fields in Each Result

| Field      | Description              | Example                        |
|------------|--------------------------|--------------------------------|
| `bvid`     | BV号                     | `"BV1uv411q7Mv"`              |
| `title`    | 标题（含 `<em>` 高亮标签）  | `"【黑神话】..."`              |
| `author`   | UP主名                   | `"萌宠教主"`                   |
| `play`     | 播放量                   | `8838288`                      |
| `duration` | 时长（mm:ss 或秒）        | `"2:51"`                       |
| `pic`      | 封面图 URL               | `"http://i2.hdslb.com/..."`   |
| `pubdate`  | 发布时间戳               | `1595203214`                   |

## Sorting & Filtering

```python
from bilibili_api.search import OrderVideo

await search.search_by_type(
    keyword="黑神话",
    search_type=search.SearchObjectType.VIDEO,
    order_type=OrderVideo.CLICK,       # 按播放量排序
    order_sort=0,                       # 0=降序, 1=升序
    time_range=7,                       # 7天内, -1=全部
    page=1,
    page_size=42,
)
```

`OrderVideo` options:
- `CLICK` — 播放量
- `PUBDATE` — 发布日期
- `DANMAKU` — 弹幕数
- `STOW` — 收藏数
- `SCORE` — 评分

## HTML Tags Cleanup

Bilibili titles contain `<em class="keyword">` highlight tags. Strip them:

```python
title = v.get("title", "").replace("<em class=\"keyword\">", "").replace("</em>", "")
```

## Save Results to JSON

Always save results to `search.json` with this structure:

```json
{
  "keyword": "黑神话",
  "timestamp": "2026-05-27T23:31:55",
  "total": 20,
  "videos": [
    {
      "bvid": "BV1yup4ewEKz",
      "title": "【黑神话】...",
      "author": "萌宠教主",
      "play": 8838288,
      "duration": "2:51",
      "url": "https://www.bilibili.com/video/BV1yup4ewEKz"
    }
  ]
}
```

## Video Download

Use `yt-dlp` to download Bilibili videos. The `download_video.py` script wraps yt-dlp with sensible defaults.

### Usage

```bash
# By BV号
/tmp/bilibili_venv/bin/python3 scripts/download_video.py BV1qD4y1U7fs

# By full URL
/tmp/bilibili_venv/bin/python3 scripts/download_video.py https://www.bilibili.com/video/BV1qD4y1U7fs
```

### Features
- Downloads best available quality (auto-selects format)
- Merges separate audio/video streams into single MP4 via ffmpeg
- Embeds thumbnail and metadata into the output file
- Files saved to `downloads/` directory (relative to current working directory, i.e. the project root)
- **Post-download verification**: checks file exists and is not empty

> **Important**: The script must be run from the **project root directory** (where `opencode.json` is), not from the `scripts/` folder itself. The `downloads/` folder is created relative to the current working directory.

## Troubleshooting & Known Issues

### 1. `--print` Implies `--simulate` (Download Does Not Actually Happen)

`yt-dlp --print` implies `--simulate` by default — it only prints the template result without downloading.

```bash
# ❌ 只计算文件名，不会下载
yt-dlp --print filename "URL"

# ✅ 下载完成后打印最终文件名
yt-dlp --print after_move:filename "URL"
```

Per yt-dlp docs: `--print` *"Implies --quiet. Implies --simulate unless --no-simulate or later stages of WHEN are used."* The `download_video.py` script uses `--print after_move:filename` which is a "later stage" and correctly triggers the download.

### 2. Always Verify Files After Download

The script output may claim a download succeeded when in fact the file was not created (e.g., if `--print` was used without `after_move`, or if yt-dlp encountered a silent error). **Always verify**:
- The output file path exists on disk
- The file size is greater than 0 bytes
- (If using the script directly) Check `ls -lh downloads/` after download

The `download_video.py` script now performs these checks automatically and exits with an error if the file is missing or empty.

### 3. Anthology Videos (合集)

Some Bilibili BV号 are **anthologies** (合集) containing multiple videos under one BV号. yt-dlp downloads the first video in the anthology by default:

```
[BiliBili] BV1mD4y1U7z9: Extracting videos in anthology
[BiliBili] BV1mD4y1U7z9: Downloading video formats for cid 348538681
```

If you need a different episode, use the specific URL with `?p=N` parameter or the episode page URL directly.

### 4. Working Directory

The script creates `downloads/` **relative to the current working directory**, not relative to the script location. Always run from the project root:
```bash
# ✅ 正确：在项目根目录运行
cd /path/to/project
/tmp/bilibili_venv/bin/python3 .opencode/skill/.../scripts/download_video.py BVxxxx

# ❌ 错误：会在 scripts/ 旁边创建 downloads/
cd .opencode/skill/.../scripts/
python3 download_video.py BVxxxx
```

### 5. Authentication for HD Quality

Without login, Bilibili limits downloads to 480P. For 1080P+/4K, pass browser cookies:

```bash
/tmp/bilibili_venv/bin/yt-dlp --cookies-from-browser chrome \
  -o "downloads/%(title)s.%(ext)s" \
  --merge-output-format mp4 \
  "https://www.bilibili.com/video/BV1qD4y1U7fs"
```

### 6. Filename Handling

yt-dlp keeps Chinese characters and punctuation (【】《》~, etc.) in filenames as-is. This can cause shell globbing issues when using `rm` or other commands. Always quote file paths with double quotes.

### Download Script

```python
# scripts/download_video.py
import subprocess
import sys
from pathlib import Path

DOWNLOAD_DIR = Path("downloads")

def download_video(url: str, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"正在下载: {url}")
    result = subprocess.run(
        [
            sys.executable, "-m", "yt_dlp",
            "-o", str(output_dir / "%(title)s.%(ext)s"),
            "--merge-output-format", "mp4",
            "--write-thumbnail",
            "--embed-thumbnail",
            "--embed-metadata",
            "--print", "after_move:filename",
            url,
        ],
        capture_output=True, text=True,
    )

    if result.returncode != 0:
        print(f"下载失败: {result.stderr.strip()}")
        sys.exit(1)

    out_path = result.stdout.strip()
    if not out_path:
        print("下载失败: 无法获取输出文件路径")
        sys.exit(1)

    out_file = Path(out_path)
    if not out_file.exists():
        print(f"下载失败: 文件不存在 — {out_path}")
        sys.exit(1)
    if out_file.stat().st_size == 0:
        print(f"下载失败: 文件为空 — {out_path}")
        sys.exit(1)

    print(f"下载完成: {out_path} ({out_file.stat().st_size / 1024 / 1024:.1f}MB)")

def main():
    if len(sys.argv) < 2:
        print("用法: python download_video.py <B站视频URL 或 BV号>")
        print("示例: python download_video.py https://www.bilibili.com/video/BV1qD4y1U7fs")
        print("示例: python download_video.py BV1qD4y1U7fs")
        sys.exit(1)

    arg = sys.argv[1]
    if arg.startswith("BV"):
        url = f"https://www.bilibili.com/video/{arg}"
    else:
        url = arg

    download_video(url, DOWNLOAD_DIR)

if __name__ == "__main__":
    main()
```

## Complete Example Script

```python
import asyncio
import json
from datetime import datetime
from bilibili_api import search


def clean_title(title: str) -> str:
    return title.replace("<em class=\"keyword\">", "").replace("</em>", "")


async def search_videos(keyword: str, page: int = 1, page_size: int = 20):
    res = await search.search_by_type(
        keyword=keyword,
        search_type=search.SearchObjectType.VIDEO,
        page=page,
        page_size=page_size,
    )
    return res.get("result", [])


def save_results(keyword: str, results: list):
    data = {
        "keyword": keyword,
        "timestamp": datetime.now().isoformat(),
        "total": len(results),
        "videos": [
            {
                "bvid": v.get("bvid", ""),
                "title": clean_title(v.get("title", "")),
                "author": v.get("author", ""),
                "play": v.get("play", 0),
                "duration": v.get("duration", ""),
                "url": f"https://www.bilibili.com/video/{v.get('bvid', '')}",
            }
            for v in results
        ],
    }
    with open("search.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"结果已保存到 search.json ({len(results)} 条)")


async def main():
    keyword = input("请输入搜索关键词: ").strip()
    if not keyword:
        print("关键词不能为空")
        return
    results = await search_videos(keyword)
    if not results:
        print("未找到相关视频")
        return
    save_results(keyword, results)
    for i, v in enumerate(results, 1):
        title = clean_title(v.get("title", ""))
        print(f"{i:2d}. {title} — {v.get('author')} | 播放: {v.get('play')}")


if __name__ == "__main__":
    asyncio.run(main())
```

## Dependencies

### For search
```bash
python3 -m venv /tmp/bilibili_venv
/tmp/bilibili_venv/bin/pip install httpx
```

If `bilibili-api-python` is needed (optional):
```bash
/tmp/bilibili_venv/bin/pip install bilibili-api-python
```

### For download
```bash
/tmp/bilibili_venv/bin/pip install yt-dlp
brew install ffmpeg          # for merging audio/video streams
```

If PyPI is slow, use a mirror:
```bash
/tmp/bilibili_venv/bin/pip install yt-dlp -i https://pypi.doubanio.com/simple/
```

Always run scripts with the venv Python:
```bash
/tmp/bilibili_venv/bin/python3 script.py
```

The library is fully async — always use `asyncio.run()` to execute.
