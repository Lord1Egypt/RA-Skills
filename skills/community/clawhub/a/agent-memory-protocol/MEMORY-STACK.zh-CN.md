# 记忆栈 — 外部工具与集成指南

<p align="center">
  <a href="MEMORY-STACK.md">English</a> · <a href="MEMORY-STACK.zh-CN.md">中文</a>
</p>

本文档描述配合 [Agent Memory Protocol](SKILL.md) 使用的完整记忆栈。Skill 定义**写什么**和**写哪里**；本文档说明**检索基础设施如何运作**以及**如何配置**。

---

## 架构概览

```
┌─────────────────────────────────────────────────────────┐
│                    Agent（LLM）                          │
│                                                         │
│  memory_search ──► qmd（向量+BM25 混合检索）              │
│  memory_get    ──► 直接读取文件                           │
│  lcm_grep      ──► LosslessClaw SQLite DAG              │
│  lcm_expand    ──► LosslessClaw 摘要树展开               │
└─────────────────────────────────────────────────────────┘
         │                          │
    ┌────▼──────┐           ┌───────▼──────┐
    │  qmd 索引  │           │  lcm.db      │
    │（SQLite +  │           │（SQLite DAG  │
    │  向量）    │           │  压缩摘要）   │
    └────┬──────┘           └──────────────┘
         │
    ┌────▼──────────────────────┐
    │  磁盘上的 Markdown 文件    │
    │  memory/  +  blackboard/  │
    └───────────────────────────┘
```

**两套独立系统，两个不同用途：**

| 系统 | 工具 | 索引内容 | 何时使用 |
|------|------|---------|---------|
| **qmd** | `memory_search` | `memory/` 和 `blackboard/` 下的 Markdown 文件 | 查事实、偏好、项目状态 |
| **LosslessClaw** | `lcm_grep` / `lcm_expand` | 历史对话的压缩摘要 | 从旧 session 中恢复决策 |

---

## 组件一：qmd（快速 Markdown 搜索）

### 功能

qmd 是 Markdown 文件的本地语义搜索引擎。对 `memory/` 和 `blackboard/` 目录建立混合索引（BM25 全文 + 向量 embedding）。`memory_search` 工具底层调用 qmd。

### 安装

```bash
# 推荐用 bun 安装
bun install -g @tobilu/qmd

# 或用 npm
npm install -g @tobilu/qmd
```

### 配置 collection

qmd 用 **collection** 定义索引哪些目录，一次性配置：

```bash
# 索引 memory 目录
qmd collection add memory-root-perlica /path/to/workspace/memory --pattern "**/*.md"

# 索引 blackboard
qmd collection add blackboard /path/to/workspace/blackboard --pattern "**/*.md"

# 验证
qmd collection list
qmd status
```

### 接入 OpenClaw

在 `openclaw.json` 中配置：

```json5
{
  "memory": {
    "backend": "qmd",
    "qmd": {
      "command": "/path/to/qmd",          // 运行 which qmd 获取路径
      "searchMode": "vsearch",            // "vsearch"（向量）或 "hybrid"
      "includeDefaultMemory": true,
      "update": {
        "interval": "5m",                 // 每 5 分钟重新索引
        "onBoot": true,                   // Gateway 启动时重建索引
        "waitForBootSync": false
      },
      "limits": {
        "maxResults": 10,
        "maxSnippetChars": 500
      },
      "scope": {
        "default": "allow"
      }
    }
  }
}
```

### 保持索引新鲜

Gateway 运行时 qmd 按 `interval` 自动更新。手动强制更新：

```bash
qmd update
qmd embed   # 如果向量 embedding 过期，重新生成
```

### Agent 如何使用

```
memory_search("项目截止日期")
  → qmd vsearch 扫描 memory/ + blackboard/
  → 返回 Top-N 片段（含文件路径 + 行号）
  → agent 调用 memory_get(path, from, lines) 读取具体内容
```

**搜索模式：**

| 模式 | 适用场景 |
|------|---------|
| `vsearch` | 默认 — 语义相似度，适合概念查找 |
| `query` | 研究类最佳 — 自动扩展 + 重排序 |
| `search` | BM25 关键词 — 精确词汇匹配 |

CLI 直接访问（调试用）：

```bash
qmd vsearch "项目截止日期"
qmd query "agent 使用什么模型" -c memory-root-perlica
qmd get qmd://memory-root-perlica/user/profile.md
qmd status
```

---

## 组件二：LosslessClaw（LCM）

### 功能

LosslessClaw 将 OpenClaw 默认的滑动窗口截断替换为 DAG 分层摘要系统。上下文满时，将较旧的对话压缩为摘要树，存储在本地 SQLite 数据库（`~/.openclaw/lcm.db`）中。内容不丢弃 — 压缩但不删除。

