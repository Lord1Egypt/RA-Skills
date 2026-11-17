# 示例 - content-calibrator

> 来源: skills/content-calibrator/SKILL.md 示例章节

## 示例1: 内容评分 (score)

### 输入

```bash
python skills/content-calibrator/scripts/calibrate_score.py \
  --content "在职场中,最可怕的不是能力不足,而是不知道自己不足。今天分享3个自我提升的方法..." \
  --platform zhihu
```

```json
{
  "mode": "score",
  "content": "在职场中,最可怕的不是能力不足,而是不知道自己不足。今天分享3个自我提升的方法...",
  "platform": "zhihu"
}
```

### 输出

```json
{
  "success": true,
  "data": {
    "scores": {"ER": 8, "HP": 7, "SR": 6, "QL": 7, "NA": 8, "AB": 7, "PV": 9},
    "composite": 7.41,
    "threshold_pass": true,
    "suggestions": ["增强社会议题关联度", "增加金句密度"]
  },
  "error": null,
  "code": null
}
```

## 示例2: 盲预测 (predict)

### 输入

```bash
python skills/content-calibrator/scripts/calibrate_predict.py \
  --content "在职场中,最可怕的不是能力不足..." \
  --rubric-notes "zhihu平台偏向深度内容和实用价值"
```

```json
{
  "mode": "predict",
  "content": "在职场中,最可怕的不是能力不足...",
  "rubric_notes": "zhihu平台偏向深度内容和实用价值"
}
```

### 输出

```json
{
  "success": true,
  "data": {
    "prediction": {"expected_views": "500-800", "expected_engagement": "3-5%"},
    "confidence": 0.75,
    "reasoning": "钩子强度中等,情感共鸣较高,预计互动率3-5%"
  },
  "error": null,
  "code": null
}
```

## 示例3: T+3d 复盘 (review)

### 输入

```bash
python skills/content-calibrator/scripts/calibrate_review.py \
  --prediction '{"predicted_views":"500-800","predicted_engagement":"3-5%"}' \
  --actual '{"views":620,"likes":45,"comments":8}' \
  --platform zhihu
```

### 输出

```json
{
  "success": true,
  "data": {
    "accuracy": 0.85,
    "deviation": {"views": 4.0, "engagement": 1.2},
    "rubric_update_suggestions": ["ER权重应从1.5调整为1.3"]
  },
  "error": null,
  "code": null
}
```
