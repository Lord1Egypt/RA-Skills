---
name: arch-review
description: |
  Architecture review based on OpenSpec documents and code. Multi-dimension
  concurrent evaluation with structured scoring and actionable recommendations.
  Use when asked to "review architecture", "arch review", "架构评审",
  "evaluate the design", or "review openspec".
  Proactively suggest when a project has openspec/specs/ and the user is about
  to start implementation or refactoring.
---

# Architecture Review Skill

## Core Principles

1. THIS IS AN ARCHITECTURE REVIEW, NOT A CODE REVIEW.
   Evaluate at the MODULE/COMPONENT level — system structure, boundaries, data flow, design trade-offs.
   Ignore code style, variable naming, function-level implementation, individual bugs, formatting.
   - Good: "web 模块直接依赖 sync 引擎，违反分层架构"
   - Bad: "第 42 行的变量命名不规范"
   - Good: "缺少统一的错误传播策略"
   - Bad: "这个 try/except 应该 catch 更具体的异常"

2. THIS SKILL PRODUCES A REPORT. It does NOT fix, modify, or implement anything.
   Output: a structured architecture evaluation report.
   No file edits. No code changes. No PRs. Report only.

---

## Phase 0: Read Configuration

Before any analysis, read and understand the current dimensions and report template.
These files live alongside this SKILL.md — the user may have customized them.

1. Read `dimensions.md` (relative to this SKILL.md).
   - Parse each `## Dimension: <name>` section.
   - Build a list of active dimensions with their id, description, scoring criteria, and checklist.
   - Count N = number of dimensions found.

2. Read `report-template.md` (relative to this SKILL.md).
   - Understand the overall report structure and per-dimension output format.
   - This template governs how the final report is assembled.

3. Read `examples.md` (relative to this SKILL.md) for output style reference.

If any file is missing, warn the user and fall back to inline defaults.

---

## Phase 1: Discover OpenSpec Documents

Locate the project's OpenSpec specifications:

1. Search for `openspec/specs/` directory in the project root.
2. If not found, search for `specs/`, `spec/`, or any `*.spec.md` files.
3. If no spec is found, ask the user to provide the spec path or switch to `--spec-only` mode with a provided document.

For each spec file found:
- Parse `### Requirement: <name>` blocks and their `#### Scenario:` sub-blocks.
- Extract the requirement name, SHALL/MUST statements, and GIVEN/WHEN/THEN scenarios.
- Build a structured requirements list.

---

## Phase 2: Scan Project Architecture

### Step 2.0: Check for previous review reports

Look for `{project_root}/.arch-review/` directory.
If it exists, read the MOST RECENT report file (sorted by date in filename).

From the previous report, extract:
- Architecture Overview section (diagram, module registry, data flow) — use as baseline
- Previously identified issues (selected + deferred) — check for recurrence
- Any structural changes since last review

If a previous report exists, this review becomes an INCREMENTAL review:
- Reuse the architecture overview as starting point, update only what changed
- Flag recurring issues (appeared in last report and still present)
- Note resolved issues (in last report but no longer applicable)

If no previous report exists, proceed with a full scan.

### Step 2.1: Scan architecture (if no previous report, or to validate/update)

If code exists (skip if spec-only mode):

Focus on STRUCTURE, not implementation details:

1. Detect project language(s) and framework(s) from package files.
2. Map the top-level module/package layout and their responsibilities.
3. Identify architectural boundaries: what are the major components and how do they connect?
4. Note dependency direction (who depends on whom at the MODULE level).
5. Identify data storage, external integrations, and communication patterns.

DO NOT read individual function bodies. Only scan module-level structure, entry points, and interfaces.

---

## Phase 3: Build Shared Context

Construct the shared context payload that every subagent will receive:

```
SHARED_CONTEXT:
- Project summary: language, framework, domain
- OpenSpec requirements list (name + SHALL statement, no full scenarios unless small)
- Code structure summary from Phase 2
- Key file paths for deeper inspection
```

Keep this under 3000 tokens to leave room for dimension-specific instructions.

---

## Phase 4: Dimension Review

The main agent performs the review directly — one dimension at a time.
Do NOT delegate to subagents via Task tool. You (the main agent) do all the work.

### Execution Mode

