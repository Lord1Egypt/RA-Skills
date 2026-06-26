---
name: chudaxia-ai-coach-tools-position-agent-skills-generator
description: 将岗位智能体提示词中的岗位核心能力转化为一组符合 Agent Skills 规范的岗位技能包。Use when users need to analyze generated position-agent prompts, extract job skills, retrieve and internalize skill knowledge into assets, create one SKILL.md directory per skill, and sync the prompt skill list with generated skills.
metadata:
  agent-created: "true"
  related-skills: chudaxia-ai-coach-tools-position-agent-prompts-generator
---

# 岗位智能体技能生成器

## 概述

本技能接在 `chudaxia-ai-coach-tools-position-agent-prompts-generator` 之后使用，将其输出的「岗位智能体提示词」中的岗位技能逐项拆解为可挂载、可检索、可维护的 Agent Skill 技能目录。

核心交付包括：每个岗位技能对应的内化技能知识文档、符合 `assets/specs/agents-skills-specification.md` 的技能目录与 `SKILL.md` 文件，以及已回写技能映射关系的岗位智能体提示词。

## 强制输出要求

- **一项岗位核心能力对应一个技能目录**：除非用户明确批准合并或拆分，否则不得把多个能力合并为一个技能，也不得把一个能力拆成多个技能。
- **每个技能必须内化运行知识**：从腾讯 IMA 或本地文件目录检索、筛选并萃取后，必须写入 `assets/knowledge/knowledge.md`，使生成技能脱离原始知识源后仍可完整执行；不得要求运行时再访问原知识库、原始文件或上游提示词。
- **缺乏知识必须清晰标注**：证据不足时创建 `assets/knowledge/knowledge-gaps.md`，并在 `assets/knowledge/knowledge.md` 对应章节标注 `[待补齐]`，不得用推测内容补全。
- **每个技能必须有来源索引**：创建 `references/source-map.md`，记录检索词、来源文档、取舍理由和未采用材料；来源索引用于追溯审计，不作为技能执行依赖。
- **每个技能目录必须符合 Agent Skills 规范**：目录名与 `SKILL.md` frontmatter 的 `name` 完全一致，名称只使用小写字母、数字和连字符。
- **输出位置必须可挂载**：技能目录应输出到用户指定的 Skills 根目录，或在交付中明确标注安装/挂载状态与后续移动路径。
- **必须回写岗位智能体提示词**：更新原提示词中的技能层与知识层，使其技能清单、技能目录、知识文档一一对应。
- **最终交付必须包含映射表**：列出原岗位技能、生成技能名、技能目录、知识来源、回写位置和状态。

## 输入确认

开始前确认以下信息：

1. **岗位智能体提示词来源**：用户粘贴的 Markdown、已生成的 `.md` 文件，或上游生成器刚输出的内容。
2. **知识库来源**：腾讯 IMA 知识库或本地文件目录；该来源只用于生成阶段检索和内化，未指定时默认先问用户，不能假设已有 IMA 访问能力。
3. **输出根目录**：优先使用用户指定的可挂载 Skills 根目录；未指定时使用 `generated-position-agent-skills/<岗位slug>/`，并在最终交付中标明这些技能仍需移动或挂载后才能被运行时发现。
4. **是否允许调整技能数量**：默认不允许；如发现能力重叠、缺失或粒度异常，先给出建议并获得用户确认。

## 核心流程

### 步骤 1：解析岗位智能体提示词

读取完整岗位智能体提示词，至少提取以下内容：

- 岗位名称、部门、核心职责与工作边界
- `3. 技能层（Capability）` 中的岗位核心能力与降级策略
- `4. 知识层（Knowledge）` 中的参考规范底座与引用规范
- `5. 流程层（Workflow）` 中与技能相关的标准步骤与异常处理
- `6. 权限层（Compliance）` 中与技能相关的白名单、黑名单和上报机制
- `7. 绩效层（KPI）` 中与技能相关的质量标准

