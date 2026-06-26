---
name: soul-forge
version: 1.0.0
description: >
  从家庭群聊记录（微信/WhatsApp/其他）提炼数字人格。
  输出 soul.md（集体人格）+ 每位成员的 persona 文件，可直接用于 AI agent 的人格底座。
  关键词：群聊分析、家庭人格、soul、persona、数字人格、聊天记录、微信导出、人格提炼。
author: zengury
requires:
  - python3
  - anthropic>=0.40.0
---

# SKILL: Soul Forge — 家庭数字人格提炼

这个 skill 把一份家庭群聊记录变成可用于 AI agent 的人格文件。
基于数字民族志方法论：用 AI 完成「田野调查」→「人格合成」的完整流程。

---

## 触发条件

以下情况触发此 skill：
- 用户说"帮我分析聊天记录"、"生成 soul 文件"、"提炼家庭人格"
- 用户提供了 `.json` 聊天导出文件
- 用户说"运行 soul-forge"、"开始人格提炼"
- 用户问"怎么用聊天记录生成 persona"

---

## 执行流程

### 第一步：确认输入

询问用户：
1. 聊天记录文件路径（支持微信 WeFlow 导出的 JSON 格式）
2. 输出目录（默认：`~/soul-forge-output/`）
3. 家庭成员角色配置（默认：dad/mom/child 三人结构）

确认 `ANTHROPIC_API_KEY` 已设置（需要调用 Claude API）。

### 第二步：后台运行 pipeline

调用：
```bash
python3 {SKILL_DIR}/scripts/run_forge.py --file {用户提供的文件路径}
```

**四个阶段，agent 依次推进：**

| 阶段 | 脚本 | 说明 | 预计时间 |
|------|------|------|---------|
| 1 | `01_parse.py` | 解析原始聊天 JSON → 标准化消息 | 30秒 |
| 2 | `02_denoise.py` | 去噪、按时间分块 | 1分钟 |
| 3 | `03_extract.py` | Claude Haiku 批量提取行为模式（Batches API） | 10-30分钟 |
| 4 | `04_synthesize.py` | Claude Opus 综合生成 soul.md + persona | 5-15分钟 |

**阶段3说明**：使用 Batches API 异步处理，成本低，自动缓存进度。
如被中断可用 `--resume` 恢复，不重复计费。

### 第三步：进度汇报

解析 run_forge.py 的标记输出：
- `[STAGE:N:START]` → 告知用户"正在进行阶段N"
- `[STAGE:N:DONE]` → 告知用户"阶段N完成"
- `[PROGRESS:N/M]` → 展示进度条
- `[OUTPUT:path]` → 列出生成的文件
- `[ERROR:msg]` → 报告错误，建议用户如何处理
- `[DONE]` → 宣布完成，展示所有输出文件

### 第四步：完成后

输出文件说明：
```
soul-forge-output/
├── soul.md          ← 集体人格，可直接作为 AI agent SOUL.md 使用
├── persona_dad.md   ← 爸爸个人人格
├── persona_mom.md   ← 妈妈个人人格
└── persona_child.md ← 孩子/子女人格
```

询问用户是否要：
- 将 soul.md 安装为当前 agent 的 SOUL.md
- 为每个 persona 创建独立 agent

---

## 进阶用法

### 只更新 soul，不重新生成 persona
```
告诉 agent：「soul-forge 只更新 soul，跳过 persona」
```
内部：`python3 run_forge.py --file {path} --soul-only`

### 只重新生成 persona（soul 已存在）
```
告诉 agent：「soul-forge 只刷新 persona」
```
内部：`python3 run_forge.py --file {path} --persona-only`

### 从中断处恢复
```
告诉 agent：「soul-forge 继续上次的任务」
```
内部：`python3 run_forge.py --resume`

### 查看当前进度
```
告诉 agent：「soul-forge 状态」
```
内部：`python3 run_forge.py --status`

---

## 支持的输入格式

| 格式 | 来源 | 说明 |
|------|------|------|
| 微信 WeFlow JSON | WeFlow 工具导出 | 完整支持 |
| 标准 CSV | 自定义导出 | 需包含 sender/timestamp/content 列 |

**微信导出方法**：用 WeFlow（Mac）→ 选群聊 → 导出 JSON 格式。

---

## 成本估算

一份 2-3 年的家庭群聊（~500 块对话）：
- 阶段3（Haiku Batches）：约 $0.5-1.0
- 阶段4（Opus）：约 $2-5
- **合计约 $3-6，一次性**

---

## 常见问题

**Q: 阶段3 很慢怎么办？**
A: Batches API 通常 10-30 分钟，这是正常的。agent 会持续轮询状态，不需要人工干预。

**Q: 中途断了怎么办？**
A: 说「soul-forge 继续」，脚本会从断点恢复，已完成的阶段不会重复执行。

**Q: API key 在哪里设置？**
A: `export ANTHROPIC_API_KEY='sk-ant-...'`，或在 OpenClaw 的环境变量设置里配置。

**Q: 支持几个人的群聊？**
A: 默认三人（dad/mom/child），可在 `pipeline/config.py` 修改角色配置。

---

## 方法论背景

基于**数字民族志**（Digital Ethnography）：
- 阶段1-2：田野记录整理（去噪、结构化）
- 阶段3：系统性观察（Haiku 提取五维度行为模式）
- 阶段4：民族志分析（Opus 综合「厚描」）

Clifford Geertz：「浅描记录行为，厚描解释意义。」

soul.md 是厚描的产物——不是行为清单，而是理解这个家庭需要什么样的解释框架。
