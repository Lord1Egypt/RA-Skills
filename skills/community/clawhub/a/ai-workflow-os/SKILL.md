# AI Workflow Operating System / AI 工作流操作系统

Version / 版本: 1.0.0  
Slug / 包名: `ai-workflow-os`

## Purpose / 目标

AI Workflow Operating System is a bilingual master skill that combines project lifecycle planning, project memory, task handoff, web and file intake, source filtering, knowledge-base governance, cross-source synthesis, and audit tracking into one unified AI workflow.

AI 工作流操作系统是一个中英双语总控 Skill，用于把项目生命周期规划、项目记忆、任务交接、网页与文件资料接入、来源筛选、知识库入库治理、多来源综合分析和审计追踪整合到一个统一工作流中。

This skill is the unified upgrade of the previous Project Lifecycle Navigator, Daily Workflow, and Web Search Rules skills. The Web Search Rules workflow is upgraded into Knowledge Intake Governance, supporting web pages, files, documents, spreadsheets, slides, images, datasets, manual notes, and other research materials. Going forward, these workflows can be maintained together in this single bilingual package.

这是此前 Project Lifecycle Navigator、Daily Workflow 和 Web Search Rules 三个 Skill 的统一升级版；其中 Web Search Rules 已升级为支持网页、文件和多来源资料的 Knowledge Intake Governance。以后这些工作流会合并在这个双语包里统一维护。

---

## Core Modules / 核心模块

1. **Project Lifecycle / 项目生命周期规划**  
   Clarify goals, requirements, MVP scope, risks, milestones, and upgrade plans.  
   明确项目目标、需求、MVP 范围、风险、里程碑和升级计划。

2. **Project Memory / 项目记忆工作流**  
   Maintain project state, status, completed work, pending work, next actions, archives, and AI handoff notes.  
   维护项目状态、当前进度、已完成事项、待办事项、下一步计划、归档记录和 AI 交接信息。

3. **Knowledge Intake Governance / 知识库资料接入治理**  
   Govern web pages, uploaded files, documents, spreadsheets, slides, images, datasets, manual notes, and cloud documents through source classification, trust evaluation, staging, review, archiving, and audit logs.  
   通过来源分类、可信度判断、暂存审核、确认归档和审计日志，治理网页、上传文件、文档、表格、幻灯片、图片、数据集、人工笔记和云端文档。

4. **Cross-source Knowledge Synthesis / 多来源知识综合分析**  
   Compare, deduplicate, reconcile, summarize, and synthesize information across source types.  
   对不同来源资料进行对比、去重、矛盾处理、摘要和综合分析。

---

## Router / 任务路由

Before acting, classify the user's request into one or more modules.

在执行前，先判断用户请求属于哪个模块或模块组合。

### Use Project Lifecycle when / 以下情况使用项目生命周期规划

- The user wants to start a new project.
- The user asks for requirement clarification, MVP planning, roadmap planning, code-review upgrade planning, or project realignment.
- The user says the project is unclear, drifting, too large, or needs structure.

- 用户要启动新项目。
- 用户要求需求澄清、MVP 规划、路线图、代码审查升级规划或项目校准。
- 用户表示项目不清楚、跑偏、范围过大或需要结构化。

### Use Project Memory when / 以下情况使用项目记忆

- The user asks to save progress, continue a previous project, create a checkpoint, wrap up work, or hand off to another AI/person.
- The user asks what has been done, what remains, or what the next step is.

- 用户要求保存进度、继续之前项目、建立检查点、收工或交接给其他 AI/人员。
- 用户询问已完成什么、还剩什么、下一步是什么。

### Use Knowledge Intake Governance when / 以下情况使用知识库资料接入治理

- The user asks to search the web, review sources, collect documents, process files, ingest materials, build a knowledge base, filter sources, manage whitelist/blacklist rules, or stage content for approval.
- The user provides PDFs, Word files, spreadsheets, slides, images, email attachments, cloud documents, datasets, or manual notes and asks to add them to a knowledge base.

- 用户要求搜索网页、审查来源、收集资料、处理文件、资料入库、建立知识库、筛选来源、管理黑白名单或暂存审核。
- 用户提供 PDF、Word、表格、幻灯片、图片、邮件附件、云端文档、数据集或人工笔记，并要求加入知识库。

### Use Combined Flow when / 以下情况使用组合流程

If a request touches multiple modules, execute in this order unless the user specifies otherwise:

如果请求涉及多个模块，除非用户另有说明，按以下顺序执行：

1. Project Lifecycle: define purpose and scope.  
   项目生命周期：先定义目标和范围。
2. Knowledge Intake Governance: define source, intake, review, and archive rules.  
   知识库资料接入治理：定义来源、接入、审核和归档规则。
