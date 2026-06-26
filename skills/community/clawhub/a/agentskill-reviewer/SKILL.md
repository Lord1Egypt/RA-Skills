---
name: agent-skill-reviewer
description: 评审 AgentSkills 质量并生成专业报告。用于检查 skill 的内容质量、结构完整性、文档清晰度、冗余问题。当用户要求"评审 skill"、"检查 skill 质量"、"审查 SKILL.md"、"分析这个 skill"时触发。
---

# Skill Reviewer - AgentSkill 质量评审系统

本 skill 用于系统化评审 AgentSkill 的质量，核心目标：**在保证功能完备的前提下，最大化精简 token 消耗**。

## 核心矛盾

- **过度精简**：说明不足，AI 无法正确执行任务
- **过度冗余**：描述繁琐，浪费 context window，逻辑缠绕

**目标：系统瘦身 + 逻辑完备** — 让 95% 的人（包括 AI）一眼看懂全流程。

## 评审流程

### 1. 初始扫描

读取目标 skill 的 `SKILL.md`：
- 理解该 skill 的核心功能
- 识别所有功能入口和工作流
- 记录 skill 的文件结构（scripts/、references/、assets/）

### 2. 逐项功能审核

对每个功能或子模块：

**可理解性审核**
- 是否可以被 95% 的人理解？
- 术语是否需要额外解释？
- 逻辑跳跃是否过大？

**Token 效率审核**
- 是否存在重复描述？
- 是否可以用脚本封装复杂逻辑？（模型只需调用一条命令）
- 是否可以扁平化层级结构？
- 是否可以用简洁示例替代冗长说明？

**冗余内容审核**
- 是否存在与功能无关的描述？
- 是否存在重复的文档片段？
- references/ 文件是否可以进一步精简或合并？

### 3. SKILL.md 审核

**Frontmatter 检查**
- `description` 是否清晰且包含触发场景？
- 是否包含所有"何时使用"信息？

**Body 检查**
- 是否存在应该移至 references/ 的详细内容？
- 工作流描述是否简洁有力？
- 是否存在应删除的冗余段落？

**Progressive Disclosure 检查**
- SKILL.md body 是否控制在 500 行以内？
- 是否正确使用 references/ 分离详细文档？
- 是否在 SKILL.md 中正确引用外部文件？

### 4. 逻辑对齐检查（关键）

对比`发现的问题`与`原始 skill 功能`：
- **禁止**为了瘦身而删减原本的任务逻辑
- **禁止**改变原有功能的语义
- **仅精简表达方式，不改变功能范围**

必要时运行 `scripts/validate_logic.py` 进行自动化逻辑对齐检查。详见 [references/validation.md](references/validation.md)。

### 5. 生成评审报告

使用 `scripts/generate_report.py` 生成结构化报告，详见 [references/report_template.md](references/report_template.md)。

**评分维度** (10 分制)：可理解性、Token 效率、功能完备性、结构合理性

**报告结构**：结论概览（打分）、优点、存在的问题（按严重程度分级）、优化计划（含 token 节省量和风险评估）

## 使用示例

```bash
# 评审某个 skill
评审 /path/to/my-skill

# 评审并指定输出路径
评审这个 skill 并输出报告到 ./reviews/my-skill-report.md
```

## 最佳实践

1. **先理解再评审** — 不熟悉功能时，先问用户澄清
2. **保守为主** — 不确定是否可删除时，保留并标注疑问
3. **量化改进** — 给出具体 token 节省数值
4. **提供示例** — 展示改进前后对比

## 输出格式

默认以中文输出，使用 Markdown 格式，清晰分级。报告默认保存到工作目录的 `skill-reviews/` 子目录下，文件名为 `<skill-name>-review-<date>.md`。