使用 `references/skill-extraction-framework.md` 建立「岗位技能登记表」。登记表必须包含：

| 字段 | 说明 |
|------|------|
| 原始能力名称 | 技能层中的原文名称 |
| 技能目录名 | 规范化 slug，必须能作为 skill `name` |
| 能力边界 | 该技能负责什么、不负责什么 |
| 知识检索词 | 用于 IMA 或本地目录检索的关键词组合 |
| 关联流程 | 该技能在岗位工作流中的调用时机 |
| 合规约束 | 该技能必须遵守的权限边界 |
| KPI 约束 | 该技能应满足的质量标准 |

### 步骤 2：检索并内化技能知识

针对登记表中的每个技能分别检索知识来源，并把可执行知识内化进技能目录：

**腾讯 IMA 来源**

1. 使用用户可用的 IMA/知识库检索能力，以「岗位名称 + 能力名称 + 关键业务对象 + SOP/规范/模板/案例」组合检索。
2. 优先选择与该技能直接相关的制度、流程、模板、案例和 FAQ。
3. 记录来源文档标题、知识库名称、检索关键词和可追溯标识。

**本地文件目录来源**

1. 使用文件搜索定位与技能关键词相关的 `.md`、`.docx` 转写、`.txt`、模板或规范文件。
2. 读取候选内容，按相关性筛选直接证据，不把泛泛背景材料当作技能知识。
3. 记录相对路径和关键摘录位置。

将每个技能的检索结果萃取并内化为 `assets/knowledge/knowledge.md`。该文件必须包含足以支撑技能独立运行的流程、规则、判断标准、模板、案例和降级说明，不得只写来源链接、检索提示或“请参考原文”。结构固定为：

```markdown
# [技能名称] 技能知识文档

## 适用范围

## 核心概念

## 标准流程

## 输入与输出

## 判断标准

## 异常与降级

## 合规边界

## 可复用模板或话术

## 内化知识来源摘要
```

同时创建 `references/source-map.md`，记录：检索来源、检索关键词、采用文档、未采用文档、采用/排除理由、可追溯标识。`references/source-map.md` 仅用于审计、复核和后续更新，不得作为技能运行时的必要知识入口。

证据不足时，不得补写成看似完整的规范；应在 `assets/knowledge/knowledge-gaps.md` 中列出缺口、已检索关键词和建议补充资料，并在 `assets/knowledge/knowledge.md` 对应章节标注 `[待补齐]`。

### 步骤 3：逐一生成技能目录

按 `assets/specs/agents-skills-specification.md` 为每个岗位技能创建目录：

```text
<output-root>/
  <skill-slug>/
    SKILL.md
    assets/
      knowledge/
        knowledge.md
        knowledge-gaps.md      # 仅在证据不足时创建
      templates/               # 仅在技能有表单、话术、画布模板时创建
    references/
      source-map.md
```

`SKILL.md` 必须满足：

- YAML frontmatter 包含 `name` 和 `description`
- `name` 与目录名完全一致，且不超过 64 个字符
- `description` 说明该技能做什么以及何时使用，包含岗位、能力和触发关键词
- 正文引用 `assets/knowledge/knowledge.md`，并在存在缺口时引用 `assets/knowledge/knowledge-gaps.md`
- 正文说明技能执行依赖已内化知识，不依赖运行时访问原始知识源
- 明确输入、处理流程、输出、降级策略、合规边界和自检标准

使用 `assets/templates/position-skill-template.md` 作为单个技能的起稿模板。

### 步骤 4：回写岗位智能体提示词

生成全部技能目录后，必须更新原岗位智能体提示词：