3. Project Memory: save the current state and next actions.  
   项目记忆：保存当前状态和下一步。
4. Cross-source Synthesis: summarize and reconcile findings.  
   多来源综合分析：总结和处理资料之间的差异。

---

## Default Workspace / 默认工作区

When the user does not specify a path, use:

如果用户没有指定路径，默认使用：

```text
Docs/
```

Recommended project files / 推荐项目文件：

```text
Docs/PROJECT.md
Docs/TARGET.md
Docs/STATUS.md
Docs/COMPLETED.md
Docs/PENDING.md
Docs/NEXT_ACTIONS.md
Docs/HANDOFF.md
Docs/CONFIG.md
Docs/archive/YYYY-MM.md
```

Recommended knowledge governance files / 推荐知识治理文件：

```text
Docs/knowledge/INTAKE_CONFIG.md
Docs/knowledge/SOURCE_RULES.md
Docs/knowledge/RESEARCH_QUEUE.md
Docs/knowledge/KNOWLEDGE_INDEX.md
Docs/knowledge/AUDIT_LOG.jsonl
Docs/knowledge/archive/YYYY-MM.md
```

---

## Knowledge Intake Source Types / 知识接入来源类型

Supported source types include:

支持的资料来源包括：

```text
web_page
pdf
docx
spreadsheet
slide_deck
image
email_attachment
cloud_doc
manual_note
local_file
dataset
api_result
```

Each intake item should be normalized into a knowledge record before archiving.

每条资料入库前都应转换为统一知识记录。

---

## Trust Levels / 来源可信度等级

Use four trust levels:

使用四级可信度：

```text
trusted  / 可信来源
allowed  / 可用来源
review   / 待审核来源
blocked  / 屏蔽来源
```

Default behavior:

默认行为：

- `trusted`: may be staged automatically; may be archived automatically only if policy permits.
- `allowed`: may be staged; usually requires review before archive.
- `review`: must enter review queue.
- `blocked`: do not archive; record only if audit requires it.

- `trusted / 可信来源`：可自动暂存；只有策略明确允许时才可自动归档。
- `allowed / 可用来源`：可暂存；通常需要审核后归档。
- `review / 待审核来源`：必须进入审核队列。
- `blocked / 屏蔽来源`：不入库；仅在审计需要时记录。

---

## Intake Status Machine / 接入状态流转

Use the following status values:

使用以下状态：

```text
searched
received
extracted
staged
needs-review
approved
archived
rejected
blocked
expired
superseded
```

Do not treat uploaded files as automatically trusted. User-provided materials can be important, but they may still contain outdated, duplicated, confidential, or unverified information.

不要把用户上传文件默认视为可信。用户提供的资料可能很重要，但仍可能包含过时、重复、机密或未经核实的信息。

---

## Safety and Confirmation Rules / 安全与确认规则

- Never upload local files or private documents to a cloud knowledge base without user confirmation.
- Never archive sensitive documents automatically unless the user has explicitly configured that policy.
- Separate temporary staging from permanent archive.
- Keep an audit trail for source decisions, rule changes, archive decisions, and cloud uploads.
- When a source is ambiguous, prefer staging and asking for confirmation.
- Preserve provenance: source URL, file name, file hash when available, upload time, extraction method, decision reason, and archive target.

- 未经用户确认，不得把本地文件或私有文档上传到云端知识库。
- 除非用户明确配置，否则不得自动归档敏感文件。
- 暂存与永久归档必须分开。
- 对来源判断、规则变更、归档决定和云端上传保留审计记录。
- 来源不明确时，优先暂存并请求确认。
- 保留来源信息：来源 URL、文件名、文件哈希、上传时间、提取方式、决策理由和归档目标。

---

## Output Style / 输出风格

- Use the user's language unless they request bilingual output.
- For operational outputs, prefer concise tables and checklists.
- For project handoff, always include current state, completed work, pending work, risks, and next actions.
- For knowledge intake, always include source type, trust level, status, summary, recommended decision, and audit note.

- 默认使用用户语言，除非用户要求双语。
- 操作型输出优先使用简洁表格和清单。
- 项目交接必须包括当前状态、已完成、待办、风险和下一步。
- 知识接入必须包括来源类型、可信度、状态、摘要、建议决策和审计备注。

---

## Key References / 关键参考文件

- `modules/project-lifecycle.md`
- `modules/project-memory.md`
- `modules/knowledge-intake-governance.md`
- `modules/cross-source-synthesis.md`
- `templates/knowledge-record-schema.md`
- `references/migration-guide.md`
- `references/source-trust-levels.md`
- `references/usage-examples.md`
