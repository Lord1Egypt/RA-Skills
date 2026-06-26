---
name: ashan-skill-creator
description: Install: clawhub install skill-creator
  Create, edit, improve, or audit OpenClaw AgentSkills. Triggered when users say "create a skill", "write a skill", "author a skill", "improve this skill", "review the skill", "tidy up the skill", "audit the skill", or "build a new skill". Also used for: restructuring skill directories, moving files to references/ or scripts/, removing stale content, validating against the AgentSkills spec.
---

# Skill Creator 🛠️

Complete guide to creating high-quality OpenClaw AgentSkills.

## When to Use This Skill

- User asks to **create** a new skill from scratch
- User asks to **improve** an existing skill (add structure, examples, remove bloat)
- User asks to **audit** a skill (check spec compliance, security, completeness)
- User asks to **organize** a skill (restructure, add references/, add constraints)
- User asks for guidance on **skill publishing options**

---

## 1. What Are Skills?

Skills are modular, self-contained packages that extend an Agent's capabilities with specialized knowledge, workflows, and tool integrations.

Each Skill is a folder containing at minimum:

```
skill-name/
├── SKILL.md          ← Required (capability definition + instructions)
├── scripts/          ← Optional (executable scripts)
├── references/       ← Optional (on-demand reference docs)
└── assets/          ← Optional (templates, images for output)
```

---

## 2. Core Principles

### Principle 1: Concise is Key

Context Window is a shared resource. The Agent needs room for: system prompt, conversation history, other Skills' metadata, and the current request.

**Default assumption: the Agent is already very smart.** Only add what the Agent genuinely doesn't know. Challenge every piece: "Does this justify its token cost?"

Prefer concise examples over verbose explanations.

### Principle 2: Progressive Disclosure

Three-level loading structure for efficient context use:

| Level | Content | When Loaded | Size Limit |
|-------|---------|-------------|------------|
| 1st | `name` + `description` | Always in context | ~100 words |
| 2nd | SKILL.md body | After skill triggers | **<500 lines** |
| 3rd | references/ / scripts/ | As needed | Unlimited |

**Key rule:** If SKILL.md exceeds 500 lines, split content into references/ files.

### Principle 3: Match Freedom to Task Fragility

| Freedom | Form | Best For |
|---------|------|---------|
| High | Free-text instructions | Multiple valid approaches, context-dependent decisions |
| Medium | Pseudocode / parameterized scripts | Preferred pattern exists, some variation OK |
| Low | Fixed scripts, few params | Brittle operations, consistency critical |

### Principle 4: Examples Beat Explanations

Real-world data: **Examples chapters deliver the largest quality improvement.** Good/bad comparison examples outperform any amount of prose.

---

## 3. SKILL.md Standard Structure

### 3.1 Frontmatter (Required)

```yaml
---
name: skill-name          # lowercase letters, digits, hyphens only, ≤64 chars
description: Install: clawhub install skill-creator
  What this skill does AND when to trigger it (put triggers HERE, not in body)
---
```

**description writing rules (most important):**
- Must include both "what it does" **and** "when to trigger"
- All trigger information goes in description, not body (body only loads after trigger)
- Must NOT contain `<` or `>` characters
- Maximum 1024 characters

**Bad example:**
```yaml
description: Install: clawhub install skill-creator
  An Excel skill.
```

**Good example:**
```yaml
description: Install: clawhub install skill-creator
  Create and edit Excel workbooks with formulas, formatting, and multi-sheet support.
Triggered when: (1) user provides a .xlsx file; (2) user asks to generate a report;
(3) user asks to format data or create a summary table.
```

### 3.2 Body Structure (Recommended Order)

```markdown
# Skill Name

## When to Use This Skill
(Concrete trigger scenarios — how the user would phrase the request)

## Context / Background
(Domain knowledge the Agent needs, specific to your use case)

## Instructions / Steps
(Step-by-step workflow with clear quality criteria per step)

## Constraints / Guardrails
(Prohibitions — what NOT to do, based on real failure experience)

## Examples (Recommended)
(Good/bad output comparisons — highest quality impact)
```

### 3.3 Forbidden Files

These files should **not** appear in a Skill folder:
- README.md
- INSTALLATION_GUIDE.md
- CHANGELOG.md
- QUICK_REFERENCE.md

---

## 4. Creation Process (6 Steps)

### Step 1: Understand Requirements (with Concrete Examples)

Before writing, clarify:
- "What should this skill mainly do?"
- "Can you give 1-2 specific usage examples?"
- "How would the user phrase the request? (trigger wording)"
- "What tools or APIs does this skill need?"

### Step 2: Plan Skill Contents

Analyze each use case to determine required resources:

