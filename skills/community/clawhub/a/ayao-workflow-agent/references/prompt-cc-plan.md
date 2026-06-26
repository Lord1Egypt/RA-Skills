# CC Plan Prompt Template

Use this template when asking cc-plan to explore the codebase and produce a design document for a feature.

## cc-plan 的职责

cc-plan 负责两件事：

1. **探索代码库**：理解现有结构、约定、相关模块
2. **输出设计文档**：将探索结果写入 `docs/design/<feature>-design.md`

cc-plan **不负责** Requirements 收集，**不负责** 最终任务拆解（Plan）。任务拆解由编排层完成，cc-plan 可在设计文档末尾提供任务建议供参考。

## 调用命令格式

```bash
claude --permission-mode bypassPermissions --no-session-persistence --print 'PROMPT'
```

---

```
## Project
[Project name] — [one-line description]
Working directory: [path]

## Requirement
[Full description of what the user wants]

## Current State
[Relevant context: what exists, what's missing, recent changes]

## Your Tasks
1. Explore the codebase to understand the relevant structure, conventions, and existing modules
2. Write a design document to docs/design/<feature>-design.md

## Design Document Format
Write the design document to docs/design/<feature>-design.md. The document must include:

### Overview
- What this feature does and why
- Key constraints and assumptions

### Architecture
- How the feature fits into the existing codebase
- New files/modules to create and their responsibilities
- Existing files/modules to modify and how

### Data Flow
- How data moves through the system for this feature
- Key interfaces and contracts between components

### Technical Decisions
- Significant design choices and their rationale
- Alternatives considered and why they were rejected

### Implementation Notes
- Coding conventions to follow (based on codebase exploration)
- Potential pitfalls or tricky areas
- Testing approach

### Suggested Tasks (for orchestration layer reference only)
Provide a preliminary task breakdown as a JSON array. This is advisory only —
the final task list will be decided by the orchestration layer.

[
  {
    "id": "T001",
    "name": "Short task name",
    "domain": "backend" | "frontend",
    "scope": {
      "create": ["file paths"],
      "modify": ["file paths"],
      "delete": ["file paths"]
    },
    "description": "What this task does in 1-2 sentences",
    "technical_notes": "Key technical details the coding agent needs",
    "depends_on": ["T00X"],
    "estimated_minutes": 30
  }
]

## Rules
- The design document MUST be written to docs/design/<feature>-design.md (create dirs if needed)
- Base all design decisions on actual codebase exploration, not assumptions
- Each suggested task = one atomic commit
- Task scope must not overlap with other tasks' file paths
- Frontend tasks (pages, components, UI) marked domain: "frontend"
- Backend tasks (API, logic, DB, infra) marked domain: "backend"
- Shared type files: assign to the task that creates/changes the type, other tasks depend on it
- Order tasks by dependency chain

## Done When
- 已探索相关代码并基于实际代码库写出设计文档
- `docs/design/<feature>-design.md` 已包含要求的所有章节
- Suggested Tasks 足够具体，可供编排层继续拆分

## Contributor Mode（任务完成后填写）
任务完成后，必须把下面的 field report 填入 git commit message body（subject line 后空一行，再粘贴 body）。
请保留标题原样，按实际结果填写；如果某项没有内容，写"无"。

## Field Report (Contributor Mode)
### 做了什么
- [list of key changes made]
### 遇到的问题
- [any issues encountered, or "无"]
### 没做的事（或者留给下个人的）
- [things explicitly skipped, or "无"]

**请将上述内容完整写入 commit message body**（第一行是 conventional commit 标题，空一行，然后是 field report）。格式示例：

    ```
    feat(scope): one-line description

    Contributor Mode:
    - 做了什么：...
    - 遇到问题：...（如无请写"无"）
    - 有意跳过：...（如无请写"无"）
    ```
```
