# Memory Types Reference

This document describes the different memory types and when to use each.

## Memory Types

### 1. Preference
**Purpose:** User preferences, coding style, tool choices, configuration decisions.
**Expiry:** Never expires (permanent)
**Score weight:** Highest (1.0)

**Examples:**
```yaml
{
  "type": "preference",
  "content": "User prefers Python for automation scripts",
  "tags": ["coding", "python", "automation"]
}
```

```yaml
{
  "type": "preference", 
  "content": "User is in UTC timezone",
  "tags": ["timezone", "config"]
}
```

### 2. Decision
**Purpose:** Decisions made, approvals, blocking choices, go/no-go decisions.
**Expiry:** Never expires (permanent)
**Score weight:** High (0.9)

**Examples:**
```yaml
{
  "type": "decision",
  "content": "Approved inbox-triage skill for publishing",
  "tags": ["income", "skills", "approval"]
}
```

```yaml
{
  "type": "decision",
  "content": "Chose memory-augment as second skill to build",
  "tags": ["income", "strategy"]
}
```

### 3. Learning
**Purpose:** What the agent learned, patterns discovered, corrections made.
**Expiry:** Never expires (permanent)
**Score weight:** Medium (0.85)

**Examples:**
```yaml
{
  "type": "learning",
  "content": "Sub-agent spawning reduces context by ~30%",
  "tags": ["pattern", "optimization"]
}
```

```yaml
{
  "type": "learning",
  "content": "User responds better to concise summaries",
  "tags": ["pattern", "communication"]
}
```

### 4. Context
**Purpose:** Session context, project state, ongoing work, temporary notes.
**Expiry:** 7 days default (configurable)
**Score weight:** Lower (0.7)

**Examples:**
```yaml
{
  "type": "context",
  "content": "Building memory-augment skill, 60% complete",
  "tags": ["project", "development"]
}
```

```yaml
{
  "type": "context",
  "content": "Waiting for user feedback on inbox-triage",
  "tags": ["waiting", "feedback"]
}
```

## Best Practices

### Use Preference for:
- ✅ User preferences and choices
- ✅ Coding style guidelines
- ✅ Tool and technology preferences
- ✅ Configuration decisions

### Use Decision for:
- ✅ Approval/rejection decisions
- ✅ Go/no-go choices
- ✅ Strategy decisions
- ✅ Income decisions

### Use Learning for:
- ✅ Patterns discovered
- ✅ Lessons learned
- ✅ Optimization insights
- ✅ Agent behavior learnings

### Use Context for:
- ✅ Session notes
- ✅ Ongoing work status
- ✅ Temporary tracking
- ✅ Waiting items

## Scoring Formula

```
score = (content_match * 0.4) + (tag_match * 0.3) + (type_weight * 0.2) + (recency * 0.1)
```

Type weights:
- preference: 1.0
- decision: 0.9
- learning: 0.85
- context: 0.7

Recency bonus (decays over 30 days):
- 1.0 on creation day
- 0.5 at 15 days
- 0.0 after 30 days

## Tag Organization

Use tags for categorization:
```yaml
# Income/skills tags
tags: ["income", "skills", "clawhub"]

# Project tags
tags: ["project", "development", "memory-augment"]

# Type tags
tags: ["preference", "decision", "learning"]

# Domain tags
tags: ["coding", "python", "automation"]
```

## Examples by Use Case

### User asks: "What did I decide about income?"
**Best memory to return:**
```yaml
{
  "type": "decision",
  "content": "Approved inbox-triage skill for publishing",
  "tags": ["income", "skills"]
}
```

### User asks: "What are my coding preferences?"
**Best memory to return:**
```yaml
{
  "type": "preference",
  "content": "User prefers Python for automation scripts",
  "tags": ["coding", "python"]
}
```

### User asks: "Where are we on memory-augment?"
**Best memory to return:**
```yaml
{
  "type": "context",
  "content": "Building memory-augment skill, 60% complete",
  "tags": ["project", "memory-augment"]
}
```

---

Built for the OpenClaw ecosystem.
