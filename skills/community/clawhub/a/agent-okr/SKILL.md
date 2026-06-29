# Agent OKR Skill

> 为每个 Agent 制定和管理 OKR（Objective & Key Results），支持双层 Review。

## 核心概念

**Agent 的 OKR 跟人的不一样：**
- 人：季度 OKR，月度检查，精力有限
- Agent：**月度 OKR，周度检查，每日执行**
- Agent 执行速度极快，瓶颈不是时间而是方向

## 文件结构

```
docs/agent-profiles/{agent-name}.json   ← 每个Agent已有档案
docs/agent-okr/                          ← OKR 存放目录
  ├── {agent-name}.yaml                  ← 每个Agent的当前OKR
  ├── archive/                           ← 历史OKR归档
  └── README.md                          ← 本文件
```

## OKR YAML 格式

```yaml
agent: blog-agent
period: 2026-06           # 月度周期 YYYY-MM
status: active            # active / completed / archived
approved_by:              # 双层审批
  strategic: ceo-agent    # 龙虾合伙人审主线方向
  tactical: efficiency-agent  # 效率管家审任务粒度
  boss: pending           # 老板审周报（每周）

objective: 成为"AI Agent实践者"内容系列的核心产出者
mainline: 内容生产→发布→运营管线

key_results:
  - id: kr1
    description: 本月产出4篇高质量文章
    metric: 文章数
    target: 4
    current: 2
    unit: 篇
  - id: kr2
    description: 文章审稿通过率80%（1-2轮过）
    metric: 通过率
    target: 80
    current: 0
    unit: "%"
  - id: kr3
    description: 建立内容管线SOP并跑通一次完整流程
    metric: 跑通次数
    target: 1
    current: 0
    unit: 次

weekly_todos:              # Agent 自拆的周任务（每周更新）
  week_of: 2026-05-19
  tasks:
    - id: w1-1
      title: 写第3篇文章：我的38个AI Agent团队怎么运转
      status: pending
      from_kr: kr1
    - id: w1-2
      title: 梳理与笔探的协作SOP
      status: pending
      from_kr: kr3

weekly_report:             # 周报（Agent每周提交）
  week_of: 2026-05-19
  status: pending          # pending → submitted → approved
  summary: ""
  kr_progress: []
  blockers: []
  next_week_plan: []
  boss_review: ""          # 老板的审批意见
```

## 周报机制

### 流程

```
每周日晚上 Agent 自动生成周报
  → 提交到 docs/agent-okr/{agent-name}.yaml 的 weekly_report 字段
  → 龙虾合伙人审核（主线方向是否偏航）
  → 老板审批（必须过）
  → 效率管家根据审批结果调整下周任务
```

### 周报内容

| 字段 | 说明 |
|------|------|
| summary | 本周做了什么（3-5条） |
| kr_progress | 每个KR的进展（当前值变化） |
| blockers | 阻塞项（需要老板/其他Agent配合的） |
| next_week_plan | 下周计划（自拆的todo） |
| boss_review | 老板的审批意见（pass/adjust/stop） |

### Review 节奏

| 角色 | 审什么 | 频率 |
|------|--------|------|
| Agent 自己 | 自拆todo、执行、写周报 | 每日 |
| 效率管家 | 任务拆分粒度是否合理 | 每周 |
| 龙虾合伙人 | 方向是否偏离Agent主线 | 每周 |
| 老板 | 周报审批、大方向决策 | 每周 |

### 老板审批优先级

不是所有Agent的周报都要老板细看：
- **主线层 Agent**（8个）：老板逐条审批
- **探索层 Agent**：老板批量扫一眼，有问题的再细看
- **生活/基础设施层**：异常时才推给老板

## 脚本

### scripts/validate-okr.sh — 校验OKR文件格式
### scripts/generate-weekly-report-template.sh — 生成周报模板
### scripts/review-summary.sh — 汇总所有Agent的周报供老板审批

## 与平台的对接

当前用 YAML 文件管理，等 Agent 属性平台（60518a5c）和目标卡系统（6d78011f）开发完成后：
- OKR 数据迁入平台数据库
- Agent 通过 API 读取自己的 OKR
- 周报通过 API 提交和审批
- YAML 文件作为备份和离线查阅

## 维护人

- 龙虾合伙人（ceo-agent）：写OKR、审主线方向
- 效率管家（efficiency-agent）：审任务粒度、分配todo
- HR Agent：档案维护
