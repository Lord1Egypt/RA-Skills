# 示例 - content-final-supervisor

> 来源: skills/content-final-supervisor/SKILL.md 示例章节

## 示例1: 全链终检通过

### 输入

```json
{
  "episode_id": 123,
  "stage": "all",
  "script_content": "剧本: 第一幕 角色A登场...",
  "storyboard_content": "{\"scenes\": [...]}",
  "video_url": "https://example.com/video/123.mp4"
}
```

### 输出

```json
{
  "success": true,
  "data": {
    "episode_id": 123,
    "stage": "all",
    "verdict": "pass",
    "checks": {
      "script": {"verdict": "pass", "supervision_id": 456},
      "storyboard": {"verdict": "pass", "supervision_id": 457},
      "video": {"verdict": "pass", "supervision_id": 458},
      "redlines": {"verdict": "pass", "violations": []},
      "consistency": {"verdict": "pass", "inconsistencies": []}
    },
    "final_supervision_id": 458,
    "can_publish": true
  },
  "error": null,
  "code": "SUPERVISION_OK"
}
```

> 全链终检: 按 script→storyboard→video 顺序依次执行,每阶段通过后才进入下一阶段。

## 示例2: 红线违规触发返工

### 输入

```json
{
  "episode_id": 124,
  "stage": "script",
  "script_content": "剧本内容...含敏感词XXX..."
}
```

### 输出

```json
{
  "success": true,
  "data": {
    "episode_id": 124,
    "verdict": "fail",
    "redline_violation": "敏感词:XXX",
    "redo_recommended": true
  },
  "error": null,
  "code": "SUPERVISION_REDO"
}
```

> 红线违规: 立即标记 verdict=fail,进入返工流程。
> 返工后重新进入对应阶段终检。返工次数 > 3 次: 触发 final_arbitration 终审。
