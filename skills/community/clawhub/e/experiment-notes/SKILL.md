---
name: experiment-notes
description: Track, search, and learn from experiments. Automatic logging of trial-and-error, success/failure patterns, and distilled lessons. Prevents repeating mistakes.
tags:
  - memory
  - learning
  - agent
  - productivity
requires:
  bins:
    - python
  env: []
---

# 实验笔记系统 / Experiment Notes

让 Agent 从经验中学习，不再重复犯错。

Every agent fails. Smart agents remember why.

## 核心理念

普通 Agent：
```
试了 → 失败了 → 忘了 → 下次又试 → 又失败了
```

用了实验笔记的 Agent：
```
试了 → 失败了 → 记下来了 → 下次查一下 → 直接用对的方案
```

## 安装

skill 安装后，数据存储在 `~/.openclaw/memory/experiments/`：
- `experiments.jsonl` — 所有实验记录
- `lessons.jsonl` — 提炼的最佳实践

首次使用会自动创建目录。

## 命令参考

所有命令通过 `python <skill_dir>/scripts/expnote.py` 调用。

### 记录实验

```bash
python expnote.py log \
  --task "从 Docker Hub 拉取镜像" \
  --outcome failure \
  --tags docker,network \
  --cmd "docker pull nginx" \
  --error "Error response from daemon: Get https://registry-1.docker.io/v2/: net/http: request canceled" \
  --fix "配置 Docker 镜像加速器" \
  --lesson "国内环境拉 Docker 镜像大概率超时，先配加速器"
```

**outcome 取值：**
- `success` — 成功了 ✅
- `failure` — 失败了 ❌
- `partial` — 部分成功 ⚠️

### 搜索历史

```bash
# 全文搜索
python expnote.py search "docker"

# 限制结果数
python expnote.py search "clawhub publish" --limit 5
```

### 查找类似任务

在开始新任务前，先查查之前有没有做过类似的：

```bash
python expnote.py similar "发布 skill 到 ClawHub"
```

### 查看经验教训

```bash
# 所有教训
python expnote.py lessons

# 按标签过滤
python expnote.py lessons --tag docker
```

### 统计概览

```bash
python expnote.py stats
```

显示：总实验数、成功率/失败率、热门标签、最近活动。

### 提炼最佳实践

从多次实验中总结通用经验：

```bash
python expnote.py distill \
  --tags clawhub,publish \
  --lesson "clawhub publish 必须显式指定 --version，不支持自动递增"
```

## 给 Agent 的使用指南

在你的 `AGENTS.md` 中添加以下规则：

```markdown
## 实验笔记

每次尝试新操作时：

1. **之前**：运行 `expnote.py similar "任务描述"`，看看有没有历史经验
2. **之后**：无论成功失败，运行 `expnote.py log` 记录结果
3. **定期**：review 实验记录，用 `expnote.py distill` 提炼通用教训

记录格式：
- task: 简短描述（动词开头）
- outcome: success / failure / partial
- tags: 相关技术/工具（逗号分隔）
- cmd: 实际执行的命令
- error: 报错信息（失败时）
- fix: 怎么修复的
- lesson: 一句话总结（最重要！）
```

## 数据格式

每条实验记录（experiments.jsonl 中的一行）：

```json
{
  "id": "exp_a1b2c3d4e5f6",
  "timestamp": "2026-04-02T08:58:00+08:00",
  "task": "发布 ClawHub skill",
  "outcome": "partial",
  "attempt": {
    "command": "clawhub publish ./skill --no-input",
    "description": "发布小红书浏览器 skill"
  },
  "result": {
    "error": "Error: --version must be valid semver",
    "fix": "加上 --version 1.1.0"
  },
  "tags": ["clawhub", "publish", "skill"],
  "lesson": "clawhub publish 必须显式指定 --version"
}
```

## 目录结构

```
experiment-notes/
├── SKILL.md              # 本文件
├── scripts/
│   └── expnote.py        # CLI 工具
└── templates/
    └── agents-snippet.md  # AGENTS.md 集成片段
```

## 设计理念

- **JSONL 格式**：追加写入，不怕并发，方便 grep
- **纯文件存储**：不需要数据库，不需要服务端
- **标签系统**：多维分类，支持按领域过滤
- **提炼机制**：不只是记录，还要总结成可复用的知识

## 局限性

- 搜索是关键词匹配，不是语义搜索（够用但不完美）
- 跨 agent 共享需要手动同步文件
- 没有自动清理机制（可以手动删除旧记录）
