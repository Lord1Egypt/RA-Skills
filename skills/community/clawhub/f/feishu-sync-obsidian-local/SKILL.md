---
name: feishu-sync-obsidian
description: >
  将飞书 Wiki 文档同步到 Obsidian PARA 知识库。
  触发：当用户说"同步飞书"或"同步文档"时使用。
  遵循 Pipeline 模式，4 步顺序执行，带硬检查点。
  必需文件：vault 根目录必须有 SYNC-RULES.md。
metadata:
  pattern: pipeline
  steps: "4"
---

# Feishu → Obsidian PARA Sync

> **模式：Pipeline** | 数据源和目标路径从 SYNC-RULES.md 读取

---

## 核心设计

**内容获取由 Agent 的 feishu_fetch_doc 工具完成，Python 脚本只做路径构建和文件写入。**
这样无需在脚本里管理 Access Token，也不需要在 clawhub 发布时携带敏感权限。

---

## 硬性规则

**禁止跳过步骤。禁止在用户确认前进入下一步。**

---

## Step 1 — 前置检查 + 获取 Wiki 节点（并行遍历）

**触发**：用户要求同步飞书文档

### 1a. 前置检查
1. 检查 vault 根目录是否存在 `SYNC-RULES.md`
   - 不存在 → 触发初始化流程
2. 读取 `SYNC-RULES.md` 中的「数据源」表格

### 1b. 获取 Wiki 根节点
使用 `feishu_wiki_space_node` 工具获取每个 Wiki 的根节点。

### 1c. 并行遍历子节点
对于 `has_child: true` 的节点，**并行**获取子节点：
- 每个 has_child 节点分配一个并行任务
- 各分支同时请求，不等待串行
- 递归直到所有分支都没有子节点

```
个人成长 (root)
├── 2026-03 (has_child) ──────┐
│   └── 7个子节点              │ 并行遍历
├── 软考笔记 (has_child) ──────┼
│   └── 4个课程文件夹          │ 并行遍历
├── Obsidian 整理报告
└── 辞职决策记录

openclaw知识库 (root)
├── 11个文档节点（部分有子节点）  并行遍历
```

### 1d. 生成同步计划
将完整节点列表传给 `sync.py --plan`，获取待写入文件清单：

```bash
echo '[节点JSON]' | python3 sync.py --stdin --plan
```

**输出**：
- `need_fetch`：需要 Agent fetch 内容的 docx 文档
- `no_fetch_needed`：只写占位符的非 docx 类型

**Gate**：显示节点总数、来源 Wiki、待写入文件数，问用户确认是否继续。

---

## Step 2 — 确认同步路径

**触发**：Step 1 确认后

**执行**：
`sync.py --plan` 已输出每个文件的 `relative_path` 和 `filename`，显示路径映射表。

**Gate**：显示写入路径映射表，确认是否继续。

---

## Step 3 — 获取文档内容并写入 Obsidian

**触发**：Step 2 确认后

### 3a. Agent fetch 内容
对 `need_fetch` 中的每个文档，调用 `feishu_fetch_doc` 获取正文。

### 3b. 批量写入
将「文档信息 + fetch 到的内容」传给 `sync.py --write`：

```bash
echo '[{"title":"...","obj_token":"...","content":"...",...}]' \
  | python3 sync.py --stdin --write [--dry-run]
```

### frontmatter 生成规则
- 基础字段：`date`、`lastmod`、`draft`、`categories`、`tags`
- 飞书扩展字段：**无条件追加**：`feishu_doc_token`、`feishu_wiki`、`feishu_node_token`
- `feishu_doc_token` 用于去重，已存在则跳过

### 目录自动创建
`relative_path` 目录不存在时，自动创建。

**Gate**：显示将写入的文件列表，确认后执行。

---

## Step 4 — 质量检查

**触发**：Step 3 执行完成后

### 执行
1. 加载 `references/review-checklist.md`
2. 对照检查清单验证同步结果
3. 报告检查结果

**输出格式**：
```
【同步报告】
- 写入：X 个文档
- 跳过：X 个（已存在）
- 失败：X 个（错误信息）
```

---

## 初始化流程

**触发**：vault 缺少 SYNC-RULES.md

**执行**：
1. 向用户说明缺少文件
2. 生成默认版本（SYNC-RULES.md 模板）
3. 展示给用户确认
4. 用户确认后写入 vault 根目录
5. 继续 Step 1

**模板文件**：`assets/sync-rules-template.md`

---

## 参考文件

| 文件 | 作用 |
|------|------|
| `scripts/sync.py` | 纯路径构建 + 写入工具，双模式（--plan / --write）|
| `assets/sync-rules-template.md` | SYNC-RULES.md 生成模板 |
| `assets/agents-template-additions.md` | AGENTS.md 补充章节 |
| `references/review-checklist.md` | 同步质量检查清单 |

---

## 已知限制

- 电子表格（sheet）、多维表格（bitable）、思维导图（mindnote）只写链接占位符，不拉内容
- 并行遍历依赖 subagent 能力，每个 has_child 分支可同时请求
- Space ID 和目标路径从 SYNC-RULES.md 读取，修改配置后重新同步即可生效