**Default: Sequential (main agent)**
- Evaluate each dimension yourself, one by one.
- For each dimension, read relevant project files, apply the scoring criteria, produce the evaluation.
- This ensures the correct model is always used (whichever model the user chose for this conversation).

**Optional: Parallel (subagents)**
- Only use Task tool if the user explicitly says "并发" / "parallel" / "用子 agent".
- When using subagents, pass the `model` parameter with the full slug from ALIAS_MAP below.

ALIAS_MAP (for subagent mode only):
| Alias | Full Slug |
|-------|-----------|
| opus | claude-4.6-opus-medium-thinking |
| sonnet | claude-4.6-sonnet-medium-thinking |
| gemini | gemini-3.1-pro |
| codex | gpt-5.3-codex |
| fast | composer-2-fast |

### Per-Dimension Evaluation Process

For EACH dimension in the active list:

1. Read the dimension's scoring criteria and checklist from dimensions.md.
2. Read relevant project files for this dimension:
   - Modularity → module layout, import structure, package boundaries
   - Data Flow → state stores, data pipelines, async patterns
   - Scalability → resource usage, growth patterns, bottleneck points
   - Resilience → error handling patterns, external call wrappers
   - Security → auth, trust boundaries, secrets handling
   - Observability → logging, metrics, tracing infrastructure
   - DevEx → docs, API consistency, onboarding paths
   - Spec Consistency → compare spec requirements against implementation structure
3. Evaluate ARCHITECTURE (not code details):
   - Design decisions and their trade-offs
   - Structural patterns and architectural fitness
   - Alignment between spec intent and system structure
   - Systemic risks and architectural debt
4. Produce the evaluation in this format:

```
### {dimension_name} — {score}/10

#### Strengths
- {architectural strength}: {explanation referencing spec or module}

#### Weaknesses
- {architectural weakness}: {explanation referencing spec or module}

#### Recommendations
| # | Priority | Recommendation | Related Spec/Module |
|---|----------|---------------|---------------------|
| 1 | ... | ... | ... |
```

DO NOT focus on code style, naming, formatting, individual bugs, or line-level issues.
Focus on design decisions, component relationships, responsibility distribution, and evolvability.

### Understanding User Intent

The user may express preferences in natural language. Parse their intent:

**Scope (which dimensions to review)**:
- "只看安全和可扩展性" / "focus on security" → only evaluate matching dimensions
- "全量评审" / "review everything" / no mention → all dimensions
- "跳过开发者体验" / "skip devex" → all dimensions except the excluded ones

**Mode (with or without code)**:
- "只看 spec" / "spec only" / "还没写代码" → skip code scanning, evaluate spec alone
- Default: review both spec and code

**Execution (sequential or parallel)**:
- Default: main agent evaluates all dimensions sequentially (model = current conversation model)
- "并发" / "parallel" / "用子 agent" → use Task tool to launch parallel subagents

---

## Phase 5: Present Full Analysis Report

Once all dimensions are evaluated:

1. Assemble and present the COMPLETE analysis report to the user:
   - Header with project info and review metadata
   - Summary scoreboard (all dimensions at a glance)
   - Detailed per-dimension sections (score, strengths, weaknesses, recommendations)
   - Top critical architectural risks

Show the user the FULL report so they understand the complete picture before making decisions.

---

## Phase 6: Issue Triage (multi-step interactive)

After the user has reviewed the full analysis report, walk through issues
dimension by dimension. Each dimension is ONE interaction step.

### Process: one AskQuestion per dimension (only for dimensions with issues)

For each dimension that has weaknesses/recommendations:

1. Present the dimension's issues with your recommended priority as a guide.
2. Let the user multi-select which issues to include in the final report.
3. After each selection, ask the user if they have comments/notes on the selected issues.

### Step format for each dimension:

```
AskQuestion:
  title: "{dimension_name} ({score}/10) — 问题确认"
  prompt: "以下是该维度的架构问题（已按推荐优先级排序）。请勾选要纳入正式报告的："
  options:
    - "[推荐: HIGH] {issue summary} — {location}"
    - "[推荐: MEDIUM] {issue summary} — {location}"
    - "[推荐: LOW] {issue summary} — {location}"
  allow_multiple: true
```

After the user selects, ask in plain text (not AskQuestion):
"对以上勾选的问题，是否有批注或补充意见？（直接输入，或回复"无"跳过）"

