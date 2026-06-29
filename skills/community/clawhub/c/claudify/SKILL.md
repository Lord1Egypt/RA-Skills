---
name: claudify
description: |
  Agentic AI lifecycle: create + improve + persist. create - convert functionality into Claude Code automation (agent/skill/rule/hook/command) [SKILL.md], improve - self-improving loop: retrospect + hook/skill review + pattern detect [improve.md], persist - knowledge persistence: documentation + memory save [persist.md]. Use when "agentify", "agentic", "automate this", "create an agent", "make a plugin", "make a skill", "self-improve", "claudify improve", "claudify persist".
metadata:
  author: es6kr
  version: "0.1.2"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Skill
  - Bash(mkdir:*)
---

# Claudify

Guide users to convert functionality into the appropriate Claude Code automation type (Agent, Skill, Rule, Command, or Hook).

## Decision Matrix

| Type | When to use | Implementation |
| ---- | ----------- | -------------- |
| **Agent** | High autonomy, multi-tool | `.claude/agents/name.md` |
| **Skill** | Domain expertise, logic | `.claude/skills/name/SKILL.md` |
| **Rule** | Constraints, styling | `.claude/rules/name.md` |
| **Slash Command** | User types `/cmd` | Simple prompt templates |
| **Hook** | Events (tool use, etc) | Automation on actions |

Full comparison: [automation-decision-guide.md](./resources/automation-decision-guide.md)

## Workflow

### Step 0: Output-size routing (HARD STOP — before Step 1)

**Before any large-output operation, decide: inline vs subagent vs script.** Parent context bloat from claudify itself reduces the budget available for the actual automation creation work.

#### Routing decision matrix

| Operation | Inline OK? | Dispatch to subagent? | Script? |
|-----------|-----------|----------------------|---------|
| Read 1 resource file (template/guide) | ✅ Inline | — | — |
| Read 2+ large resource files (>200 lines each) | ❌ | ✅ general-purpose subagent | — |
| Scan transcript for automation patterns (no target) | ❌ | ✅ Explore or general-purpose | — |
| Enumerate `~/.claude/plugins/marketplaces/*/plugins/*/` | ❌ | — | ✅ `find` / `ls` 1-liner |
| Create single agent/rule/command file (inputs known) | ✅ Inline | — | — |
| Create multi-topic skill (writer + multiple topic files) | ❌ | ✅ skill-writer subagent | — |
| Marketplace remote search (WebFetch + parsing) | ❌ | ✅ general-purpose subagent | — |

#### Don't / Do table

| # | Don't | Do |
|---|-------|-----|
| 1 | Read `resources/agent-templates.md` (358 lines) + `automation-decision-guide.md` + `askuserquestion-patterns.md` inline before creating one agent | Dispatch general-purpose subagent: "Read these 3 templates and create agent at `<path>` with name=X, tools=Y, description=Z. Return the created file path only." |
| 2 | Inline scan transcript for candidates by Read-ing the full session JSONL | Dispatch Explore subagent: "Find verbose tool-output patterns (>500 tokens repeated 2+ times) in conversation. Return candidate list (label + 1-line description) under 200 words." |
| 3 | Inline Glob + Read all marketplace plugin SKILL.md files | Bash 1-liner: `find ~/.claude/plugins/marketplaces/*/plugins/*/ -name SKILL.md -exec head -3 {} \;` returns names without body |
| 4 | "Just one more Read" cumulative inline reading | Quantify: if next operation expected to add >2K tokens to parent context AND result is not the deliverable itself, dispatch subagent |
| 5 | Dispatch subagent with vague prompt ("create the agent") | Subagent prompt must include: target file path, name, tools, model, description (single-line YAML), trigger keywords. Return only the file path |

#### Self-check (before each Read/Glob/WebFetch in claudify workflow)

1. Is the read result the deliverable, or intermediate context that the subagent's parent doesn't need?
2. Will this Read + subsequent Reads cumulatively add >2K tokens to parent context?
3. Is the operation parallelizable (multiple Reads, multiple files)?
4. If 1=intermediate OR 2=yes OR 3=yes → dispatch subagent

**Subagent return contract**: subagent returns only the deliverable path(s). No template dump, no intermediate analysis, no confirmation text.

### Step 1: Identify Candidates

**If no target specified** ("agentify" alone):
- Review conversation for automation candidates
- Look for: verbose outputs, multi-step workflows, repeated patterns
- **MUST use `multiSelect: true`** when presenting candidates (users often want multiple)

**If target specified**:
1. Check local marketplaces first:
   - `~/.claude/plugins/marketplaces/*/plugins/*/`
   - Use `/skill-dedup` command to find overlaps
2. If not found locally, search remote: `WebFetch https://claudemarketplaces.com/?search=[keyword]`
3. If found, recommend existing or extend. If not, proceed to create

**Step 1 Guards (HARD STOP)**:

- **No immediate-execution options**: AskUserQuestion options must all be automation types (Skill/Agent/Rule/Hook/Command). "Just execute now" or "Execute without automation" options are forbidden — claudify's purpose is creating/extending automation, not executing the underlying task.
- **Scope check when extending existing skills**: Before proposing to extend a global skill (`~/.claude/skills/`), verify the change is project-agnostic. Project-specific variables, hostnames, or environment values must NOT be added to global skills. If the automation is project-specific, recommend a project-level skill (`.claude/skills/`) or a project rule (`.claude/rules/`) instead.

### Step 1.5: Merge logic / Grouping / AskUserQuestion

