# 业务规则 - content-calibrator

> 来源: skills/content-calibrator/SKILL.md (引用 02手册§十一W9, 增强实施计划v2.1 FIX-06/07)

## 规则列表

### 7维度评分模型

来源: 02手册§十一W9

| 维度 | 代码 | 说明 | 默认权重 |
|:-----|:-----|:-----|:---------|
| 情感共鸣 | ER | 内容引发读者情感反应的能力 | 1.5 |
| 钩子强度 | HP | 前3秒/首段抓注意力的能力 | 1.5 |
| 社会议题 | SR | 内容与社会热点/普遍议题的关联度 | 1.5 |
| 金句密度 | QL | 可传播金句/核心观点的密度 | 1.0 |
| 叙事性 | NA | 故事性/叙事流畅度 | 1.0 |
| 受众广度 | AB | 内容覆盖的受众范围 | 1.0 |
| 实用价值 | PV | 读者可获得的实用信息/技巧 | 1.0 |

### 综合分公式

```
composite = (ER*1.5 + HP*1.5 + SR*1.5 + QL + NA + AB + PV) / 8.5 * 2.0
```

- 各维度评分范围: 0-10 分
- 综合分范围: 0-10 分

### 评分阈值

- threshold_pass: 综合分达到阈值则通过 (具体阈值由 rubric 配置决定)

### Rubric 进化规则

- 偏差阈值: 维度预测偏差 > 1.5 时触发权重调整
- 权重调整步长: 0.1
- 权重调整范围: 0.5 - 2.5
- 偏差映射: views 偏差→HP/SR 权重; engagement 偏差→ER/QL 权重
- 进化频率: 每周一次 (周一 09:00, FIX-06 降频)

### 盲预测硬约束 (FIX-07)

- 不使用 sessions_spawn (会读对话历史)
- exec 脚本直调 LLM,硬禁读对话历史
- 仅喂稿件 + rubric_notes

### Cron 频率 (FIX-06)

- 频率: 每周一次,非实时
- 时间: 周一 09:00 批量处理
- 评分模型: sensenova-6.7-flash-lite (免费)
- 复盘模型: deepseek-v4-flash
- Token 消耗: 原方案单评估周期 ~140K Token,降频后周批量处理

### 按平台独立迭代

- 每个平台独立维护 rubric 文件: `data/content-calibrator/rubrics/{platform}.json`
- 支持平台: douyin / xiaohongshu / bilibili / zhihu 等

### Rubric 降级

- rubric 文件不存在: 使用默认 rubric + v1 (降级,非错误)
- calibrate_score.py 读取 rubric.json 动态权重 (不再硬编码)