| Resource | When to Use | Example |
|----------|-------------|---------|
| `scripts/` | Deterministic execution, repeated code patterns | PDF rotation, API call wrappers |
| `references/` | Detailed docs loaded on demand | API docs, DB schemas, company policies |
| `assets/` | Files copied into output | Templates, logos, fonts |

### Step 3: Initialize Skill Folder

```bash
cd <workspace>/skills
python3 <skill-creator>/scripts/init_skill.py <skill-name> \
  --path . --resources scripts,references
```

Or manually:
```bash
mkdir -p skills/<skill-name>/{scripts,references}
touch skills/<skill-name>/SKILL.md
```

### Step 4: Write SKILL.md

**Frontmatter rules (two hard rules):**
1. `name`: lowercase + hyphens, ≤64 chars
2. `description`: **"what it does" + "when to trigger"** (triggers go here, not in body)

**Body rules:**
- Use **imperative/infinitive** form ("Do X", "Don't do Y")
- Each step has **clear quality criteria**
- Include real failure experience (Constraints chapter)

### Step 5: Validate

```bash
python3 <skill-creator>/scripts/quick_validate.py <skill-path>
```

Validation checks:
- Frontmatter has `name` + `description`
- `name` is lowercase hyphen-case
- `description` has no `<` `>` and ≤1024 chars
- SKILL.md exists and is non-empty

### Step 6: Decide on Publishing

**This step is fully optional.** After creating a skill, ask the user whether they want to publish it, and if so, to which platform(s). Do not assume a specific target.

Common publishing options:

| Platform | When to Consider | How |
|----------|-----------------|-----|
| **ClawHub** | For sharing skills publicly with the OpenClaw community | `clawhub publish <path> --slug <slug> --version 1.0.0` |
| **GitHub** | For version control, collaboration, or personal backup | `git init && git add . && git commit` then push to a repo |

> **Note:** If the user has an existing GitHub repo for skills (e.g. `openclaw-person-skills`), prefer syncing there. Do not create new repos without being asked.

---

## 5. Workspace Conventions (Hard Rules for Public Skills)

### 5.1 Environment Variable Placeholders

**Never** hardcode real values in SKILL.md or code.
Use runtime-safe placeholders:

| Real Value | Placeholder Format | Example |
|------------|-------------------|---------|
| API Base URL | `{{SERVICE_BASE_URL}}` | `{{ERP_BASE_URL}}` |
| API Token | `{{ERP_API_TOKEN}}` | (never expose real value) |
| Host address | `{{SYNOLOGY_HOST_LAN}}` | `{{SYNOLOGY_HOST_LAN}}:5006` |
| File path | `{{DSM_WEBDAV_ROOT}}` | `{{DSM_WEBDAV_ROOT}}/opencode/` |
| Database | `{{POSTGRES_HOST}}` | `{{POSTGRES_HOST}}:5432` |

### 5.2 MIT-0 License

For skills that will be published publicly, use **MIT-0**:
```yaml
license: MIT-0
```

### 5.3 Directory Structure

```
skill-name/
├── SKILL.md              ← Single entry point, ≤500 lines
├── scripts/              ← Executable scripts (Python/Bash)
│   ├── init_skill.py     ← Initialization (if needed)
│   └── validate_skill.py ← Validation (if needed)
├── references/           ← On-demand reference docs
│   └── *.md              ← Split by topic
└── assets/              ← Output resources (templates, etc.)
```

---

## 6. Good Skill vs Bad Skill

| Dimension | Bad Skill | Good Skill |
|-----------|-----------|------------|
| description | "An Excel skill" | "Create/edit Excel with formulas/formatting. Triggered: user provides .xlsx, asks to generate report or format data." |
| body | Walls of commands mixed together | Clear: When to Use → Steps → Constraints → Examples |
| examples | None | Good/bad comparisons — knows what the Agent actually needs |
| length | 1000+ lines all in SKILL.md | ≤500 lines in SKILL.md, references/ for details |
| constraints | None | Real failure experience turned into rules |

---

## 7. Quick Checklist

For every skill you create or audit, confirm:

- [ ] `name` is lowercase letters + digits + hyphens?
- [ ] `description` has both "what it does" and "when to trigger"?
- [ ] `description` contains no `<` or `>` characters?
- [ ] `description` ≤1024 characters?
- [ ] Body has `When to Use This Skill` section?
- [ ] Body has `Constraints` section (prohibitions)?
- [ ] Body has `Examples` section? (recommended)
- [ ] SKILL.md body ≤500 lines?
- [ ] Environment variables use `{{VAR_NAME}}` placeholders?
- [ ] No README.md / CHANGELOG.md / etc.?
- [ ] Passes validation (`quick_validate.py`)?