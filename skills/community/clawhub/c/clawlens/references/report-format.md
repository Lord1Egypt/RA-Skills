# Clawlens Report Format Reference

This document defines the expected Markdown structure for the clawlens insights report.

## Report Structure

```markdown
# Clawlens 使用洞察报告

> 分析期间: {start_date} ~ {end_date} | {total_sessions} 会话 | {total_messages} 消息 | {days_active} 活跃天

## 概览摘要

{4-5 sentence executive summary covering: what's working, what's hindering, quick wins, ambitious suggestions}

---

## 1. 使用概览

### 基础统计

| 指标 | 数值 |
|------|------|
| 会话数 | {n} |
| 消息数 | {n} |
| 活跃天数 | {n} |
| Token 消耗 | 输入 {n} / 输出 {n} |
| 总费用 | ${n} |

### 活跃时间分布

{Describe peak hours and weekday patterns using text and small tables}

### Token 消耗趋势

{Week-over-week trend description}

---

## 2. 任务分类

### 分类占比

| 类别 | 占比 | 会话数 |
|------|------|--------|
| {category} | {%} | {n} |
| ... | ... | ... |

### 趋势变化

{Describe how task distribution changed over the analysis period}

### 高价值任务

{List tasks that saved the most time or had highest repeat frequency}

---

## 3. 摩擦分析

### Claw 侧问题

| 摩擦类型 | 次数 | 示例 |
|----------|------|------|
| {type} | {n} | {brief example from session} |

### 用户侧摩擦

| 摩擦类型 | 次数 | 示例 |
|----------|------|------|
| {type} | {n} | {brief example from session} |

### Top 摩擦模式

{Narrative description of the top 3 friction patterns with specific session examples}

---

## 4. Skills 生态分析

### 使用情况

| Skill | 使用次数 | 状态 |
|-------|---------|------|
| {skill_name} | {n} | 活跃 / 未使用 |

### 未使用 Skills

{List installed but unused skills with cleanup suggestion}

### 推荐

{Suggest skills from community based on task patterns}

---

## 5. 自主行为审计

### 概览

| 指标 | 数值 |
|------|------|
| 自主行为总次数 | {n} |
| 用户确认/采纳率 | {%} |
| 否决/忽略率 | {%} |

### 行为分类

{Breakdown by type: cron, heartbeat, background}

### 异常标记

{Flag any out-of-bounds or unexpected autonomous actions}

---

## 6. 多渠道分析

### 渠道使用分布

| 渠道 | 会话数 | 占比 |
|------|--------|------|
| {channel} | {n} | {%} |

### 渠道 x 任务类型

{Cross-tabulation of channels and task types}

### 渠道优化建议

{Suggest better channel-task matches}

---

*报告由 clawlens v{version} 生成于 {timestamp}*
```

## Style Guidelines

- Use second person ("你") in Chinese, "you" in English
- Be direct and actionable, not vague or fluffy
- Include specific session examples where possible (truncated quotes)
- Use tables for quantitative data, narrative for qualitative insights
- Bold key findings and recommendations
- Keep each section self-contained and scannable

## Task Categories

| Key | Chinese | English |
|-----|---------|---------|
| email_management | 邮件管理 | Email Management |
| scheduling | 日程协调 | Scheduling |
| info_retrieval | 信息检索 | Info Retrieval |
| content_creation | 内容创作 | Content Creation |
| coding_assistance | 编码辅助 | Coding Assistance |
| automation | 自动化脚本 | Automation |
| smart_home | 智能家居控制 | Smart Home |
| file_operations | 文件操作 | File Operations |
| communication | 通信/消息 | Communication |
| planning | 规划/任务管理 | Planning |
| personal_assistant | 个人助理/杂项 | Personal Assistant |

## Friction Categories

### Claw-side

| Key | Chinese | English |
|-----|---------|---------|
| misunderstood_intent | 误解指令 | Misunderstood Intent |
| wrong_execution | 执行错误 | Wrong Execution |
| ignored_preference | 未遵循偏好 | Ignored Preference |
| hallucinated_info | 编造信息 | Hallucinated Info |
| excessive_action | 过度操作 | Excessive Action |

### User-side

| Key | Chinese | English |
|-----|---------|---------|
| insufficient_context | 上下文不足 | Insufficient Context |
| unclear_instruction | 指令模糊 | Unclear Instruction |
| wrong_channel | 渠道不当 | Wrong Channel |
| contradictory_request | 矛盾请求 | Contradictory Request |
