---
name: context-slimming
description: >
  Diagnose and optimize an OpenClaw agent workspace's injected context files (AGENTS.md, SOUL.md,
  USER.md, MEMORY.md, TOOLS.md, HEARTBEAT.md, etc.) to reduce per-round token consumption.
  Use when: user asks to reduce token usage, slim down workspace, optimize system prompt, audit
  context files, or when workspace *.md files have grown large and repetitive.
  Triggers on: "token 瘦身", "context slimming", "压缩上下文", "优化注入", "workspace 瘦身",
  "reduce injected tokens", "context audit".
---

# Context Slimming

压缩 OpenClaw 工作空间注入上下文，降低每轮对话基础 token 消耗。

核心思路：**顶层只留必需，细节按需加载，消除跨文件重复。**

---

## 原理

OpenClaw 将所有顶层 `*.md` 文件自动注入到每轮对话的系统提示中。
初始典型注入量约 25,000–32,000 tokens，其中 70%+ 可在不损失能力的前提下移除。

## 目标

| 阶段 | 典型注入 | 说明 |
|------|---------|------|
| 瘦身前 | 25k–32k | 含详细规则/范例/重复内容 |
| 结构拆分后 | 5k–8k | 详细规则 → skill 引用 |
| 文言化（可选） | 4k–6k | 中文描述古典化 |

## 执行流程

### Step 1: 全量扫描

```bash
# 列出所有顶层注入文件及大小 (bytes)
wc -c /path/to/workspace/*.md

# 列出总注入量
cat /path/to/workspace/*.md | wc -c
```

计算 token 估算：UTF-8 bytes / 4 ≈ tokens（英文）；中文 / 3 ≈ tokens。

### Step 2: 诊断

逐文件检查以下内容：

- [ ] **BOOTSTRAP.md** — 是否可删除？（首次运行完成后即应删除）
- [ ] **IDENTITY.md** — 是否可合并到 SOUL.md？（避免与 SOUL.md 重复）
- [ ] **跨文件重复** — 同一概念是否出现在多个文件中？（安全红线、记忆管理、主动性等）
- [ ] **详细操作指南** — 是否可移到 skill 引用？（安全审计流程、工作法详解等）
- [ ] **代码样例/脚本** — 是否可移到 `scripts/` 目录？（审计脚本、处理脚本等）
- [ ] **说明性文字** — 比喻、解释、范例是否必要？
- [ ] **模板残留** — 是否有未修改的模板文字？（如 "Customize this..."）

### Step 3: 结构拆分（最大贡献）

**顶层注入文件原则**：每文件 ≤ 1,500 bytes。只保留：
- 必须每轮知道的信息（身份、红线、启动流程）
- 指向其他资源的引用（"按需读 X"）

**移出内容**：
```
workspace/
├── AGENTS.md          # 只留：启动流程 + 安全红线表 + 技能索引
├── SOUL.md            # 只留：身份 + 原则 + 边界
├── USER.md            # 只留：用户画像摘要 + 沟通策略
├── MEMORY.md          # 只留：关键决策摘要 + 错误模式索引
├── TOOLS.md           # 只留：凭证位置 + 关键配置
├── HEARTBEAT.md       # 只留：心跳检查核心清单
├── rules/             # 详细操作规则（按需读）
│   ├── skill-audit.md
│   ├── memory.md
│   └── workflow.md
├── reference/         # 参考资料（按需读）
└── scripts/           # 可执行脚本（不注入）
```

AGENTS.md 中的技能引用格式：
```markdown
## 技能指引（按需读）

| 场景 | Skill | 触发 |
|------|-------|------|
| 安装审查 | skill-vetter | 装 skill 前 |
| 记忆管理 | memory-heat-system | 写/搜记忆 |
```

### Step 4: 去重复

建立"事实的唯一来源"清单。例如：

| 概念 | 唯一归属 | 他处处理 |
|------|---------|---------|
| 安全红线 | AGENTS.md | SOUL.md 只留原则级描述 |
| 记忆管理 | 见对应 skill | 其他文件只留一句话引用 |
| 主动性规则 | proactivity skill | 其他文件只留一句话引用 |

### Step 5: 删除模板/过期文件

- BOOTSTRAP.md（首次完成后删除）
- 重复的 IdenTITY.md（合并到 SOUL.md）
- 过期的 memory 文件
- 模板残留文字

### Step 6: 文言化（可选）

中文描述部分可文言化，压缩比约 3:1。
**不可压缩的**：命令、路径、工具名、表格代码。

示例：
- "不废话、不猜测" → "言必有据，不言无徵"
- "写下来，记忆会失效" → "笔之于书，胜于于心"
- "行不通？第 11 种方法" → "此路不通，另辟蹊径"

详见 [references/wenyan-patterns.md](references/wenyan-patterns.md)

### Step 7: 验证

```bash
# 瘦身后验证
wc -c /path/to/workspace/*.md
cat /path/to/workspace/*.md | wc -c

# 确认无语法问题（重启 agent 验证行为正常）
```

### Step 8: 提交变更

```bash
cd /path/to/workspace
git add -A
git commit -m "workspace: context slimming — structure + dedup + optional classical"
```

---

## 实战数据

一次完整瘦身实践的压缩效果：

| 文件 | 瘦身前 | 结构拆分后 | + 文言化 |
|------|--------|-----------|---------|
| AGENTS.md | 7,865 | 1,632 | — |
| SOUL.md | 3,074 | 746 | 746 |
| USER.md | 5,176 | 1,158 | 689 |
| MEMORY.md | 5,480 | 1,421 | 1,079 |
| HEARTBEAT.md | 3,247 | 626 | 416 |
| TOOLS.md | 3,107 | 354 | 297 |
| IDENTITY.md | 635 | 删除 | — |
| BOOTSTRAP.md | 1,471 | 删除 | — |
| **合计** | **30,055** | **5,937** | — |

**总压缩率：-80% 到 -86%**（含删除冗余文件）

---

## 检查清单

见 [references/slimming-checklist.md](references/slimming-checklist.md)

## 前后对照

见 [references/before-after.md](references/before-after.md)
