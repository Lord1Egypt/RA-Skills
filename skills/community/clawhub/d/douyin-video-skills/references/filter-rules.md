# Filter Rules for Douyin Video Selection

## Purpose

Use this file when selecting a target video from Douyin search results before transcript extraction.

## Recommended parameter set

```json
{
  "keyword": "青少年无人机",
  "pickIndex": 1,
  "mustInclude": ["青少年", "无人机"],
  "excludeWords": ["直播", "纯广告", "录播回放"],
  "minLikes": 0,
  "preferRecentDays": 365,
  "durationMinSec": 15,
  "durationMaxSec": 120,
  "contentTypeHints": ["培训", "推荐", "科普", "选购"],
  "accountHints": ["教练", "教育", "俱乐部", "培训"]
}
```

## Selection priority

### 1. Hard filters
Reject candidates when any of the following is true:
- Title does not match the main topic
- Title/account contains excluded words
- Video is obviously unrelated to the task
- Duration is too short to contain useful spoken content

### 2. Soft preferences
Prefer candidates with:
- clearer title-topic match
- stronger relevance to the user goal
- recent publish time
- enough spoken content for transcript extraction
- lower ambiguity between card title and modal title

### 3. Topic fit heuristics
For educational / training topics like 青少年无人机, prefer:
- training / education / recommendation / parenting guidance angles
- explicit benefit explanation
- explicit age range / scenario / selection advice

Avoid when possible:
- live replay
- pure promo with no spoken value
- montage / B-roll only
- off-topic entertainment clips

## Validation after click-through

After opening a candidate video, always validate:
1. card title
2. current modal_id
3. current modal/video title (if readable)

If mismatch is detected, do not continue extraction blindly.
