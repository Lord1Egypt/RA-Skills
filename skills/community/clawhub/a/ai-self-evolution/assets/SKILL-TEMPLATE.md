# Skill 模板

用于从 learnings 中抽取 skill 的模板，可复制后按需定制。

---

## SKILL.md 标准模板

```markdown
---
name: skill-name-here
description: "简要说明此 skill 何时使用、用于解决什么问题，并包含触发条件。"
---

# Skill 名称

简要介绍该 skill 解决的问题及其来源背景。

## 快速参考

| 场景 | 操作 |
|-----------|--------|
| [触发条件 1] | [执行动作 1] |
| [触发条件 2] | [执行动作 2] |

## 背景

说明这条知识为何重要、能避免哪些问题、以及原始 learning 的上下文。

## 解决方案

### 分步执行

1. 第一步（可附代码或命令）
2. 第二步
3. 验证步骤

### 代码示例

\`\`\`language
// 演示解决方案的示例代码
\`\`\`

## 常见变体

- **变体 A**：说明及处理方式
- **变体 B**：说明及处理方式

## 注意事项

- 常见问题或风险点 #1
- 常见问题或风险点 #2

## 相关内容

- 相关文档链接
- 相关 skill 链接

## 来源

从 learning 条目抽取。
- **Learning ID**: LRN-YYYYMMDD-XXX
- **原始分类**: correction | insight | knowledge_gap | best_practice
- **抽取日期**: YYYY-MM-DD
```

---

## 精简模板

适用于结构简单、无需完整章节的 skill：

```markdown
---
name: skill-name-here
description: "说明此 skill 的用途与触发时机。"
---

# Skill 名称

[一句话问题描述]

## Solution

[直接给出解决方案与代码/命令]

## Source

- Learning ID: LRN-YYYYMMDD-XXX
```

---

## 含脚本模板

适用于包含可执行辅助脚本的 skill：

```markdown
---
name: skill-name-here
description: "说明此 skill 的用途与触发时机。"
---

# Skill 名称

[简介]

## 快速参考

| 命令 | 作用 |
|---------|---------|
| `./scripts/helper.sh` | [功能说明] |
| `./scripts/validate.sh` | [功能说明] |

## 使用方式

### 自动化（推荐）

\`\`\`bash
./skills/skill-name/scripts/helper.sh [args]
\`\`\`

### 手动步骤

1. 步骤一
2. 步骤二

## 脚本说明

| 脚本 | 描述 |
|--------|-------------|
| `scripts/helper.sh` | 主工具脚本 |
| `scripts/validate.sh` | 校验脚本 |

## 来源

- Learning ID: LRN-YYYYMMDD-XXX
```

---

## 命名规范

- **Skill 名称**：全小写，单词间使用连字符
  - Good: `docker-m1-fixes`, `api-timeout-patterns`
  - Bad: `Docker_M1_Fixes`, `APITimeoutPatterns`

- **Description**：以动作动词开头，并明确触发条件
  - Good: "Handles Docker build failures on Apple Silicon. Use when builds fail with platform mismatch."
  - Bad: "Docker stuff"

- **文件结构**：
  - `SKILL.md` - 必填，主文档
  - `scripts/` - 可选，可执行代码
  - `references/` - 可选，详细文档
  - `assets/` - 可选，模板资源

---

## 抽取检查清单

从 learning 创建 skill 之前：

- [ ] Learning 已验证（status: resolved）
- [ ] 方案具备通用性（非一次性问题）
- [ ] 内容完整（包含必要上下文）
- [ ] 名称符合规范
- [ ] 描述简洁且信息充分
- [ ] 快速参考表可执行
- [ ] 代码示例已验证
- [ ] 已记录来源 Learning ID

创建之后：

- [ ] 回写原 learning 状态为 `promoted_to_skill`
- [ ] 在 learning Metadata 中添加 `Skill-Path: skills/skill-name`
- [ ] 在新会话中读取并验证该 skill 可独立使用