1. 在 `3. 技能层（Capability）` 中，将每项岗位核心能力补充为「能力名称 + 生成技能目录 + 内化技能知识文档 + 调用时机」。
2. 在 `4. 知识层（Knowledge）` 中补充生成的 `assets/knowledge/knowledge.md` 清单，并标注已挂载或待挂载状态。
3. 在文档末尾增加或更新「岗位技能包映射表」，列出所有一一对应关系。
4. 在映射表附近增加「技能包同步记录」，包含生成时间、生成器名称、知识来源类型和本次更新摘要。
5. 保持原七层结构完整，不改变身份、人设、流程、权限、绩效层的原意。

如果原提示词已经存在技能映射表或人工补充内容，先保留原内容并追加更新；发现同一岗位技能已有不同技能目录时，列出冲突并要求用户确认，不得静默覆盖。

如果输入不是可编辑文件，而是用户粘贴内容或上游技能刚输出的内容，必须输出一份完整的「已回写岗位智能体提示词」Markdown；如用户希望落盘，先确认目标文件路径再创建。

映射表格式：

| 原岗位技能 | 生成技能目录 | 技能知识文档 | 来源索引 | 知识来源 | 回写状态 |
|------------|--------------|--------------|----------|----------|----------|
| ... | ... | ... | ... | ... |

当存在 `assets/knowledge/knowledge-gaps.md` 时，回写状态必须标为「知识待补齐」，并在知识层对应文档后标注 `[待补齐]`。

### 步骤 5：质量自检

按 `references/skill-package-checklist.md` 完成自检。必须通过：

- 技能数量与原提示词技能层核心能力数量一致
- 每个技能目录都有有效 `SKILL.md`
- 每个 `SKILL.md` 的 `name` 与目录名一致
- 每个技能都有 `references/source-map.md`
- 每个技能至少有 `assets/knowledge/knowledge.md`，且该文件足以支撑技能脱离原始知识源运行
- 证据不足时另有明确的 `assets/knowledge/knowledge-gaps.md`，并在内化知识文档中标注 `[待补齐]`
- 原提示词已回写技能目录、知识文档和映射表
- 回写后的提示词仍保留七层结构；如同时存在结构化 JSON 表示，需再按 `chudaxia-ai-coach/assets/schemas/prompt-framework-schema.json` 校验
- 无虚构知识来源、无不可追溯结论

任一检查失败，先修正再交付。

## 命名规范

- 技能目录名优先使用英文语义 slug，例如 `quality-inspection-standard-design`。
- 只允许小写字母、数字和连字符；不得使用中文、空格、下划线或连续连字符。
- 目录名超过 64 字符时，压缩为「岗位域 + 核心动作 + 对象」，例如 `finance-budget-variance-analysis`。
- 同名冲突时添加短后缀，如 `-workflow`、`-review`，不要添加无意义序号，除非用户要求保留原顺序编号。

## 边界与异常处理

- **无法访问 IMA**：切换到用户提供的本地目录或要求用户提供导出的知识库材料。
- **本地目录无资料**：生成技能骨架和 `assets/knowledge/knowledge-gaps.md`，并在最终映射表标为「知识待补齐」。
- **岗位技能粒度混乱**：先输出拆分/合并建议，获得用户确认后再改变数量。
- **提示词不是七层结构**：先列出缺失层与可识别字段，获得用户确认后再按七层模板补齐；无法确认的内容标为 `[待补齐]`，不得擅自补成确定事实。
- **存在企业敏感信息**：技能知识文档保留必要业务规则，但对公司名、人名、内部系统名做泛化处理，除非用户明确要求保留。

## 最终交付格式

交付时使用 Markdown，包含：

1. 生成的技能目录清单
2. 岗位技能包映射表
3. 已更新的岗位智能体提示词路径或内容
4. 知识缺口与待补资料清单
5. 质量自检结果

## 参考资源

- `references/skill-extraction-framework.md`：岗位技能拆解与跨层映射方法。
- `references/skill-package-checklist.md`：技能目录、知识文档和提示词回写检查清单。
- `assets/templates/position-skill-template.md`：单个岗位技能 `SKILL.md` 模板。
- `assets/specs/agents-skills-specification.md`：Agent Skills 目录与 frontmatter 规范。