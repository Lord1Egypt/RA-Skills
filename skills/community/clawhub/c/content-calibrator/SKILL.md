---
name: content-calibrator
version: "1.0.0"
description: "内容质量校准与预测闭环,7维评分(ER情感/HP钩子/SR议题/QL金句/NA叙事/AB受众/PV实用)+盲预测+T+3d复盘+rubric进化,按平台独立迭代。触发:内容评分/质量预测/校准复盘/rubric更新"
tools: [read, exec]
dependencies:
  - published-track
metadata:
  layer: plugin
  priority: P1
  category: content-analytics
  version: "1.0.0"
  author: "JueJin AI"
  requires:
    config: []
    env: ["SENSENOVA_API_KEY", "SENSENOVA_BASE_URL"]
    bins: ["python"]
---

# Content Calibrator - 内容质量校准与预测闭环

**版本**: v1.0.0
**创建日期**: 2026-07-07
**优先级**: P1 (来源: FIX-17, 非赚钱链路核心, 从P0降为P1)
**所属部门**: 礼部（内容质量）
**来源**: 02手册§十一 W9 / 增强实施计划v2.1第3批 FIX-06/07
**依赖**: published-track (发布记录+数据采集统一入口)
**Cron频率**: 每周一次 (周一09:00, FIX-06降频)
**评分模型**: sensenova-6.7-flash-lite (免费, 来源:.env SENSENOVA_API_KEY)
**复盘模型**: deepseek-v4-flash (来源:.env SENSENOVA_BASE_URL, 通过sensenova渠道)

---

## 使用场景

| 场景 | 触发条件 | 说明 |
|:-----|:---------|:-----|
| 内容评分 | 发布前或发布后 | 7维度LLM评分,输出综合分+改进建议 |
| 盲预测 | 评分后发布前 | 仅喂稿件+rubric,不读对话历史,预测互动表现 |
| T+3d复盘 | 发布3天后 | 预测vs实际数据对比,计算偏差 |
| Rubric进化 | 周一Cron | 基于历史复盘数据更新评分标准 |

**核心价值**: 通过"评分→预测→复盘→进化"闭环,持续提升内容质量评估准确度。按平台独立维护rubric,适配不同平台的内容特征。

**FIX-06降频方案**: 原方案7维评分×多平台盲预测单评估周期消耗~140K Token。修订为每周一次批量处理,评分使用免费模型(sensenova-6.7-flash-lite),复盘使用deepseek-v4-flash。

**FIX-07变通方案**: 盲预测不使用sessions_spawn(会读对话历史),改为exec脚本直调LLM,硬禁读对话历史,只喂稿件+rubric_notes。

---

## 工作流

### 1. 内容评分（score）

**输入**: content(文本), platform(平台), rubric_version(版本,可选)

**执行**:
```bash
python skills/content-calibrator/scripts/calibrate_score.py \
  --content "今天分享一个提高效率的小技巧..." \
  --platform douyin \
  --rubric-version v1
```

**处理**: 调用sensenova-6.7-flash-lite对7个维度各打0-10分,计算综合分

**7维度定义**(来源:02手册§十一W9):
| 维度 | 代码 | 说明 | 权重 |
|:-----|:-----|:-----|:-----|
| ER | 情感共鸣 | 内容引发读者情感反应的能力 | 1.5 |
| HP | 钩子强度 | 前3秒/首段抓注意力的能力 | 1.5 |
| SR | 社会议题 | 内容与社会热点/普遍议题的关联度 | 1.5 |
| QL | 金句密度 | 可传播金句/核心观点的密度 | 1.0 |
| NA | 叙事性 | 故事性/叙事流畅度 | 1.0 |
| AB | 受众广度 | 内容覆盖的受众范围 | 1.0 |
| PV | 实用价值 | 读者可获得的实用信息/技巧 | 1.0 |

**综合分公式**: `composite = (ER×1.5 + HP×1.5 + SR×1.5 + QL + NA + AB + PV) / 8.5 × 2.0`

### 2. 盲预测（predict）

**输入**: content(文本), rubric_notes(评分标准备注)

**执行**:
```bash
python skills/content-calibrator/scripts/calibrate_predict.py \
  --content "今天分享一个提高效率的小技巧..." \
  --rubric-notes "douyin平台偏向情感共鸣和钩子强度"
```

**处理**: exec直调LLM(不读对话历史),仅基于稿件+rubric_notes预测互动表现

**硬约束(FIX-07)**: 脚本内部构造独立prompt,不传入任何对话上下文/历史消息