### 安装

```bash
# 通过 OpenClaw 插件系统安装
openclaw plugins install @martian-engineering/lossless-claw
```

### 在 OpenClaw 中配置

在 `openclaw.json` 的 `plugins.entries.lossless-claw` 下：

```json5
{
  "plugins": {
    "allow": ["lossless-claw"],
    "entries": {
      "lossless-claw": {
        "enabled": true,
        "config": {
          "summaryProvider": "anthropic",       // 摘要模型的 provider
          "summaryModel": "claude-haiku-4-5",   // 推荐用便宜快速的模型
          "freshTailCount": 32,                 // 最近 N 条消息保持原文不压缩
          "contextThreshold": 0.75,             // 上下文达到 75% 时触发压缩
          "ignoreSessionPatterns": [
            "agent:*:cron:**"                   // cron session 不压缩
          ],
          "incrementalMaxDepth": 10             // DAG 最大深度，超出强制全量汇总
        }
      }
    }
  }
}
```

**关键参数：**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `summaryModel` | — | 推荐 haiku 或 flash 等快速模型 |
| `freshTailCount` | 32 | 最近 N 条消息保持原文 |
| `contextThreshold` | 0.75 | 触发压缩的上下文占比阈值 |
| `ignoreSessionPatterns` | `[]` | 跳过压缩的 session 通配符 |
| `incrementalMaxDepth` | 10 | DAG 深度上限 |

### Agent 如何使用

LosslessClaw 暴露四个工具：

| 工具 | 功能 |
|------|------|
| `lcm_grep` | 在所有压缩摘要中做正则/全文搜索 |
| `lcm_describe` | 按 ID 查看特定摘要（sum_xxx） |
| `lcm_expand` | 展开摘要树，恢复细节 |
| `lcm_expand_query` | 针对问题展开相关摘要并给出聚焦回答 |

**检索流程：**

```
lcm_grep("微信插件修复")
  → 返回匹配的摘要 ID（sum_abc123）

lcm_expand(summaryIds=["sum_abc123"])
  → 返回该对话段的压缩内容

lcm_expand_query("触发符最终改成什么，为什么")
  → 委托子 agent 展开摘要并回答问题
```

**何时用 LosslessClaw vs qmd：**

| 场景 | 用哪个 |
|------|--------|
| 「用户对 X 的偏好是什么？」 | `memory_search` → qmd（搜 memory 文件） |
| 「上周那个 session 里决定了什么？」 | `lcm_grep` → `lcm_expand`（搜压缩对话） |
| 「当前项目状态如何？」 | `memory_search` → qmd（搜 blackboard） |
| 「为什么当时改了触发符？」 | `lcm_expand_query`（从旧对话中恢复推理过程） |

---

## 两套系统如何互补

```
信息生命周期：

  对话 ──► LosslessClaw 压缩 ──► lcm.db（可恢复）
    │
    │  （agent 将结构化事实写入 memory/ 文件）
    ▼
  memory/ 文件 ──► qmd 索引 ──► memory_search 检索
```

- **qmd** 管理**当前真相** — agent 写入 `memory/` 的结构化、精选事实
- **LosslessClaw** 管理**对话历史** — 过去 session 中的推理、讨论、决策（尚未正式写入 memory 文件的部分）

运转良好的 agent：
1. 将重要事实/决策写入 `memory/` 文件（永久、结构化）
2. 日常检索依赖 qmd
3. 需要从旧对话中恢复未正式记录的内容时，回退到 `lcm_grep`

---

## 维护

### qmd

```bash
# 检查索引健康状态
qmd status

# 强制重新索引（在 gateway 外修改了文件时运行）
qmd update

# 重建向量 embedding
qmd embed -f

# 查看已索引内容
qmd ls memory-root-perlica
qmd ls blackboard
```

### LosslessClaw

```bash
# 查看 lcm.db 大小
ls -lh ~/.openclaw/lcm.db

# 数据库随时间增长；OpenClaw 自动管理，无需手动维护
```

---

## 快速参考

| 我想... | 命令 / 工具 |
|---------|------------|
| 在记忆中查找事实 | `memory_search("query")` |
| 读取特定文件段落 | `memory_get(path, from, lines)` |
| 搜索旧 session 对话 | `lcm_grep("pattern")` |
| 恢复过去的某个决策 | `lcm_expand_query("X 当时决定了什么")` |
| 强制重建 qmd 索引 | `qmd update`（CLI） |
| 检查 qmd 健康状态 | `qmd status`（CLI） |
| 查看某条摘要 | `lcm_describe("sum_xxx")` |
