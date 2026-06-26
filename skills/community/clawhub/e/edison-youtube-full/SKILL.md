---
name: edison-youtube-full
description: "Complete YouTube toolkit for agents: search videos, fetch metadata, browse channels and playlists, and pull transcripts. Use when you need comprehensive YouTube Data API access (search, channels, playlists) plus transcript extraction in a single workflow."
---

# YouTube Full Skill

本技能把常见的 YouTube 工作流（搜索、视频/频道/播放列表元数据、字幕抓取）封装成可复用脚本，方便在单个会话里串联使用。

## 依赖与准备

1. **YouTube Data API Key**  
   - 到 [Google Cloud Console](https://console.cloud.google.com/apis/library/youtube.googleapis.com) 启用 YouTube Data API v3，并创建 API Key。
   - 在当前 shell 设置：
     ```bash
     export YOUTUBE_API_KEY="YOUR_KEY"
     ```
     或者在运行脚本时使用 `--api-key` 参数。

2. **Python 依赖**（建议放在虚拟环境）：
   ```bash
   pip install -r scripts/requirements.txt
   ```
   - `requests`：调用官方 REST API
   - `youtube-transcript-api`：抓取字幕

3. 所有脚本默认输出 JSON（stdout），方便直接被上游工具读取，或通过 `jq` 等命令行处理。

## 快速开始

| 任务 | 命令 | 说明 |
|------|------|------|
| 搜索视频 | `python scripts/search_videos.py --query "openclaw" --max-results 5` | 返回匹配视频/频道集合 |
| 视频详情 | `python scripts/get_video_details.py --ids dQw4w9WgXcQ` | 支持一次查询多个视频 ID（逗号分隔） |
| 频道最新上传 | `python scripts/get_channel_videos.py --channel-id UC_x5XG1OV2P6uZZ5FSM9Ttw --max-results 10` | 可指定 order=latest/popular |
| 播放列表内容 | `python scripts/get_playlist_items.py --playlist-id PLBCF2DAC6FFB574DE` | 支持分页（自动拉全量） |
| 字幕抓取 | `python scripts/get_transcript.py --video-id dQw4w9WgXcQ --languages zh-CN,en` | 按语言优先级尝试抓取 |

> 🌐 更多 API 字段参考 `references/api_quickstart.md`。

## 工作流建议

1. **组合式使用**：先用 `search_videos.py` 拿到 videoId/channelId，再调用其他脚本获取详情或字幕。
2. **批量处理**：大多数脚本支持一次性传入多个 ID（用逗号分隔），能减少 API 调用次数。
3. **速率限制**：YouTube Data API 默认 10,000 quota/天。`search`/`videos` 等接口有不同配额消耗，见参考文档。
4. **字幕回退**：`youtube-transcript-api` 会自动 fallback 到指定语言列表的下一个选项；若视频无字幕会抛异常，脚本会以非零退出码返回。

## 文件结构

```
youtube-full/
├── SKILL.md
├── references/
│   └── api_quickstart.md
└── scripts/
    ├── requirements.txt
    ├── search_videos.py
    ├── get_video_details.py
    ├── get_channel_videos.py
    ├── get_playlist_items.py
    └── get_transcript.py
```

## 故障排查

| 问题 | 可能原因 | 解决办法 |
|------|----------|----------|
| HTTP 403 / quotaExceeded | API Key 配额不足或未启用服务 | 去 GCP 控制台检查配额、启用结算或更换 Key |
| 找不到字幕 | 视频关闭字幕或无匹配语言 | 换语言列表、改用自动字幕 (`--languages auto`) |
| `HttpAccessTokenRefreshError` | 使用 OAuth token 且已过期 | 重新获取 token 或改用 API Key |
| CLI 报 `ModuleNotFoundError` | 缺少依赖 | 重新执行 `pip install -r scripts/requirements.txt` |

## 最佳实践

- 把常用命令写成脚本/Makefile，方便一键获取多条数据。
- 对于需要批量处理的视频列表，优先调用 `get_playlist_items.py` / `get_channel_videos.py` 拉取 ID，然后再批量获取详情或字幕。
- 脚本输出 JSON，建议直接 `| jq` 做筛选或保存为文件供后续步骤使用。
