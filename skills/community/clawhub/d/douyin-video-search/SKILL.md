---
name: douyin-video-search
description: (已验证) 通过 TikHub API 搜索抖音视频，支持关键词、分页、多维度排序和筛选。
metadata:
  version: 1.0.0
  source: https://github.com/your-repo/douyin-video-search
  author: an
  tags: [douyin, search, video, tikhub, social-media]
  license: MIT
  requirements:
    - python
    - "pip:requests"
---

# SKILL.md for douyin-video-search

## Description

一个功能强大的抖音视频搜索技能，它通过调用 **TikHub 官方 API** 来获取搜索结果。该技能支持通过关键词进行搜索，并提供了丰富的参数选项，包括分页、多种排序方式（综合、最多点赞、最新发布）以及发布时间和视频时长的筛选。

这是一个核心的、原子化的搜索工具，可以被其他上层技能（如 `visual-benchmark-finder`）调用，以实现更复杂的业务逻辑。

## Configuration

本技能需要一个有效的 TikHub API Token 才能工作。请在您的 `~/.openclaw/config.json` 文件中添加以下配置项。该 Token 可与 `douyin-downloader` 等其他 TikHub 系技能共用。

```json
{
  "tikhub_api_token": "YOUR_TIKHUB_API_TOKEN"
}
```
> 您可以在 [TikHub 官网](https://user.tikhub.io/register) 注册免费获取 Token。

## How to Use

该技能的核心脚本 (`scripts/douyin_search.py`) 是一个功能完善的命令行工具，可以直接调用，也可以被其他技能通过 `exec` 工具调用。

### Parameters

*   **`keyword`** (必填): 搜索的关键词。
*   **`--cursor`**: 分页游标，第一页默认为 `0`。
*   **`--sort`**: 排序方式。
    *   `0`: 综合 (默认)
    *   `1`: 最多点赞
    *   `2`: 最新发布
*   **`--publish`**: 发布时间。
    *   `0`: 不限 (默认)
    *   `1`: 最近一天
    *   `7`: 最近一周
    *   `180`: 最近半年
*   **`--duration`**: 视频时长。
    *   `0`: 不限 (默认)
    *   `0-1`: 1分钟内
    *   `1-5`: 1-5分钟
    *   `5-10000`: 5分钟以上
*   **`--raw`**: 如果提供此参数，将输出原始的 JSON 数据而不是格式化后的文本。

### Example Invocation

**简单搜索:**
```powershell
& "F:\python 3.10\python.exe" "C:\Users\EDY\.openclaw\skills\douyin-video-search\scripts\douyin_search.py" "美食"
```

**带参数的高级搜索:**
```powershell
& "F:\python 3.10\python.exe" "C:\Users\EDY\.openclaw\skills\douyin-video-search\scripts\douyin_search.py" "旅行" --sort "2" --publish "7"
```
