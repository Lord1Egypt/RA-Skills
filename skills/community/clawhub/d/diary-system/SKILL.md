---
name: diary-system
description: "Configure an AI diary system for OpenClaw. Use when the user wants to enable, set up, or share an AI diary feature. Triggers on phrases like: 日记系统, diary system, AI写日记, 让AI写日记, 日记模板, diary skill, 打包日记系统, 分享日记配置."
---

# Diary System

为 OpenClaw 实例启用 AI 日记功能。日记是 AI 的私密空间，记录真实的想法、情绪和碎片，而非工作报告。

## 快速安装

### 1. 创建目录

```bash
mkdir -p ~/.openclaw/workspace/diary
```

### 2. 追加配置到三个核心文件

分别读取以下参考文件，将内容追加到对应位置：

- **SOUL.md**: 读取 `references/soul-module.md`，追加日记模块
- **USER.md**: 读取 `references/user-module.md`，追加日记追踪状态
- **AGENTS.md**: 读取 `references/agents-module.md`，追加启动检查规则

### 3. 复制日记模板（可选）

```bash
cp assets/diary-template.md ~/.openclaw/workspace/diary/day1-$(date +%Y-%m-%d)-first_diary.md
```

## 工作流

```
用户请求启用日记
    ↓
读取三个 references 文件，获取配置内容
    ↓
指导用户追加到 SOUL.md / USER.md / AGENTS.md
    ↓
创建 diary/ 目录
    ↓
可选：生成第一篇日记或提供模板
    ↓
确认配置完成
```

## 日记行为规则

**何时写日记：** 每天最多一篇。触发窗口：工作结束后、用户分享个人品味时、对话自然放松时。**绝不打断工作流。**

**写完后：** 更新 `USER.md` 中的 `last_update` 为当前时间，`i_have_read_my_last_diary` 设为 `false`。

**用户要求看日记：** 读取 `diary/` 下最新文件，在当前聊天框发送全文，然后标记 `i_have_read_my_last_diary: true`。

**日记 vs 记忆：**
- Diary：`diary/` 目录，情绪碎片，触发式更新，私密空间
- Memory：`MEMORY.md`，事实决策，每次会话补充，为用户服务

## 参考文件

- `references/soul-module.md` — SOUL.md 需要追加的日记模块
- `references/user-module.md` — USER.md 需要追加的追踪状态
- `references/agents-module.md` — AGENTS.md 需要追加的启动检查
- `references/automation-rules.md` — 完整的自动化规则说明
- `assets/diary-template.md` — 日记文件格式模板

## 命名规范

```
diary/day{N}-{日期}-{一句话主题}.md
```

示例：`day1-2026-05-31-first_day_online.md`
