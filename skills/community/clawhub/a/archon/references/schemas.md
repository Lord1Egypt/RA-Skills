# Archon File Schemas

All files use YAML frontmatter + Markdown body. Dates: `YYYY-MM-DD`. Tags: lowercase kebab-case.

---

## Daily Log — `daily/YYYY-Wnn/YYYY-MM-DD.md`

```yaml
---
date: "YYYY-MM-DD"
weekday: "Monday"          # Monday Tuesday ...
mood: ""                   # great/good/neutral/low/bad
energy: ""                 # high/medium/low
key_events: []
decisions_made: []
people_interactions: []
tags: []
---

## 今日要点
- ...

## 详细记录
...

## 反思与感悟
...

## 明日计划
- ...
```

---

## Decision — `decisions/YYYY-MM-DD-short-title.md`

```yaml
---
title: ""
date: "YYYY-MM-DD"
status: "pending"           # pending/decided/executing/completed/abandoned
category: ""               # tech/team/process/business/career
importance: ""             # critical/high/medium/low
reversibility: ""          # reversible/partially-irreversible/irreversible
context: ""
options: []
decision: ""
rationale: ""
related_decisions: []
related_signals: []
tags: []
---

## 利弊分析

### 选项 A：
**优势**：
- ...

**劣势**：
- ...

## 预期风险
...

## 后续跟进
...

## 结果回访（YYYY-MM-DD）
**实际结果**：
**偏差分析**：
**经验教训**：
```

---

## Signal — `signals/YYYY-MM-DD-short-title.md`

```yaml
---
title: ""
date: "YYYY-MM-DD"
type: ""                   # risk/opportunity/trend/anomaly
severity: ""               # critical/high/medium/low
source: ""                 # daily-log/observation/metrics/external
status: "watching"        # watching/escalated/addressed/dismissed
description: ""
indicators: []
action_taken: ""
related_decisions: []
tags: []
---

## 信号描述
...

## 具体指标/观察
- ...

## 已采取行动
...

## 下一步
...
```

---

## Coach — `coach/YYYY-MM-DD-area-scenario.md`

```yaml
---
date: "YYYY-MM-DD"
area: ""                   # 向上管理/沟通表达/管带与辅导
scenario: ""
trigger: ""
challenge: ""
ai_suggestion: ""
practice_plan: []
follow_up_date: ""
outcome: ""
tags: []
---

## 场景描述
...

## 面临的挑战
...

## AI 建议

### 沟通策略
...

### 话术模板
...

### 注意事项（基于我的短板）
...

## 练习计划
- ...

## 跟进
- 跟进日期：
```

---

## War Room — `war-room/YYYY-MM-DD-issue.md`

```yaml
---
title: ""
created: "YYYY-MM-DD"
status: "active"           # active/resolved/archived
priority: ""               # critical/high/medium/low
deadline: ""
owner: ""
description: ""
constraints: []
progress: ""
resolution: ""
---

## 问题描述
...

## 约束条件
- ...

## 当前进度
...

## 下一步行动
- ...

## 决议
...
```

---

## Pattern — `patterns/category-short-title.md`

```yaml
---
title: ""
category: ""               # tech-management/team-building/process/career/industry
source: ""
applicability: ""
summary: ""
key_insights: []
related_decisions: []
tags: []
---

## 摘要
...

## 核心洞察
- ...

## 适用场景
...

## 与我的关联
...

## 参考资料
- ...
```

---

## Priority Project Index — `projects/index.md`

```yaml
---
owner: "Sopaco"
last_updated: "YYYY-MM-DD"
active_projects: []
archived_projects: []
tags: ["projects", "portfolio"]
---

## 重点项目总览

| 项目 | 状态 | 当前周期 | 负责人 | 本期重点 | Top Risk | 下次检查 |
|------|------|----------|--------|----------|----------|----------|
| ... | ... | ... | ... | ... | ... | ... |

## 管理原则

- `projects/` 仅管理用户明确指定纳入的重点项目
- 默认节奏：周 WBR、月度 OKR 检查、季度 OKR 复盘
- 汇报默认采用结论先行、状态透明、影响导向、诉求明确的风格
```

---

## Project Charter — `projects/active/<project-slug>/charter.md`

```yaml
---
title: ""
project_slug: ""
status: "active"            # active/on-hold/completed/archived
priority: ""                # critical/high/medium/low
owner: ""
start_date: "YYYY-MM-DD"
target_date: ""
current_quarter: "YYYY-Qn"
annual_objective: ""
business_value: ""
scope_in: []
scope_out: []
key_stakeholders: []
success_metrics: []
review_cadence: ["wbr", "monthly-okr", "quarterly-review"]
tags: []
---

## 项目背景
...

## 战略意义
...

## 年度目标
...

## 范围边界

### 范围内
- ...

### 非范围
- ...

## 干系人
- ...

## 成功标准
- ...

## 治理机制
- 周：WBR
- 月：OKR 检查
- 季：OKR 复盘
```

