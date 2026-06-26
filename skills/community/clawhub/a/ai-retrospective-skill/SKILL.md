---
name: ai-retrospective
version: 1.0.0
description: >
  AI Collaboration Retrospective — a tool-agnostic post-session analysis framework.
  After each AI-assisted coding/development session, it systematically reviews the entire
  conversation across eight dimensions to identify improvement opportunities and generate
  a structured retrospective report. Core goal: make every AI session better than the last.
triggers:
  - "复盘"
  - "回顾一下"
  - "retrospective"
  - "retro"
  - "review this session"
license: MIT-0
compatibility:
  - Any AI coding assistant with conversation context access and file I/O
  - Tested with: WorkBuddy, Cursor, Claude Code, GitHub Copilot Chat, Windsurf, Cline
---

# AI Collaboration Retrospective

Post-session systematic review tool. Eight-dimension deep analysis drives a continuous improvement loop for AI-assisted development.

## Core Principles

- **Conversation context is the data source**: The complete conversation history of the current session is already in context — no external data fetching needed
- **Progressive loading**: Detailed evaluation criteria live in `references/analysis_dimensions.md` — load on demand
- **Self-reflection first**: Examine the AI's own shortcomings before analyzing user-side improvements. This is NOT about criticizing the user — it's about finding efficiency gains in the "AI + Human" collaboration
- **Quantify everything**: Every finding must reference specific conversation turns, wasted operations, and include counterfactual reasoning ("If X had been done, Y turns could have been saved")
- **Dig deep**: Don't settle for "no findings." Complete the self-check list for each dimension before declaring it clean

## Execution Model

This skill is **pure LLM instruction-driven** — no scripts, no external dependencies. It works on any AI assistant that can:
1. Access the current conversation history
2. Read reference files from this skill's directory
3. Write output files to the workspace

**Capability adaptation**: The workflow below references file operations and memory updates. If your AI tool doesn't support a specific capability, skip that step and note it in the report. The analysis itself only requires conversation context access.

## Workflow (Six Steps)

### Step 1: Conversation Review — Extract Key Events + Tag Waste Points

Scan the entire conversation context and extract these key events into a timeline:

| Event Type | Recognition Signal |
|-----------|-------------------|
| Tool invocations | Command execution, file reading/writing, web searches, code generation |
| File changes | Files created, modified, or deleted |
| Errors & fixes | Error messages, lint failures, debugging cycles |
| Repeated modifications | Same file/feature modified multiple times, user providing multiple clarifications |
| Decision points | Technology choices, architecture decisions, trade-offs |
| Automation/plugin usage | Any skill, agent, plugin, or extension triggered during the session |
| User clarifications | User adding context because the AI misunderstood intent |
| **Verification rounds** | User providing test data/feedback, AI analyzing verification results |
| **AI misjudgments** | AI providing wrong conclusions, missing critical issues, or jumping to premature conclusions |

**Filter rule**: System initialization events (bootstrap files, identity setup, etc.) are excluded from analysis.

**Critical step — Waste point tagging**:

After building the timeline, interrogate each event in reverse:
1. **Could this step have been avoided?** If something had been done earlier, would this step be unnecessary?
2. **Could this step have happened sooner?** Did the AI delay something it should have proactively done?
3. **Did this step duplicate prior work?** Was the AI hand-writing logic that could have been reused?

Tag events where the answer is "yes" with `[⚠ Optimizable]` and record the reason. These tags are the core input for Step 2.

Output format: Chronological event list with type labels and brief descriptions. Waste points tagged separately.

### Step 2: Eight-Dimension Deep Analysis

Load `references/analysis_dimensions.md` for detailed evaluation criteria, self-check lists, and common patterns per dimension. Analyze conversation events dimension by dimension to identify improvement opportunities.

**Eight dimensions overview:**

