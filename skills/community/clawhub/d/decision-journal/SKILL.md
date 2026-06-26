---
name: decision-journal
description: Record, track, and analyze personal or professional decisions with structured reflection. Use when the user wants to (1) document a decision they're making or have made, (2) review past decisions and their outcomes, (3) analyze decision patterns and learn from them, (4) create a decision-making framework, or (5) reflect on decision quality and outcomes. Triggers on phrases like "record decision", "decision log", "track my decisions", "analyze my choices", "reflect on my decision", "decision review".
---

# Decision Journal

> ⚠️ **免责声明**：本工具仅用于个人或职业决策的记录、回顾与反思，不构成心理咨询、医疗建议、法律意见、投资建议或其他专业判断。涉及情绪危机、自伤/伤人风险、医疗、法律或高风险投资时，应立即寻求相应专业人士或当地紧急支持资源。

A structured system for capturing, organizing, and learning from decisions.

## Quick Start

### Record a New Decision

```
/decision "Should I take the new job offer?"
- Context: Current role stable but stagnant, new offer 30% higher pay but more travel
- Options: (1) Stay, negotiate raise (2) Accept new role (3) Decline and keep looking
- Decision: Accept new role
- Reasoning: Growth opportunity outweighs lifestyle impact; can reassess in 6 months
- Expected outcome: Higher salary, new skills, possible travel fatigue
- Review date: 2025-09-15
```

### Review Past Decisions

```
/decision review
/decision review --last 5
/decision review --tag career --status pending
```

## Capability Boundaries

### Tier 1: Currently Supported (Core)
- record and store structured decisions with context, options, reasoning
- review past decisions and capture outcomes/lessons
- list and filter decisions by tag, status, date
- basic statistics and pattern analysis
- export decision data for personal review (JSON/Markdown/CSV)
- review reminders and due date tracking

### Tier 2: Ready with Light Engineering
- calendar integration for review reminders
- advanced pattern detection across decisions
- decision quality scoring algorithms
- backup/sync across devices

### Tier 3: Explicitly Not Supported
- mental health counseling, diagnosis, or crisis support
- telling the user which life choice is objectively "best"
- medical, legal, investment, or other licensed professional advice
- handling self-harm, suicide, violence risk, or acute mental health emergencies inside the normal workflow

If the user is actually asking for emotional stabilization, crisis support, or psychological guidance, do not force this skill. Route to a more appropriate support flow instead.

## High-Risk Escalation

⚠️ **Stop the normal decision-journal flow immediately** if the user expresses any of the following:
- self-harm or suicide thoughts
- intent to harm other people
- overwhelming despair or inability to stay safe
- obvious acute mental-health crisis that makes structured reflection inappropriate

Use a direct response like:

> ⚠️ 重要提示：现在不适合继续做普通决策记录。若你有伤害自己或他人的想法，或已难以保证自身安全，请立即联系身边可信任的人，并尽快联系当地急救、医院急诊、心理危机干预热线或持证专业人士。

Then keep the tone calm, direct, and serious. Do not continue normal prompts such as options, reasoning, or review dates until safety is addressed.

## Core Concepts

Each decision entry captures:

| Field | Purpose |
|-------|---------|
| **Situation** | What prompted the decision |
| **Options** | Alternatives considered |
| **Decision** | What was chosen |
| **Reasoning** | Why this choice was made |
| **Expected** | Anticipated outcomes |
| **Review Date** | When to evaluate results |
| **Outcome** | Actual results (added later) |
| **Lessons** | Insights gained |

## Commands

### `/decision <title>`
Record a new decision interactively or with inline details.

**Options:**
- `--tag <tag>`: Categorize (career, finance, health, relationships, etc.)
- `--importance <1-5>`: Significance level
- `--reversible <yes/no>`: Whether decision can be undone
- `--review <date>`: When to evaluate outcomes

### `/decision list`
Show recent decisions with status.

