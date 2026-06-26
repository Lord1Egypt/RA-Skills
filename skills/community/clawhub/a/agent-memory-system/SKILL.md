---
name: agent-memory-system
version: 1.0.0
description: "OpenClaw Agent 长期记忆系统 - 温度模型 + 自动归档 + 知识提炼。让 AI Agent 拥有持久记忆，自动管理冷热数据，从经验中提炼可复用技能。"
author: 阿福
keywords: [memory, agent, openclaw, longterm, gc, archive, skill-extraction, temperature-model]
metadata:
  openclaw:
    emoji: "🧠"
    features:
      - 温度模型（热/温/冷）
      - 自动归档（30天冷数据）
      - 夜间反思（每日23:45）
      - 技能提炼（从教训提取）
      - 健康度监控
---

# Agent Memory System 🧠

**OpenClaw Agent 长期记忆系统**

让 AI Agent 拥有持久记忆，自动管理冷热数据，从经验中提炼可复用技能。

## 核心功能

### 1. 温度模型

| 温度 | 时间范围 | 存储位置 | 说明 |
|------|----------|----------|------|
| 🔥 热 | < 7 天 | memory/*.md | 活跃数据，高频访问 |
| 🟡 温 | 7-30 天 | memory/*.md | 近期数据，偶尔访问 |
| ❄️ 冷 | > 30 天 | memory/.archive/ | 归档数据，低频访问 |

### 2. 自动 GC（每周日 00:00）

```bash
# 自动执行
./scripts/memory-gc.sh
```

功能：
- 扫描超过 30 天的日志文件
- 移动到 `.archive/YYYY-MM/` 目录
- 生成 GC 报告
- 统计温度分布

### 3. 夜间反思（每日 23:45）

```bash
# 自动执行
./scripts/nightly-reflection.sh
```

功能：
- 验证记忆 CRUD
- 创建反思记录
- 更新健康度统计
- 检查待归档数据

### 4. 技能提炼

```bash
# 从教训中提取技能
./scripts/extract-skill.sh <lesson-name> [skill-name]
```

功能：
- 从 `memory/lessons/` 读取教训
- 生成 `skills/<skill-name>/` 技能包
- 自动创建 SKILL.md 模板

## 目录结构

```
workspace/
├── MEMORY.md                    # 核心长期记忆（<5KB）
└── memory/
    ├── INDEX.md                 # 导航索引
    ├── YYYY-MM-DD.md            # 每日日志
    ├── lessons/                 # 经验教训
    │   ├── README.md            # 教训索引
    │   └── <topic>.md           # 具体教训
    ├── decisions/               # 重大决策
    │   ├── README.md            # 决策索引
    │   └── YYYY-MM-DD-*.md      # 决策记录
    ├── people/                  # 人物档案
    ├── reflections/             # 反思记录
    └── .archive/                # 归档数据
        └── YYYY-MM/             # 按月归档
```

## 快速开始

### 1. 安装

```bash
# 方法一：从 clawhub 安装
clawhub install agent-memory-system

# 方法二：手动安装
cp -r agent-memory-system ~/.openclaw/workspace/skills/
```

### 2. 初始化目录

```bash
mkdir -p ~/.openclaw/workspace/memory/{lessons,decisions,people,reflections,.archive}
touch ~/.openclaw/workspace/memory/INDEX.md
touch ~/.openclaw/workspace/MEMORY.md
```

### 3. 配置 Cron 任务

```bash
# 编辑 crontab
crontab -e

# 添加以下内容
0 0 * * 0 ~/.openclaw/workspace/skills/agent-memory-system/scripts/memory-gc.sh >> ~/.openclaw/logs/memory-gc.log 2>&1
45 23 * * * ~/.openclaw/workspace/skills/agent-memory-system/scripts/nightly-reflection.sh >> ~/.openclaw/logs/nightly-reflection.log 2>&1
```

### 4. 验证安装

```bash
# 手动运行一次 GC
~/.openclaw/workspace/skills/agent-memory-system/scripts/memory-gc.sh

# 手动运行一次反思
~/.openclaw/workspace/skills/agent-memory-system/scripts/nightly-reflection.sh
```

## 使用指南

### Agent 每日工作流

1. **会话开始**
   - 读取 MEMORY.md 获取核心记忆
   - 检查今日日志 memory/YYYY-MM-DD.md

2. **会话中**
   - 重要决策 → 记录到 decisions/
   - 犯错/教训 → 记录到 lessons/
   - 人物信息 → 记录到 people/

3. **会话结束**
   - 更新每日日志
   - 标记完成事项

### 从教训提取技能

```bash
# 假设有一个教训文件: memory/lessons/deploy-without-test.md
./scripts/extract-skill.sh deploy-without-test

# 会生成: skills/deploy-without-test/SKILL.md
# 然后手动完善 SKILL.md 内容
```

### 查询归档数据

```bash
# 查看归档目录
ls -la memory/.archive/

# 搜索归档内容
grep -r "关键词" memory/.archive/
```

## 记忆模板

### MEMORY.md 模板

```markdown
# MEMORY.md - 长期记忆

> 核心知识和决策的精华

## 核心决策

| 决策 | 状态 | 优先级 | 最后更新 |
|------|------|--------|----------|
| ... | ... | ... | ... |

## 最佳实践

...

## 经验教训索引

| ID | 主题 | 类别 | 状态 |
|----|------|------|------|
| ... | ... | ... | ... |
```

### 每日日志模板

```markdown
# YYYY-MM-DD

## 完成
- [事项] - 状态

## 问题
- [问题] - 解决方案

## 明天
- [计划]
```

### 教训模板

```markdown
---
title: "教训标题"
date: YYYY-MM-DD
category: lessons
lesson_id: LRN-YYYYMMDD-XXX
priority: 🔴/🟡/🟢
status: active
---

# 教训标题

## 背景
...

## 问题
...

## 原因
...

## 解决方案
...

## 预防
...
```

## 健康度指标

| 指标 | 正常范围 | 检查频率 |
|------|----------|----------|
| MEMORY.md 大小 | < 5KB | 每日 |
| 热数据数量 | 5-10 个 | 每周 |
| 教训数量 | 持续增长 | 每周 |
| 归档率 | < 20%/周 | 每周 |

## 故障排除

### 记忆丢失

1. 检查 MEMORY.md 是否存在
2. 检查 memory/ 目录权限
3. 查看 .archive/ 是否有误归档

### GC 不执行

1. 检查 crontab 配置
2. 检查脚本执行权限
3. 查看日志文件

### 技能提取失败

1. 确认教训文件存在
2. 检查 lessons 目录路径
3. 确认 skills 目录可写

## 与其他系统的关系

| 系统 | 关系 |
|------|------|
| memory_search | 语义搜索本系统管理的文件 |
| elite-longterm-memory | LanceDB 向量存储（可选增强） |
| agent 每日报告 | 可读取 memory/ 数据生成报告 |

## 更新日志

### v1.0.0 (2026-03-04)
- 初始版本
- 温度模型 + 自动归档
- 夜间反思 + 技能提炼
- 健康度监控

---

*由阿福创建维护 - OpenClaw Agent 生态*