### 3. T+3d复盘（review）

**输入**: prediction_id, actual_stats(实际数据), platform(平台,P2-07新增)

**执行**:
```bash
python skills/content-calibrator/scripts/calibrate_review.py \
  --prediction '{"predicted_views":500,"predicted_engagement":0.05}' \
  --actual '{"views":520,"likes":30,"comments":5}' \
  --platform douyin
```

**处理**: 对比预测vs实际,计算准确率和偏差,生成rubric更新建议。review记录保存platform和deviation供evolve使用(P2-07修复)

### 4. Rubric进化（evolve）

每周一Cron执行,基于本周所有复盘数据:
1. 聚合本周所有review记录
2. 分析哪些维度预测偏差最大
3. 更新对应平台的rubric评分标准
4. 写入 `data/content-calibrator/rubrics/{platform}.json`

**执行**:
```bash
python skills/content-calibrator/scripts/calibrate_evolve.py tnt_001 --days 7
```

**处理**: 聚合近N天review数据→按平台分组→计算各维度偏差比率→偏差超阈值(1.5)的维度调整权重(步长0.1,范围0.5-2.5)→原子写入rubric.json

**P2-07修复(2026-07-12)**:
- 创建calibrate_evolve.py(之前缺失)
- calibrate_review.py添加--platform参数,review记录保存platform和deviation
- calibrate_score.py读取rubric.json动态权重(不再硬编码)
- 偏差映射: views偏差→HP/SR权重, engagement偏差→ER/QL权重

### 5. 按平台独立迭代

每个平台独立维护rubric文件:
```
data/content-calibrator/
├── rubrics/
│   ├── douyin.json       # 抖音评分标准
│   ├── xiaohongshu.json  # 小红书评分标准
│   ├── bilibili.json     # B站评分标准
│   └── ...
├── predictions/
│   └── {prediction_id}.json  # 预测记录
└── reviews/
    └── {prediction_id}.json  # 复盘记录
```

---

## 输入格式

```json
{
  "mode": "score|predict|review",
  "content": "内容文本",
  "platform": "douyin",
  "rubric_version": "v1",
  "rubric_notes": "评分标准备注",
  "prediction": {"predicted_views": 500, "predicted_engagement": 0.05},
  "actual": {"views": 520, "likes": 30, "comments": 5}
}
```

---

## 输出格式

### 评分输出
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

### 预测输出
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

### 复盘输出
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

---

## 异常处理

| 异常 | 处理 | code |
|:-----|:-----|:-----|
| SENSENOVA_API_KEY未配置 | 返回error提示 | ENV_MISSING |
| LLM调用超时(>30s) | 返回error+降级建议 | LLM_TIMEOUT |
| LLM返回非JSON | 尝试解析失败后返回error | LLM_PARSE_FAILED |
| 空内容输入 | 返回error | EMPTY_CONTENT |
| 无效平台名 | 返回error | INVALID_PLATFORM |
| rubric文件不存在 | 使用默认rubric+v1 | (降级,非错误) |

---

## Cron配置

```json
{
  "name": "content-calibrator-weekly",
  "schedule": "0 9 * * 1",
  "agent": "libu",
  "message": "执行content-calibrator周复盘: 1.采集上周所有平台发布内容数据 2.对每条内容执行T+3d复盘 3.聚合分析预测偏差 4.更新各平台rubric评分标准"
}
```

**频率约束(FIX-06)**: 每周一次,非实时。周一09:00批量处理,避免高频Token消耗。

---

## 示例

### 评分示例
```bash
python skills/content-calibrator/scripts/calibrate_score.py \
  --content "在职场中,最可怕的不是能力不足,而是不知道自己不足。今天分享3个自我提升的方法..." \
  --platform zhihu
```

### 盲预测示例
```bash
python skills/content-calibrator/scripts/calibrate_predict.py \
  --content "在职场中,最可怕的不是能力不足..." \
  --rubric-notes "zhihu平台偏向深度内容和实用价值"
```

### 复盾示例
```bash
python skills/content-calibrator/scripts/calibrate_review.py \
  --prediction '{"predicted_views":"500-800","predicted_engagement":"3-5%"}' \
  --actual '{"views":620,"likes":45,"comments":8}'
```

---

## 历史记录

| 日期 | 版本 | 变更 |
|:-----|:-----|:-----|
| 2026-07-07 | v1.0.0 | 初始创建, W9第3批, FIX-06/07降频+exec直调LLM |
