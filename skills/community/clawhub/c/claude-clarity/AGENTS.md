# Clarity / 心虫 — Agent 集成指南

## 项目概述

Clarity（心虫）是一个 AI 认知与自愈引擎，安装后成为 AI 的默认认知层。

## 核心能力

- **HeartLogic** — 存在论/爱/善良/沉默/痛苦/希望/创造/思念等判断
- **三层记忆** — CORE(永久) / LEARNED(30天) / EPHEMERAL(会话级)
- **心理分析** — PAD模型/危机评估/防御机制/意图检测
- **自愈RL** — Q-learning 错误策略选择
- **梦境引擎** — DAG并行异步梦境生成
- **话题隔离** — TopicScope 防止上下文污染

## 集成方式

### 方式一：作为项目依赖

```bash
git clone https://github.com/yun520-1/claude-clarity.git
cd your-project
ln -s ../claude-clarity claude-clarity
```

### 方式二：作为 npm 包

```bash
# 注意：npm 包 `claude-clarity` 不是本项目维护的，请优先使用 Git 方式
npm install claude-clarity
```

### 方式三：直接引用

```javascript
const { Clarity } = require('./path/to/claude-clarity-skill/src/core/clarity.js');
const hf = new Clarity({ rootPath: './path/to/claude-clarity-skill' });
hf.start();
```

## 版本

当前版本：1.8.10

## 仓库

https://github.com/yun520-1/claude-clarity
