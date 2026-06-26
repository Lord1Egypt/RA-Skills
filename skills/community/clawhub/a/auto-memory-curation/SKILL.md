---
name: auto-memory-curation
description: Automatically analyzes messages for important information and stores it in the right memory files. Runs silently on every message. Filters noise, captures meaningful content. Use when you want passive memory building without manual "remember this" commands.
version: 1.0.0
---

# Auto Memory Curation Skill

## Overview
Silently analyze every message for important information and store it appropriately. Reduces manual memory management while building rich context over time.

## How It Works

### Trigger
- Runs on every message (silently)
- No user activation needed

### Analysis Pipeline

**Step 1: Filter Noise**
Skip these message types:
- Greetings (hi, hello, hey)
- Thanks/thanking
- Acknowledgments (ok, sure, yes, yeah)
- Questions without context
- Single word responses
- Bot commands

**Step 2: Categorize**
For non-noise messages, categorize:

| Category | What to look for | Store in |
|----------|------------------|----------|
| **Fact** | New info about user, projects, preferences | MEMORY.md |
| **Decision** | Choices made, conclusions reached | memory/YYYY-MM-DD.md |
| **Preference** | Likes, dislikes, style preferences | USER.md |
| **Idea** | Random thoughts, inspiration, concepts | memory/topics/ideas.md |
| **Learning** | Lessons, insights, discoveries | memory/topics/lessons.md |
| **Project** | Project updates, progress, blockers | memory/projects/ |
| **Goal** | Goals, targets, milestones | memory/topics/goals.md |
| **Error** | Mistakes, corrections to avoid | memory/topics/anti-patterns.md |
| **Commitment** | Promises I make, tasks to do | tasks.md |

**Step 3: Extract & Store**
- Extract the key information
- Add timestamp reference
- Store in appropriate file
- Use append mode (never overwrite)

### Guidelines

#### What to Capture
- New facts about Vini (name, preferences, goals)
- Project updates or decisions
- Ideas for future projects
- Learning insights
- Corrections (what doesn't work)
- Commitments I make

#### What to SKIP
- Passwords, secrets, API keys
- Trivial acknowledgments
- Basic confirmations
- Questions I'm asking
- Technical errors that are fixed

### Quality Rules

1. **Be selective** - Don't store everything
2. **Be concise** - One sentence per memory
3. **Be contextual** - Include enough info to understand later
4. **Be accurate** - Don't paraphrase incorrectly
5. **Never duplicate** - Check if already stored

### Format

```
## [Category] - YYYY-MM-DD

- **[What]:** [Brief description]
  *Context:* [Why it matters or relevant message]
```

### Examples

**User says:**
> "I prefer concise messages, no filler words"

**Stored in USER.md:**
> ## Preference - 2026-03-06
> - **Communication:** Prefers concise messages, no filler words

---

**User says:**
> "Let's build a landing page for the consultancy inspired by Nexus AI"

**Stored in memory/2026-03-06.md:**
> ## Decision - 2026-03-06
> - **Consultancy:** Will use Nexus AI style for landing page

---

**User says:**
> "I realized I work better with visual examples first, then theory"

**Stored in MEMORY.md:**
> ## Learning - 2026-03-06
> - **Learning Style:** Visual examples first, theory after

---

## Testing

Periodically review stored memories to calibrate:
- Am I capturing too much noise?
- Am I missing important things?
- Are categories correct?

Adjust based on quality of accumulated memories.

## Override

User can disable or adjust this skill at any time by saying:
- "Don't store that"
- "Clear recent memories"
- "Adjust memory curation"
