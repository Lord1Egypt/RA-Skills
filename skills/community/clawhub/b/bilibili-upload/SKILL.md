---
name: bilibili-upload
description: Upload videos to Bilibili (哔哩哔哩). Supports automatic login, title, description, tags, and partition selection.
---

# Bilibili Upload 📺

Upload local video files to Bilibili (哔哩哔哩).

## Features
- Upload videos with custom title, description, and tags
- Support selecting different partitions (tid)
- Uses biliup for reliable uploading
- Handles Windows encoding issues automatically

## Requirements
- Python 3.8+
- `biliup` package (installed automatically: `pip install biliup`)

## Installation
1. The skill will install biliup automatically on first use
2. Run `biliup login` in terminal to scan QR code and login
3. Login cookies are saved locally for future use

## Usage

### First Time Login (required once)
```powershell
chcp 65001
$env:PYTHONIOENCODING = "utf-8"
biliup login
```
Scan the QR code with Bilibili App to login. Cookies are saved automatically for future use.

### Basic Upload
```powershell
chcp 65001
$env:PYTHONIOENCODING = "utf-8"
python {skill_dir}/upload.py ^
"full/path/to/your/video.mp4" ^
--title "Your Video Title" ^
--desc "Video description" ^
--tags "tag1,tag2,tag3" ^
--tid 138
```

### Example (after login)
```powershell
python ~/.openclaw/workspace/skills/bilibili-upload/upload.py ^
"C:\Users\hyzu\Documents\openclaw\news_briefing_20260311.mp4" ^
--title "2026年3月11日新闻简报" ^
--desc "每日新闻简报，带金色字幕，AI自动生成" ^
--tags "新闻,每日新闻,简报,AI生成" ^
--tid 138
```

The script automatically handles:
- Path expansion (supports `~` for home directory)
- Windows UTF-8 encoding to avoid Unicode errors
- Error checking for missing video file

### Common Partition IDs
| ID  | Partition |
|-----|-----------|
| 138 | 日常      |
| 124 | 生活      |
| 171 | 科技      |
|  95 | 娱乐      |
| 188 | 美食      |
| 208 | 影视      |
| 210 | 体育      |
| 201 | 动画      |
|  15 | 音乐      |
| 189 | 知识      |

## Notes
- On Windows, always set code page to UTF-8 before login/upload: `chcp 65001`
- Set `PYTHONIOENCODING=utf-8` to avoid Unicode encoding errors
- Login needs interactive terminal to display QR code, must do it manually once
- After login, cookies are saved automatically and future uploads can be automated
- If you don't see video immediately after upload, it's probably still in Bilibili's review queue

## Script
The upload script is located at:
`{skill_dir}/upload.py`

Where `{skill_dir}` is the installation directory of this skill. The script accepts any full path from the user, and automatically handles path expansion.
