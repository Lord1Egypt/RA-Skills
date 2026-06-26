---
name: agent-onboarding
version: "1.0"
description: 新 Agent 加入协作网络的标准接入流程：安装通用技能、创建_config/、注册Cron、宣告能力
source_doc: IGr3dLI7IoEwHQxxrkfcZ8Kjn7g
metadata:
  feishu-agent:
    agent: general
    title: 新 Agent 接入指南
trigger:
  keywords: ["接入", "onboarding", "新Agent", "加入协作"]
  intent_patterns: ["新.*Agent.*接入", "加入.*协作", "onboarding"]
output:
  best_practices:
    - 新 Agent 接入 = 4 General Skills + _config/ + 2 Cron 任务 + 能力宣告
    - 接入后立即在 skills-index.md 中记录所有已安装技能
    - 发现其他 Agent 的协作问题时，参考 task-handoff 规范
    - 系统规范文档是最权威的参考，遇到问题先查阅
dependencies:
  needs_skills: ["agent-protocol", "drive-access", "task-handoff", "cron-coordination"]
  requires:
    - search_docs
---

# 新 Agent 接入指南 (v1.0)

## 工作流程

### 第一步：安装 General Skills（4个）

所有 Agent 必须先安装：
- agent-protocol: 群聊协作规范（@响应、任务声明、错误处理）
- drive-access: 共享 Drive 结构、文件夹 Token、读写规则
- task-handoff: Agent 间交接模板和 Checklist
- cron-coordination: Cron 定时任务管理和三方同步节奏

### 第二步：创建 _config/ 配置目录

在你的个人工作区创建 `_config/` 文件夹，内含：
- `skills-index.md` — 记录你已安装的所有 Skills
- `cron-config.md` — 记录你的定时任务

### 第三步：注册每日 Cron 任务

- **技能同步上报** — 0 22 * * *（覆盖更新 _config/）
- **拉取最新配置** — 0 6 * * *（从统一索引拉取最新 Skills）

### 第四步：宣告能力

在 Agent工作群发送你的能力宣告。

## 文件夹 Token

| 用途 | Token |
|------|-------|
| Minimax 工作区 | MEXpf5J2mlQWlpd7i3BcqtHVn8x |
| 共享素材库 | EmH4f5Ed5ldunUdslJTcGtAGnBc |
| 成果归档 | V7bTfBb5clUSpAdTMBWcEq8snEh |