---

## Project OKR — `projects/active/<project-slug>/okr.md`

```yaml
---
project_slug: ""
period: "annual"
owner: ""
last_updated: "YYYY-MM-DD"
objectives: []
key_results: []
milestones: []
dependencies: []
tags: []
---

## 年度 Objectives
- ...

## Quarterly Objectives
- ...

## Key Results

| KR | Owner | Baseline | Target | Current | Status |
|----|-------|----------|--------|---------|--------|
| ... | ... | ... | ... | ... | on-track |

## 关键里程碑
- ...

## 关键依赖
- ...
```

---

## Project Collaboration — `projects/active/<project-slug>/collaboration.md`

```yaml
---
project_slug: ""
last_updated: "YYYY-MM-DD"
collaboration_items: []
escalation_items: []
tags: []
---

## 跨团队协作总览

| 团队/角色 | Owner | 协作事项 | 当前状态 | 风险等级 | 下一步 | 是否需升级 |
|-----------|-------|----------|----------|----------|--------|------------|
| ... | ... | ... | in-progress | medium | ... | no |

## 当前分歧与卡点
- ...

## 升级路径
- ...
```

---

## Project Reporting — `projects/active/<project-slug>/reporting.md`

```yaml
---
project_slug: ""
last_updated: "YYYY-MM-DD"
overall_status: ""          # on-track/at-risk/off-track/completed
reporting_focus: ""
key_asks: []
tags: []
---

## Executive Summary
...

## Progress Against Goals
- ...

## Key Wins / Impact
- ...

## Risks / Issues
- ...

## Dependencies / Support Needed
- ...

## Next Steps
- ...

## 对上汇报口径
...

## 横向同步口径
...
```

---

## Project Risks — `projects/active/<project-slug>/risks.md`

```yaml
---
project_slug: ""
last_updated: "YYYY-MM-DD"
risk_items: []
tags: []
---

## 风险台账

| 风险 | 类型 | 概率 | 影响 | 状态 | Owner | 缓解措施 | 升级条件 |
|------|------|------|------|------|-------|----------|----------|
| ... | dependency | medium | high | open | ... | ... | ... |

## 当前 Top Risks
- ...
```

---

## Project WBR — `projects/active/<project-slug>/wbr/YYYY-Wnn.md`

```yaml
---
project_slug: ""
week: "YYYY-Wnn"
date: "YYYY-MM-DD"
overall_status: ""          # on-track/at-risk/off-track/completed
focus: ""
progress_summary: ""
kr_changes: []
milestone_status: []
blockers: []
dependencies: []
escalations: []
next_week_priorities: []
tags: []
---

## Executive Summary
...

## Progress This Week
- ...

## KR Changes
- ...

## Milestone Status
- ...

## Risks / Blockers
- ...

## Dependencies / Support Needed
- ...

## Next Week Focus
- ...
```

---

## Project Monthly OKR Check — `projects/active/<project-slug>/monthly/YYYY-MM.md`

```yaml
---
project_slug: ""
month: "YYYY-MM"
date: "YYYY-MM-DD"
overall_status: ""          # on-track/at-risk/off-track/completed
objective_status: []
kr_status: []
major_deliveries: []
key_variances: []
risks: []
corrective_actions: []
tags: []
---

## Monthly Summary
...

## Objective / KR Status

| Objective / KR | Status | Current | Target | Notes |
|----------------|--------|---------|--------|-------|
| ... | on-track | ... | ... | ... |

## Key Deliveries
- ...

## Variances and Root Causes
- ...

## Risks and Corrective Actions
- ...

## Next Month Focus
- ...
```

---

## Project Quarterly Review — `projects/active/<project-slug>/quarterly/YYYY-Qn.md`

```yaml
---
project_slug: ""
quarter: "YYYY-Qn"
date: "YYYY-MM-DD"
overall_result: ""          # achieved/partially-achieved/not-achieved
objective_review: []
kr_results: []
major_wins: []
misses: []
root_causes: []
key_decisions: []
collaboration_learnings: []
next_quarter_implications: []
leadership_asks: []
tags: []
---

## Quarter Summary
...

## Objective / KR Review

| Objective / KR | Result | Notes |
|----------------|--------|-------|
| ... | achieved | ... |

## Major Achievements
- ...

## Misses / Gaps
- ...

## Root Causes
- ...

## Collaboration Learnings
- ...

## Implications for Next Quarter
- ...

## Leadership Asks
- ...
```

