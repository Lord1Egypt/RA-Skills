# Douyin Video Processor — OpenClaw Skill

Extract text from Douyin (TikTok China) videos, get watermark-free download links, and download videos — all from within OpenClaw.

## What It Does

| Capability | API Key Needed? |
|---|:---:|
| Parse video info (ID, title, URL) from share link | No |
| Download watermark-free video to local file | No |
| Transcribe video speech to text (Chinese + English) | Yes |

## Quick Setup

### 1. Install the Skill

```
/skills install @yzfly/douyin-video-processor
```

### 2. Get an API Key (for text extraction only)

Go to [Alibaba Cloud Bailian](https://help.aliyun.com/zh/model-studio/get-api-key) and create an API key.

### 3. Set the Key

```
/secrets set DASHSCOPE_API_KEY sk-your-key-here
```

Done. Start pasting Douyin links.

## Usage

**Extract text from video:**
> "Extract text from this Douyin video: https://v.douyin.com/xxxxx/"

**Get download link:**
> "Get the download link for this Douyin video: https://v.douyin.com/xxxxx/"

**Download video:**
> "Download this Douyin video: https://v.douyin.com/xxxxx/"

**Batch processing:**
> "Transcribe all these Douyin videos: [link1] [link2] [link3]"

## How It Works

This skill ships 3 standalone Python scripts. No external MCP server or service is needed — everything runs locally (except the Alibaba Cloud ASR API call for text extraction).

| Script | Purpose |
|--------|---------|
| `scripts/douyin_parse.py` | Parse share link → video metadata JSON |
| `scripts/douyin_download.py` | Parse + download watermark-free .mp4 |
| `scripts/douyin_extract_text.py` | Parse + transcribe speech to text via Alibaba Cloud ASR |

All scripts accept a Douyin share link as input and output JSON to stdout.

## Requirements

- Python 3.10+
- Python packages: `requests`, `dashscope` (auto-installed via `scripts/install_deps.sh`)

## Cost

- Parsing and downloading are **completely free**
- Text extraction uses Alibaba Cloud ASR — very low per-minute pricing

## Security

- API key is only sent to `dashscope.aliyuncs.com` (Alibaba Cloud official endpoint)
- No data collection, no telemetry, no background processes
- Full source code included in the skill package

## Links

- GitHub: https://github.com/yzfly/douyin-mcp-server
- API Key Setup: https://help.aliyun.com/zh/model-studio/get-api-key
- Issues: https://github.com/yzfly/douyin-mcp-server/issues

## License

Apache 2.0
