# Output Templates

Use these templates as defaults. Compress only when the user explicitly wants a lighter result.

## 1) 中文 Executive Brief

```md
# Executive Brief

## 目标一句话
- 

## 解决的问题
- 

## 推荐 MVP
- 

## 为什么这样切
- 

## 现在不做什么
- 

## 关键风险
- 

## 推荐推进顺序
1. 
2. 
3. 
```

## 2) 中文 Design Brief

```md
# Design Brief

## 背景与问题定义
- 

## 用户 / 场景 / JTBD
- 

## 目标
- 

## 范围
- 

## 非目标 / 非范围
- 

## 功能拆解
- 

## 信息架构 / 数据流 / 状态流
- 

## 异常与边界条件
- 

## 依赖 / 约束 / 风险 / Trade-offs
- 

## 验收标准
- 
```

## 3) 中文 Phase Plan

```md
# Phase Plan

## Phase 0
- 目标：
- 最小交付物：
- 依赖：

## Phase 1
- 目标：
- 最小交付物：
- 依赖：

## Phase 2
- 目标：
- 最小交付物：
- 依赖：
```

## 4) English Canonical Context Blueprint

```md
# Canonical Context Blueprint

## Objective
- 

## Product Intent
- 

## Scope
- 

## Non-goals
- 

## Constraints
- 

## Existing Repo / System Context
- 

## Required Deliverables
- 

## Acceptance Criteria
- 

## Risks
- 

## Open Questions
- 

## Verification Plan
- 
```

## 5) English Codex Handoff

```md
# Codex Handoff

## Task
- 

## First Files To Read
- 

## Editable Boundaries
- 

## Do Not Change
- 

## Implementation Sequence
1. 
2. 
3. 

## Deliverables
- 

## Tests / Verification
- 

## Report Back With
- 
```

## 6) English Antigravity Handoff

```md
# Antigravity Handoff

## Mission
- 

## Architecture Reading Priorities
- 

## Product / Design Intent
- 

## Invariants / Guardrails
- 

## Recommended Phase Order
1. 
2. 
3. 

## Ambiguity Handling Rules
- 

## Verification Checkpoints
- 

## Report Back With
- 
```

## 7) Optional OpenClaw Work Packet

```md
# Work Packet: <name>

## Objective
- 

## Inputs
- 

## Boundaries
- 

## Expected Output
- 

## Done Criteria
- 

## Verification
- 

## Dependencies / Handoff Target
- 
```

## 8) Assumption / Decision Log

```md
# Assumption / Decision Log

## Facts
- 

## Assumptions
- 

## Unknowns
- 

## Decisions Already Made
- 

## Decisions Still Needed
- 
```

## Compression rules

If the user asks for a faster, lighter result:
- keep the section names,
- collapse bullets aggressively,
- do not remove `Scope`, `Non-goals`, `Acceptance Criteria`, or the fact/assumption separation.