---

## Profile Files

### `profile/me.md`
```yaml
name: "Sopaco"
title: "大前端平台与架构部负责人"
company: "Hytech"
experience_years: 15
location: "北京"
industry: "金融"
preferred_communication: "indirect"
meeting_style: "structured"
feedback_style: "sandwich"
```

### `profile/values.md`
```yaml
core_values:
  - "目标驱动，结果导向"
  - "成长思维，持续学习"
  - "坦诚清晰，公开透明"
  - "上下齐心，相互支持"
management_philosophy: "信任优先，赋能大于管控，数据逻辑大于主观情绪"
decision_principles:
  - "可逆决策快做，不可逆决策慢做"
  - "事 > 人 > 技术（但看情况：当人的问题严重影响团队时，人优先）"
  - "长期价值优于短期利益"
anti_patterns:
  - "官僚一言堂"
  - "信息不透明"
  - "人情世故大于客观事实"
```

### `profile/preferences.md`
```yaml
work_style: "deep-focus"
decision_style: "analytical"
information_preference: "mixed"
risk_tolerance: "moderate"
delegation_preference: "balanced"
conflict_style: "collaborate"
learning_style: "practice"
```

### `profile/strengths.md`
```yaml
technical_strengths:
  - "跨端架构（Android → 大前端全栈）"
  - "技术平台化与工程化"
  - "技术选型与方案设计"
management_strengths:
  - "团队从零搭建（多次 0→30 人经验）"
  - "快速适应新环境（6 次跳槽均成功立足）"
  - "目标拆解与结果交付"
interpersonal_strengths:
  - "真诚建立信任"
  - "跨团队协作"
recognized_achievements:
  - "15 年从初级开发到部门负责人，薪酬增长 18 倍"
  - "多次成功搭建和带领 10-30 人团队"
  - "跨行业适应（教育→旅行→O2O→音乐→短视频→金融）"
```

### `profile/growth-areas.md`
```yaml
growth_areas:
  - area: "向上管理"
    current_level: "developing"
    target_level: "proficient"
    strategies:
      - "建立定期向上同步机制（周报/周会主动汇报进展与风险）"
      - "向上沟通前准备 3 要点：结论、依据、需要什么支持"
      - "学会要资源：把需求包装成对上级目标的投资而非成本"
      - "理解上级关注点，用上级的语言说话"
      - "刻意练习在冲突中表达不同意见（先认同再转折）"
    recent_progress: ""
    coaching_count: 0
  - area: "沟通表达"
    current_level: "developing"
    target_level: "proficient"
    strategies:
      - "结构化表达练习：所有输出先用结论-依据-行动三段式"
      - "控制信息密度：一次只传达一个核心观点 + 最多 3 个支撑论据"
      - "重要场合提前写提纲，不依赖临场发挥"
      - "练习电梯演讲：30 秒说清一件事"
      - "录音回听自己的表达，识别冗余和不清晰之处"
    recent_progress: ""
    coaching_count: 0
  - area: "管带与辅导"
    current_level: "developing"
    target_level: "proficient"
    strategies:
      - "固定 1v1 节奏（每 2 周一次），不因忙碌取消"
      - "给予具体可操作的反馈，而非笼统评价"
      - "学会放手：分配任务时说清目标和边界，过程不微操"
      - "建立团队仪式感（周会分享、里程碑庆祝）增强凝聚力"
      - "识别下属成长诉求，主动提供机会而非等下属提"
    recent_progress: ""
    coaching_count: 0
last_updated: "2026-04-26"
```

---

## Org Files

### `org/organization.md`
```yaml
company: "Hytech"
department: "大前端平台与架构部"
level: "部门负责人"
report_to: "郑焦"
total_reports: 30
org_description: "合约交易（CFD）技术服务公司，国内研发团队通过剥离主体、三方委派方式提供产研服务"
```

### `org/team-overview.md`
```yaml
teams: []
# Template:
# - name: ""
#   size: 0
#   lead: ""
#   tech_stack: []
#   current_focus: ""
#   health: ""  # green/yellow/red
#   last_updated: ""
```

### `org/stakeholders.md`
```yaml
stakeholders:
  - name: "郑焦"
    role: "大前端团队负责人（客户端+前端，150人）"
    relationship: "superior"
    communication_style: "待观察"
    influence_level: "high"
    notes: "公司国内研发团队元老（2022年创立时加入），与老板关系很好，传统IT出身，无大厂背景"
```

---

## Key Tension (Always Remember)

Sopaco's values say "坦诚清晰" but his default communication is "委婉间接" and
conflict style is "accommodate". In coaching, always help him find ways to be
**candid without being combative**.