When duplicate or similar automation candidates are found, confirm grouping and merge options with the user using AskUserQuestion.

**Grouping criteria:**
- Similarity in model or functionality
- Contextual similarity
- Keyword grouping (e.g., "openclaw management")

**Merge criteria:**

| Condition | Recommendation |
| --------- | -------------- |
| 3+ similar topics | **multi-topic Skill** |
| Different triggers + same skill | General Agent |
| Simple instructions + Bash script | **Skill** (Agent with skill) |
| Complex multi-step + multiple tools | Agent |

**AskUserQuestion (merge options):**
"Candidates found. How should I structure them?"
options:
  - "Merge related topics into one multi-topic skill (e.g., openclaw: exec/gateway/test)"
  - "Create separate agents for each functionality"
  - "Skill + Agent combination (instruction=skill, implementation=agent)"

**PROHIBITED**: Do not create separate agents without merging candidates into a logical structure if they are related.

### Step 2: Gather Requirements

Use AskUserQuestion to clarify:
- **Triggers**: Commands or conditions that activate the automation
- **Tools**: Required tools or skills
- **Scope**: Global (`~/.claude/`) / Project (`.claude/`)
- **Language**: code comments, variable names, documentation

Question patterns: [askuserquestion-patterns.md](./resources/askuserquestion-patterns.md)

### Step 3: Recommend Type

Use the [automation-decision-guide.md](./resources/automation-decision-guide.md) to recommend the best type.

### Step 4: Create

**CRITICAL**: Follow the creation method for each type. **Apply Step 0 routing first** — multi-template Reads or transcript scans dispatch to subagent.

**Skill with scripts** (If scripts are required, use skill directory structure):
```
skill-name/
├── SKILL.md          # frontmatter + documentation + node scripts/xxx.js (mode)
├── topic-a.md        # topic file
├── topic-b.md        # topic file
└── scripts/
    └── xxx.js        # actual logic (temp location, permanent storage)
```
- Do not create `tmp_*.js` in current directory; move to `scripts/`
- Call in SKILL.md: `node <skill-dir>/scripts/xxx.js <mode>`
- Use relative path from `__dirname` in scripts
- **Separate implementation logic and topic files**

**Skill (no scripts)**: **MUST** use skill-writer (do NOT create directly)
```
Skill tool: skill: "project-automation:skill-writer"
```

**Agent**: Create in `~/.claude/agents/` or `.claude/agents/`
- [agent-templates.md](./resources/agent-templates.md)

**Rules**: Create in `~/.claude/rules/` or `.claude/rules/`
- [rules-guide.md](./resources/rules-guide.md)

**Slash Command**: Create in `~/.claude/commands/` or `.claude/commands/`
- [slash-command-syntax.md](./resources/slash-command-syntax.md)

**Hook**: Add to settings.json
- [hook-examples.md](./resources/hook-examples.md)

**Plugin** (open source):
- [plugin-creation.md](./resources/plugin-creation.md)

### Step 5: Validate

1. Register or copy to target location
2. Reload Claude Code:
   1. Manual sync to cache, OR
   2. New session to reload

**Auto-sync hook**: `plugin-cache-sync.sh` syncs marketplace to cache on Edit/Write

## Output Guidelines

Keep responses concise:
1. List identified candidates (with multiSelect)
2. Summarize the recommended structure (Merge logic)
3. Provide the creation plan

| Context | multiSelect |
| ------- | ----------- |
| Automation candidates | **true** (users often want multiple) |
| **Merge options** (Complexity) | **false** (merge vs separation - mutually exclusive) |
| Type selection | false (mutually exclusive) |
| Scope selection | false (one location) |
| Feature selection | **true** (additive choices) |

## Success Case

**Scenario (2026-03-09)**:
- Found 3 openclaw-related functions
- Proposed 3 options for merging
- Result: Implementation success, user satisfied

**Key factors**:
1. Identification of 3 functions
2. "Merge?" AskUserQuestion
3. merging skills using skill-writer (multi-topic)

## Ralph Mode (AskUserQuestion bypass)

**Detection condition**: do not judge by `.ralph/` presence alone. Ralph mode requires **all** of:
1. `.ralph/` directory exists AND
2. Environment variable `RALPH_LOOP=1` is set (Ralph autonomous loop sets this)

**Even when `.ralph/` exists, an interactive user session is normal mode** — AskUserQuestion works as usual.

**Workflow Change**:

| Step | User Interaction | Workflow |
| ---- | ---------------- | -------- |
| Step 1: Auto-detect | AskUserQuestion (multiSelect) | Summary info to `.ralph/improvements.md` |
| Step 1.5: Merge logic / Structure | - | improvements.md recording |
| Step 2: Requirements | AskUserQuestion | trigger/scope recommendation to improvements.md |
| Step 3: Type recommendation | Recommend only | improvements.md recording |
| Step 4: Implementation | Direct action | **PROHIBITED** - Use `[NEEDS_REVIEW]` tag |
| Step 5: Validation | Validation | **Auto validation** (after changes are complete) |

**improvements.md recording example**

```markdown
## Agentify Candidate (Implementation)

### [Candidate Name]
- **Context**: [Why it was found]
- **Recommended Type**: [Skill/Agent/Hook/Slash Command]
- **Recommended Structure**: [Topics]
- **Rationale**: [Why it's recommended]
- **Tag**: [NEEDS_REVIEW]
```

## Self-Improvement

After changes are complete, **Self-improve based on conversation**:

1. Identify failure and workaround patterns