**Filters:**
- `--tag <tag>`: Filter by category
- `--status <pending/completed/review>`: Filter by status
- `--last <n>`: Show last N decisions
- `--since <date>`: From date onward

### `/decision review <id>`
Review and update a specific decision with outcomes.

### `/decision analyze`
Analyze decision patterns and quality over time.

**Reports:**
- `--timeframe <period>`: Analysis period (30d, 90d, 1y, all)
- `--tag <tag>`: Analyze specific category
- `--type <accuracy/speed/patterns>`: Report type

### `/decision export`
Export decision history to various formats.

**Formats:**
- `--format markdown`: Readable document
- `--format json`: Structured data
- `--format csv`: Spreadsheet compatible

## Storage

Decisions are stored in:

```
~/.openclaw/decisions/
├── decisions.jsonl     # Append-only decision log
├── reviews.jsonl       # Review records
├── patterns.json       # Extracted patterns
├── index.json          # Searchable index
└── templates/
    ├── default.md      # Standard decision template
    ├── quick.md        # Minimal template
    └── strategic.md    # Complex decision template
```

## Workflow Patterns

### Pattern 1: Capture in the Moment

When facing a decision, quickly log the key elements before deciding:

```
/decision "Which vendor to choose for project X?"
- Vendor A: Cheaper, less proven
- Vendor B: 20% more expensive, strong track record
- Vendor C: New entrant, innovative approach

[After deliberation]
Decision: Vendor B
Reason: Risk mitigation worth the premium for critical project
Review: 2025-06-01
```

### Pattern 2: Scheduled Review

Set review dates for important decisions:

```
/decision review --due
# Shows all decisions where review date has passed
# Update with actual outcomes and lessons
```

### Pattern 3: Decision Pre-mortem

Before committing, imagine the decision failed:

```
/decision "Pre-mortem: Project launch failed"
- What went wrong? Market timing off
- What signals did we miss? Competitor moved faster
- What would we do differently? Earlier soft launch

Now: Adjust plan based on these insights
```

## Decision Quality Framework

When reviewing decisions, assess:

1. **Process Quality**
   - Did I consider enough options?
   - Did I gather relevant information?
   - Did I account for biases?

2. **Outcome Quality**
   - Did the expected outcomes materialize?
   - Were there unexpected consequences?
   - Am I satisfied with the result?

3. **Learning Value**
   - What would I do differently?
   - What patterns emerge across decisions?
   - How has my decision-making improved?

## Integration

### With Calendar

Link review dates to calendar reminders:

```
/decision "Should I invest in X?"
--review 2025-12-01
--calendar-reminder "Review investment decision"
```

### With Notes

Reference related notes or documents:

```
/decision "Office relocation decision"
--reference [[meeting-notes/2025-03-01]]
--reference [[budget-analysis-q1]]
```

## Templates

See [templates/](templates/) for decision frameworks:

- **WRAP** (Widen options, Reality-test, Attain distance, Prepare)
- **10-10-10** (How will I feel in 10 min/10 months/10 years?)
- **Pros/Cons/Consequences** (Weighted analysis)
- **Decision Matrix** (Criteria-based scoring)

For detailed template usage, see [references/templates.md](references/templates.md).

## Analysis & Insights

The skill can generate reports on:

- **Decision velocity**: How quickly you decide
- **Decision types**: What you decide most often
- **Outcome accuracy**: Expected vs. actual results
- **Bias patterns**: Overconfidence, sunk cost, etc.
- **Improvement trends**: Decision quality over time

For analysis methodology, see [references/analysis.md](references/analysis.md).

## CLI Usage

The skill provides a CLI tool `decision`:

```bash
# Add a new decision
decision add "Title" --situation "..." --options "A|B|C" --decision "A" --review 2025-06-01

# List decisions
decision list --last 10 --tag career

# Review a decision
decision review <id> --outcome "..." --lessons "..." --satisfaction 4

# Analyze patterns
decision analyze --timeframe 90d

# Export data
decision export --format markdown --output decisions.md

# Check for pending reviews
decision remind
```
