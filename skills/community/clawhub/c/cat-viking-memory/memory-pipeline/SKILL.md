---
name: memory-pipeline
description: 统一记忆存取工作流。基于 viking-memory-system 设计，支持 L0-L4 分层、遗忘算法、重要记忆保护。使用 Gemini CLI 调用 LLM 自动压缩记忆。
---

# memory-pipeline

统一记忆存取工作流，基于人类记忆层级衰减机制设计。

## 核心能力

1. **分层管理**：L0-L4 五层热度管理
2. **遗忘算法**：自动压缩降级（LLM 生成）
3. **重要记忆保护**：标记 important=true 不降级
4. **语义检索**：向量搜索支持
5. **自动降级**：每天凌晨 Gemini CLI 执行

## 记忆分层原则

| 层级 | 目录 | 时间 | 内容详细程度 | 触发方式 |
|------|------|------|-------------|---------|
| **L0** | hot/ | 0-1天 | 100%完整细节 | 自动 |
| **L1** | hot/ | 2-7天 | ~70%核心轮廓 | 自动 |
| **L2** | warm/ | 8-30天 | ~30%关键词 | 搜索触发 |
| **L3** | cold/ | 30-90天 | ~10%极简标签 | 搜索触发 |
| **L4** | archive/ | 90天+ | 0%归档 | 搜索可回忆 |

**注意：** 目录用 hot/warm/cold/archive，文件内容里标注 L0-L4 层级

## 记忆文件格式 (Frontmatter + Markdown)

```yaml
---
id: mem_20260314_001
title: "2026-03-14 今日工作"
importance: high        # low | medium | high
important: true         # 重要记忆，不降级
tags: [工作, 项目A]
created: 2026-03-14T10:30:00Z
last_access: 2026-03-14T14:22:00Z
access_count: 5
retention: 90
current_layer: L0
level: 0
weight: 14.2
---

# 今日工作 [L0]

## 背景
...

## 过程
...

## 结果
...

## 待办
- [ ] ...
```

## 权重计算公式

```
W = importance_factor × (1/(days+1)^0.3) × (access_count+1)
```

- importance_factor: high=2.0, medium=1.0, low=0.5
- days: 距创建天数
- access_count: 访问次数

## 自动重要性判断

**存储时自动检测：**

| 关键词 | importance | important |
|--------|-----------|-----------|
| 董事长、决策、关键、bug、错误、交付、会议 | high | - |
| 待办事项 | medium | - |
| 董事长、紧急、致命、严重、支付、账号、密码、面试 | - | true (不降级) |

**手动指定：**
```bash
# 手动指定重要性
mp_store --content "..." --importance high --title "xxx"

# 手动标记重要（不降级）
mp_store --content "..." --important --title "xxx"
```

### 写入规范

**L0 层（0-1天，完整记录）：**
```markdown
# 任务标题 [L0]

**层级**: L0 | **创建时间**: YYYY-MM-DD HH:MM

**标签**: xxx, yyy

---

## 背景
（完整任务背景和目标）

## 过程
（详细执行过程和关键步骤）

## 决策
（所有决策及原因）

## 结果
（完整任务结果和产出）

## 待办
- [ ] 待办1
- [ ] 待办2
```

**L1 层（2-7天，核心轮廓）：**
```markdown
# 任务标题 [L1]

**层级**: L1 | **创建时间**: YYYY-MM-DD

**标签**: xxx

---

核心轮廓：xxx
结果：xxx
```

**L2 层（8-30天，关键信息）：**
```markdown
# 任务标题 [L2]

**层级**: L2 | **标签**: xxx

关键词：xxx, xxx
结果：xxx
```

**L3 层（30-90天，极简标签）：**
```markdown
# 任务标题 [L3]
**标签**: xxx, yyy
```

**L4 层（90天+，归档）：**
```markdown
# 任务标题 [L4]
```

## 使用场景

### 场景 1：存储重要记忆

当需要存储重要数据到长期记忆时，必须使用此 skill：

```python
# 错误的做法（直接写入）
sv_write("viking://agent/memories/hot/today.md", "# 任务...")

# 正确的做法（使用 memory-pipeline）
# 自动完成：ontology 映射 → Viking 存储 → 索引更新
# 按热度存储：hot/ 7天内, warm/ 7-30天, cold/ 30天+
```

### 场景 2：检索记忆

当需要从长期记忆中检索信息时：

```python
# 使用 memory-pipeline 检索
sv_find("董事长偏好")
# 或
sv_read("viking://agent/memories/config.md")
```

## 工作流程

```
存储流程：
┌─────────────┐    ┌──────────────┐    ┌────────────┐    ┌──────────┐
│ 输入数据     │ → │ Ontology 映射 │ → │ Viking 存储 │ → │ 索引更新 │
└─────────────┘    └──────────────┘    └────────────┘    └──────────┘

检索流程：
┌─────────────┐    ┌────────────┐
│ 搜索关键词   │ → │ Viking 查询 │
└─────────────┘    └────────────┘
```

## 快速使用

### 存储记忆

