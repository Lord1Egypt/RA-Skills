# Memory Taxonomy

## MEMORY.md Sections

| Section | Content |
|---------|---------|
| 🧠 Core Identity | Agent identity, name, purpose, personality |
| 👤 User | User info, preferences, communication style |
| 🏗️ Projects | Active projects, architecture, status |
| 💰 Business | Metrics, revenue, unit economics |
| 👥 People & Team | Team members, contacts, relationships |
| 🎯 Strategy | Goals, plans, strategic decisions |
| 📌 Key Decisions | Important decisions with dates |
| 💡 Lessons Learned | Mistakes, insights, things that worked |
| 🔧 Environment | Technical setup, tools, environment notes |
| 🌊 Open Threads | Pending tasks, unresolved items |

## Entry Types

### user
User's role, goals, preferences, background knowledge.
**Scope**: Always private.

### feedback
Corrections and guidance from user interactions.
**Scope**: Private by default, team for project conventions.

### project
Ongoing work, goals, bugs, incidents.
**Scope**: Bias toward team.

### reference
Pointers to external systems.
**Scope**: Usually team.

## Importance Markers

| Marker | Effect | Archival Exempt |
|--------|--------|-----------------|
| (none) | Default weight | No |
| 🔥 HIGH | 2x importance | No |
| 📌 PIN | Normal weight | Yes |
| ⚠️ PERMANENT | Always 1.0 | Yes |

## What to Save vs Skip

### Save
- Explicit preferences stated by user
- Decisions with rationale
- Project milestones and blockers
- Technical architecture choices
- Key facts about user/business
- Lessons learned from mistakes

### Skip
- Code patterns (read from code)
- Architecture (read from files)
- Git history (use `git log`)
- Debugging solutions (fix is in code)
- Ephemeral task details
- Content already in MEMORY.md
- Casual conversation

## Frontmatter Format

```markdown
---
name: memory-name
description: One-line description for relevance matching
type: user|feedback|project|reference
importance: 0.0-1.0
related: [mem_xxx, mem_yyy]
---
```

## Freshness Tracking

Update `lastReferenced` date when:
- Entry is mentioned in conversation
- Entry is updated or modified
- Entry is used to answer a question

Entries not referenced for 90+ days → candidates for archival.