1. **AI Self-Reflection** ⭐ — AI's mistakes, delayed reactions, missed judgments in this session (highest priority, must be analyzed first)
2. **Verification Strategy** — Did the AI proactively define verification criteria and expected outcomes, or passively wait for user feedback?
3. **Automation Opportunities** — Repetitive workflows or hand-written scripts that could be encapsulated into reusable automations
4. **Existing Automation Tuning** — Were any existing automations/skills/templates used? Did they have gaps, unclear instructions, or output issues?
5. **Tool Integration Opportunities** — Operations that would benefit from dedicated tool integrations, plugins, or API connections
6. **Knowledge Persistence** — Preferences, conventions, and technical decisions from this session that should be persisted for future sessions
7. **Documentation Updates** — Project docs, coding standards, or architecture notes that need updating
8. **Workflow Efficiency** — Sequential steps that could be parallel, repeated labor, suboptimal tool choices

**Analysis requirements (mandatory):**

For each dimension:
- Run through the dimension's self-check list (defined in `references/analysis_dimensions.md`)
- For findings, output: **Specific event reference** (which turn, what operation) + **Counterfactual reasoning** (if X had been done, Y could be saved) + **Recommendation** + **Priority**
- Only after all self-check items pass can a dimension be declared "no findings" and skipped

### Step 3: Generate Retrospective Report

Load `assets/report_template.md` for the report template. Fill the template with results from Step 1 and Step 2 to produce a complete Markdown retrospective report.

**Report save path**: `{workspace}/retrospectives/{topic}_retrospective.md`

Naming rules:
- `{topic}` uses 2-4 English words joined by hyphens, summarizing the session's core task (e.g., `multithread-scope-collection`, `login-flow-refactor`)
- **Multiple retrospectives on same topic**: If the file already exists, append the new report at the end (separated by `---` and a new date heading) — don't create a new file

If the `retrospectives/` directory doesn't exist, create it first.

> **Note**: The save path above is a sensible default. Adapt to your project's conventions if they differ.

### Step 4: Display Full Analysis in Conversation

**The complete analysis must be shown directly in the conversation** — don't just output a summary and point to the file. The file is an archive; the primary reading experience is in the conversation.

Output content (show in full, no trimming):

1. **Session summary**: One-sentence overview
2. **Efficiency score**: Optimizable turns / total turns
3. **Event timeline**: Complete table with waste point tags
4. **All dimension findings**: Each with event reference, problem, counterfactual reasoning, recommendation (this is the core content — **never abbreviate or reduce**)
5. **Pending action list** (if any)
6. **Report archive location**

Format: Use Markdown tables and headings for clear structure. Better to be thorough than to cut valuable analysis.

### Step 5: Automatic Execution — Knowledge Persistence

For items identified in the "Knowledge Persistence" dimension (Dimension 6), execute persistence operations available in your AI tool:

- If your tool supports persistent memory (e.g., memory APIs, memory files, `.memory` directories), write new preferences/conventions directly
- If your tool supports project-level notes or config, update those
- If your tool has no persistence mechanism, list the items that *should* be persisted and recommend the user save them manually

Briefly state what was updated after each operation. Skip this step if no knowledge needs persisting.

### Step 6: Pending Action List

For the following types of improvement suggestions, **do not auto-execute** — list them for user selection:

| Action Type | Examples |
|------------|---------|
| Create new automation | Reusable workflow, script template, custom command |
| Tune existing automation | Modify instructions, parameters, or trigger conditions |
| Create/update project rules | Coding standards, review checklists, conventions |
| Update project documentation | Architecture docs, API references, onboarding guides |
| Create tool integration | Custom plugin, API connection, webhook |

List format: Numbered list, each item includes "Action type + Specific content + Expected benefit." User can reply with numbers to select which actions to execute.

If no pending actions, skip this step and state "No additional actions needed for this session."

## Edge Cases

**Very short sessions**: If the conversation is only a few turns with simple content, output a brief summary and state "This session was brief — no significant improvement opportunities identified." Don't force analysis.

**Compressed/summarized history**: If the conversation history appears compressed or truncated, analyze based on available context and note in the report: "Some conversation history was compressed; analysis is based on visible context."

**Tool capability limitations**: If the AI tool being used lacks certain capabilities referenced in this workflow (e.g., no file writing, no memory persistence), adapt gracefully — perform the analysis steps that are possible and clearly note any skipped steps with the reason.
