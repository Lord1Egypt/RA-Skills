# Agent Audit Log

## English

Agent systems are good at doing things, but they are often bad at leaving behind a clean record of what actually happened. A lot of important actions end up scattered across chat logs, shell output, git history, and half-remembered notes.

This skill is a lightweight way to fix that.

It is designed for assistants, personal automation systems, and agent workspaces that need a practical audit trail without turning into a heavyweight security product. The goal is simple: record the actions that really matter, keep the format structured, and make later review easier.

It is useful for tracking things like:

- installs and setup changes
- config edits and secret injection events
- system updates and maintenance actions
- repository creation, visibility changes, and history rewrites
- external publishing flows
- export-safety checks before public release
- unresolved follow-up risks and open items

The skill provides:

- a compact `SKILL.md`
- reference notes for schema, risk levels, export safety, open items, and examples
- a small initialization script that creates the audit directory and starter files

The structure stays intentionally lightweight: JSONL for raw facts, indexes for navigation, and a human-readable summary layer for fast review.

## 中文介绍

很多助手系统其实并不缺“做事能力”，缺的是一套清楚、持续、可回看的操作记录。真正重要的动作，常常散落在聊天记录、命令输出、git 提交和零碎备注里，过几天再回头看，就很难还原到底发生了什么。

这个 skill 想解决的，就是这个问题。

它不是那种很重的企业安全产品，也不是为了监控一切，而是给 AI 助手、个人自动化工作流和 agent 工作区准备的一套**轻量操作审计机制**。目标很直接：把真正值得记录的动作记下来，格式尽量统一，后面复盘时更容易看清。

它适合记录这些事情：

- 安装与环境配置
- 配置修改和 secret 注入
- 系统更新与维护动作
- 仓库创建、可见性调整、历史重写
- 外部发布流程
- 对外公开前的 export safety 检查
- 尚未处理完的风险和后续事项

这个 skill 提供的内容包括：

- 一个简洁的 `SKILL.md`
- 关于日志结构、风险分级、外发检查、open items 和示例的参考说明
- 一个初始化脚本，用来快速生成审计目录和基础文件

整个结构刻意保持轻量：用 JSONL 记录原始事实，用索引做导航，再补一层人类可读摘要，方便快速回看。