Record any user comments — they will be included in the final report alongside the issue.

### Priority recommendation rules:

- HIGH: Impacts multiple modules, blocks evolution, or violates core spec intent
- MEDIUM: Localized but creates tech debt or limits a specific capability
- LOW: Minor structural inelegance, acceptable in current scope

### After all dimensions are triaged:

Present a final summary of selections:
```
"已确认 X 个问题纳入正式报告，Y 个问题留档。是否确认生成最终报告？"
```

Wait for user confirmation before proceeding to Phase 7.

---

## Phase 7: Produce Final Report

Based on user selection, produce the final report with this structure:

### Section 1: Architecture Overview (ALWAYS include at top)

This section enables downstream agents to quickly understand the system without re-scanning.

Include:
- **Architecture Diagram** (mermaid): component/module relationships, data flow direction,
  external dependencies. Use a high-level diagram (not class-level).
- **Architecture Summary**: 3-5 sentences describing the system's structural approach.
- **Tech Stack**: language, framework, storage, external services.
- **Module Registry**: table of top-level modules with their responsibility and key entry points.
- **Data Flow**: how data enters, transforms, and exits the system.
- **External Boundaries**: what external systems are integrated and how.

```markdown
## Architecture Overview

### System Diagram

\`\`\`mermaid
flowchart TD
    ...
\`\`\`

### Summary
{3-5 sentence architecture description}

### Tech Stack
| Layer | Technology |
|-------|-----------|
| Language | ... |
| Framework | ... |
| Storage | ... |
| External | ... |

### Module Registry
| Module | Responsibility | Entry Point |
|--------|---------------|-------------|
| {module_path} | {what it does} | {main file/class} |
| ... | ... | ... |

### Data Flow
{source} → {processing} → {storage} → {presentation}

### External Boundaries
| System | Protocol | Module |
|--------|----------|--------|
| {e.g. GitHub API} | {REST/gRPC/etc} | {which module handles it} |
```

This section serves as an INDEX for future agent invocations — it should contain
enough structural info that a new agent can orient itself in < 30 seconds.

### Section 2: Selected Issues

1. **Selected issues** → Include in the final report with full detail:
   - Architectural problem description
   - Impact analysis
   - Related OpenSpec requirements
   - Key file/module locations (for downstream fix agent to locate the problem)
   - Suggested architectural direction (not code-level fix, but structural approach)

2. **Unselected issues** → Save to an appendix section "Deferred Issues":
   - One-line summary per issue
   - Score and dimension
   - Key location reference
   - These are recorded for future review cycles, not lost

3. Write the final report to a file in the project:
   - Path: `{project_root}/.arch-review/{date}-report.md`
   - Create the directory if it doesn't exist

The final report MUST include a machine-readable metadata section at the end for
downstream agents to consume:

```markdown
<!-- ARCH-REVIEW-META
project: {project_path}
date: {iso_date}
dimensions_reviewed: [list of dimension ids]
selected_issues:
  - id: {issue_id}
    dimension: {dimension}
    severity: {high|medium|low}
    location: {module or file path where the problem is rooted}
    spec_refs: [related requirement names]
    summary: {one-line}
deferred_issues:
  - id: {issue_id}
    dimension: {dimension}
    severity: {high|medium|low}
    location: {module or file path}
    summary: {one-line}
-->
```

THIS SKILL PRODUCES A REPORT. It does NOT fix, modify, or implement anything beyond
writing the report file itself. No code changes. No PRs. Report only.

The report is designed to be consumed by a separate fix agent that will:
- Read the metadata section to find issue locations
- Use the architectural direction to guide its fixes
- Ignore deferred issues unless explicitly told otherwise

---

## Slash Command and Usage Examples

Trigger: `/arch-review` — then the user may add natural language instructions:

| User says | Effect |
|-----------|--------|
| `/arch-review` | Full review, all dimensions, sequential |
| `/arch-review 只看安全和可观测性` | Only review security + observability |
| `/arch-review 还没写代码，先评审 spec` | Spec-only mode, no code scanning |
| `/arch-review 并发` | Use parallel subagents |
| `帮我做个架构评审` | Same as `/arch-review` (natural trigger) |

Note: The review uses whatever model the user chose for the current conversation.
To use a specific model, start the conversation with that model, then trigger the review.
