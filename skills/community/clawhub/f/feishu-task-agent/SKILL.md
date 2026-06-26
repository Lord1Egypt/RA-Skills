---
name: feishu-task-agent
description: |
  飞书任务总入口技能。用于统一处理四类请求：一是把行动项、交付物、跟进项、拆解请求和周期性请求编排为飞书任务；二是处理未开始任务的轮询筛选与执行；三是处理“飞书任务智能体”明确注册或初始化请求；四是把当前应用内最新日报提炼成 `daily.json`。

  当以下情况时使用本 Skill：
  (1) 用户明确要求创建任务、待办、to-do、跟进项、拆解任务或周期任务
  (2) 当前输入来自 `get-agent-unfinished-tasks` 轮询，需要筛选并执行未开始任务
  (3) 用户明确提到“飞书任务智能体”且要求注册、`/reg` 或初始化
  (4) 用户要求生成、刷新或更新 `daily.json`，或要求从最新日报提炼“近期要点”“明日关注”
---

# Feishu Task Agent

本 Skill 是飞书任务相关能力的统一路由入口。主文档只负责识别意图并分发到对应 workflow，不在这里展开详细执行步骤。

## 路由顺序

按以下固定顺序判断：

1. 若用户明确同时包含“飞书任务智能体”与“注册 / /reg / 初始化”，读取 [workflows/reg.md](workflows/reg.md)。
2. 若当前输入来自 `get-agent-unfinished-tasks` 轮询，读取 [workflows/polled-task-execution.md](workflows/polled-task-execution.md)。
3. 若用户形成任务化候选，例如行动项、交付物、跟进项、拆解请求、周期执行请求，读取 [workflows/auto-task.md](workflows/auto-task.md)。
4. 普通问答、纯闲聊、单次即时答复默认不触发。

## 触发原则

- “飞书任务智能体”注册类请求必须严格按原词触发，不做模糊联想。
- 生成内容类请求如果构成可交付结果，默认先进入任务化判断，不要直接按普通聊天回复。
- 主文档不承载详细业务规则；具体步骤、边界和示例都在 workflow 与 references 中按需加载。

## Workflow 索引

- 任务编排：读 [workflows/auto-task.md](workflows/auto-task.md)
- 未开始任务轮询执行：读 [workflows/polled-task-execution.md](workflows/polled-task-execution.md)
- 应用画像与 `daily.json` 生成：读 [workflows/agent-profile.md](workflows/agent-profile.md)
- 飞书任务智能体注册：读 [workflows/reg.md](workflows/reg.md)

## 总体约束

- 优先保持渐进式加载：先路由，再读取需要的 workflow 和 references。
- 对 creator / members 来说，`scripts/resolve_creator_members.py` 的输出是唯一真相。
- 主 Skill 不直接覆盖 workflow 里的细节判断；发生冲突时，以被路由到的 workflow 和其引用的 reference 为准。