```bash
# 使用 pipeline 存储（推荐）

# L0 层 - 完整记录 0-1天（默认）
mp_store --content "背景: xxx\n过程: xxx\n结果: xxx" --title "任务标题" --tags "工作" --tier L0

# L1 层 - 核心轮廓 2-7天
mp_store --content "核心轮廓: xxx\n结果: xxx" --title "任务标题" --tier L1

# L2 层 - 关键词 8-30天
mp_store --content "关键词: xxx\n结果: xxx" --title "任务标题" --tier L2

# L3 层 - 标签 30-90天
mp_store --content "标签: xxx" --title "任务标题" --tier L3

# L4 层 - 归档 90天+
mp_store --content "标题" --title "任务标题" --tier L4
```

### 检索记忆

```bash
# 语义搜索
sv_find "猫经理 偏好"

# 读取指定记忆 (按热度层级)
sv_read "viking://agent/memories/config/config.md"
sv_read "viking://agent/memories/hot/today.md"

# 列出所有记忆
ls -la ~/.openclaw/viking-*/agent/memories/
```

## 工具

| 工具 | 描述 |
|------|------|
| `mp_store` | 一键存储（自动添加 frontmatter + 生成向量嵌入） |
| `mp_search` | 语义搜索已存储的记忆 |
| `mp_tier_gemini` | 使用 Gemini CLI 执行自动降级（包含遗忘算法） |
| `memory-embed` | 向量化管理（嵌入、搜索、重建） |

## 向量搜索

### 存储时自动向量

每次 `mp_store` 会自动：
1. 写入 Markdown 文件（含 Frontmatter 元数据）
2. 调用 Ollama embedding 模型生成向量
3. 存储到 `.viking_vectors.json` 索引

### 语义搜索

```bash
# 语义搜索记忆
~/.openclaw/skills/memory-pipeline/scripts/memory-embed.sh search "董事长偏好" ~/.openclaw/viking-maojingli 5

# 重建向量库
~/.openclaw/skills/memory-pipeline/scripts/memory-embed.sh rebuild ~/.openclaw/viking-maojingli

# 测试向量服务
~/.openclaw/skills/memory-pipeline/scripts/memory-embed.sh test
```

## 自动保存机制

### 触发条件

**关键词触发**（自动保存）：
- 完成、解决、修复、创建、更新、修改、删除
- 提交、部署、测试、验证、确认、通过

**会话结束**（自动保存）：
- 调用 `memory-session-hook.sh` 自动保存会话摘要

### 使用方式

```bash
# 1. 自动保存（关键词触发）
~/.openclaw/skills/memory-pipeline/scripts/memory-auto-save.sh save "内容" "标题"

# 2. 检查是否需要保存
~/.openclaw/skills/memory-pipeline/scripts/memory-auto-save.sh check "内容"

# 3. 监听模式（持续监听输入）
~/.openclaw/skills/memory-pipeline/scripts/memory-auto-save.sh monitor

# 4. 会话结束钩子
~/.openclaw/skills/memory-pipeline/scripts/memory-session-hook.sh "会话摘要"
```

### 配置 OpenClaw 钩子

在 agent 配置中添加：
```yaml
hooks:
  on_session_end:
    - name: "自动保存记忆"
      command: "~/.openclaw/skills/memory-pipeline/scripts/memory-session-hook.sh"
```

**每天凌晨 3 点自动执行**（通过 cron 调用 Gemini CLI）：

```
0 3 * * * ~/.openclaw/skills/memory-pipeline/scripts/memory-tier-gemini.sh
```

### 遗忘算法流程

```
1. 扫描 hot/ 目录
2. 检查元数据 (current_layer, created, important)
3. 如果 important: true → 跳过降级
4. 根据时间判断是否需要降级：
   - L0 (0-1天) → L1: LLM 生成 100 字轮廓
   - L1 (2-7天) → L2: LLM 提取 5 个关键词
   - L2 (8-30天) → L3: LLM 提取 3 个标签
   - L3 (30-90天) → L4: 仅保留标题
5. 更新 frontmatter (current_layer, level, weight)
6. 在文件末尾添加压缩内容
```

### 手动执行

```bash
# 使用 Gemini CLI 执行降级
~/.openclaw/skills/memory-pipeline/scripts/memory-tier-gemini.sh
```

## 配置

默认使用当前 Agent 的 Viking workspace：
- 猫经理：`~/.openclaw/viking-maojingli/`
- 猫小咪：`~/.openclaw/viking-maoxiami/`
- 猫工头：`~/.openclaw/viking-maogongtou/`
- 猫助理：`~/.openclaw/viking-maozhuli/`

全局共享：`~/.openclaw/viking-global/`

## 重要规则

> **强制要求**：所有重要数据存储必须使用 memory-pipeline，确保数据经过 ontology 映射规范化后再存入 Viking。

这样可以：
1. 保证数据格式统一
2. 便于跨 Agent 检索
3. 建立统一的知识图谱

---

*此 skill 封装了 ontology-viking-workflow 和 simple-viking，确保记忆存取流程规范化。*
