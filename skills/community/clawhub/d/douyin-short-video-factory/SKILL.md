---
name: douyin-short-video-factory
description: >
  Create Douyin (抖音) short videos end-to-end: AI image generation, video prompt 
  creation, frame extraction, and hashtag optimization. Integrates with Douyin's 
  ecosystem for viral content.
  Triggers: "抖音视频", "douyin", "短视频创作", "short video factory".
version: 1.0.0
tags:
  - latest
  - chinese-platform
  - video
  - content-creation
---

# Douyin Short Video Factory

End-to-end Douyin (抖音) short video creation: AI image generation, video prompt engineering, frame extraction, and hashtag optimization.

## Usage

### Parse Douyin Video

```bash
mcporter call 'douyin.parse_douyin_video_info(share_link: "https://v.douyin.com/xxx/")'
mcporter call 'douyin.get_douyin_download_link(share_link: "https://v.douyin.com/xxx/")'
```

### Generate Douyin Hashtags

```python
def generate_douyin_tags(topic, categories):
    hot = ["#抖音", "#热门", "#推荐", "#fyp", "#viral"]
    niche = [f"#{c}" for c in categories[:3]]
    return f"#{topic} " + " ".join(hot + niche)
```

### Virality Scoring

```python
def score_douyin_virality(meta):
    score = min(30, meta.get("digg_count", 0) // 10000)
    score += min(30, meta.get("comment_count", 0) // 1000)
    duration = meta.get("duration", 0)
    if 15 <= duration <= 30: score += 20
    elif 30 <= duration <= 60: score += 15
    return min(100, score)
```

## Tags

`douyin` `抖音` `video` `short-video` `chinese-platform` `content-creation` `ai-video`
