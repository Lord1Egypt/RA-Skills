---
name: dream-memory
description: >
  完整的工作区记忆管理系统。四层架构：文件存储 + OpenViking 向量引擎 + Ollama bge-m3 + Agent 规则。
  Use when: 用户询问记忆系统如何工作、如何安装记忆系统到新 Agent、记忆文件结构、向量检索原理、
  Session Flush 机制、长期记忆晋升规则、OpenViking 配置、bge-m3 参数调优、跨会话记忆丢失排查。
  也适用于为新 OpenClaw 实例部署完整记忆管理方案。
---

# Dream Memory — Agent 记忆管理系统

## 架构总览四层

```
第 1 层: Agent 规则 (AGENTS.md) — 何时写、写哪、怎么写
第 2 层: 文件存储 (Markdown)   — MEMORY.md + memory/ + WEEKLY-PROGRESS.md
第 3 层: 向量检索 (OpenViking)  — memory/ 目录的向量化索引
第 4 层: 会话生命周期           — sessions.json 追踪 + Session Start Check
```

## 文件结构（工作区根目录）

```
workspace/
├── AGENTS.md             # 操作规则（记忆写入逻辑在此）
├── MEMORY.md             # 长期记忆索引（< 200 行, < 25KB）
├── SOUL.md               # Agent 人格
├── USER.md               # 用户画像
├── WEEKLY-PROGRESS.md    # 本周进度表
├── memory/
│   ├── YYYY-MM-DD.md     # 每日日志（Append only）
│   ├── topics/           # 专题详情
│   ├── archive/          # 压缩归档
│   └── .data/            # OpenViking 数据
└── .consolidate-lock     # 蒸馏检查锁
```

## 实时记录规则

**何时写：** 用户纠正/偏好/目标/"记住"/报告完成/外部指针
**格式：** `- HH:MM 类型：内容`
**规则：** Append only，不修改历史行，跨日自动切换文件

## Session End Flush 🔥

触发：用户说"下班/再见"、>30 min 未写、心跳 >8h 未写、跨日切换

检查清单：重要决定 / 新知识 / 错误 / 待办 / MEMORY.md 超 4KB

输出格式：`## [日期] - 主题 (标签)` 每条 1-2 行

## Session Start Check 🔍

每次新会话启动时：
1. 读取 `~/.openclaw/agents/{agent-id}/sessions/sessions.json`
2. 找上一个用户会话的 `endedAt`
3. 对比当天日志最后修改时间
4. 日志时间 < endedAt → ❌ 补写

补写格式：`## [日期 HH:MM 补写] — 标题\n- 修复了什么\n- 补写原因`

详细配置（OpenViking + bge-m3 参数）→ 见 [references/ollama-setup.md](references/ollama-setup.md)
详细 Ollama 安装指南 → 见 [references/ollama-setup.md](references/ollama-setup.md)
自检脚本 → `scripts/memory-check.sh`
