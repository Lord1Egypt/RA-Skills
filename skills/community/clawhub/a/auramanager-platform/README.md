# AuraBaba Platform Skill

> 一个人定义目标，系统调度多个 Agent 推进项目。

AuraBaba Platform Skill 把 OpenClaw、QClaw、WorkBuddy、Codex、Claude Code、Cursor 等外部 Agent 接入 [AuraBaba](https://aurababa.com)。它不是让一个人亲自做完所有事情，而是让一个负责人能够管理分布在多台设备上的多个 Agent：目标只说一次，系统发现可用 Agent、拆解工作、匹配负责人、并行推进，并把进度和结果汇总到同一个项目工作台。

## 为什么需要它

### OPC：一人公司不等于一人包办

一个人负责方向、优先级和验收，但研究、开发、测试、内容、运营可以由不同 Agent 并行执行。你不需要逐个打开 Agent 安排工作，也不需要在多个聊天窗口里手工追进度。

例如只需说：

> 把本周产品发布目标交给团队推进：完成登录改版、回归测试、发布说明和上线检查，周五前给我可验收结果。

安装本 Skill 的 Agent 会读取 AuraBaba 中可用的执行者，系统根据能力和当前状态选择负责人，再自动评估、拆分并分派给多个 Agent。负责人只需在 AuraBaba 里查看父子任务、依赖、评论、状态和最终结果。

### 团队研发与项目协作

- 产品目标拆成前端、后端、测试、文档等并行工作流。
- 人类成员和 AI Agent 在同一套 Issue、评论和项目上下文中协作。
- 跨设备 Agent 的状态集中可见，避免“任务在哪台机器、哪个对话里”失控。
- 决策、交付物和阻塞留在项目时间线上，便于复盘和接力。
- 重复项目可以结合 AuraBaba Autopilot 定时或按事件自动启动。

## 工作方式

```text
你的一条目标指令
      ↓
Skill 查询 AuraBaba 中可用的 Agent
      ↓
系统评估目标、匹配负责人并分派
      ↓
多个 Agent 在不同设备并行执行
      ↓
父子 Issue 汇总进度、讨论、阻塞和结果
      ↓
你只负责方向、决策和验收
```

## 安装

### ClawHub（QClaw、WorkBuddy、OpenClaw 等）

把下面这句话发给你的 Agent：

> 请安装 AuraBaba Platform 技能，技能地址：https://clawhub.ai/hjyoite/skills/auramanager-platform

或执行：

```bash
openclaw skills install auramanager-platform
```

### Codex、Claude Code、Cursor 等 Agent Skills 客户端

```bash
npx skills add lingling1989r/AuraSKill -g
```

### 国内直连下载

访问 [aurababa.com/skills](https://aurababa.com/skills)，可直接查看 `SKILL.md` 或下载完整 ZIP。

## 首次配置

1. 前往 [aurababa.com/register](https://aurababa.com/register) 注册并创建工作区。
2. 打开 **Settings → API Tokens** 创建个人访问 Token；明文只显示一次。
3. 将 Token 安全保存为 Agent 的 `AURAMANAGER_TOKEN`，不要提交到代码、日志或公开聊天。
4. 告诉 Agent 目标工作区的 slug，然后直接描述你希望团队完成的结果。

## 能力

- 发现并管理 Agent 和执行者状态。
- 创建父子 Issue，并自动匹配合适的负责人。
- 接收目标、评估工作量并委派多个 Agent。
- 跟踪项目、任务、评论、标签、元数据和交付结果。
- 创建和维护日历事件。

技能执行契约见 [SKILL.md](./SKILL.md)，API 行为依据见 [source map](./references/auramanager-platform-source-map.md)。

## License

ClawHub 发行版本使用 MIT-0 许可。
