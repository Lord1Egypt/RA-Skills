---
name: clear-mind
description: "Memory file maintenance and optimization system. Use when factual information (portfolio, projects, technical details) accumulates in MEMORY.md, or when periodic memory cleanup is needed. Migrates factual content to separate files, keeps only core rules and indexes in MEMORY.md, maintains Quick Index table for navigation. Size/line count is NOT a trigger — only factual bloat matters."
---

# Clear-Mind Skill

Memory hygiene system to prevent MEMORY.md bloat.

## When to Use

Activate this skill when:
- **Factual information (portfolio, projects, technical details) accumulates in MEMORY.md** — Primary trigger condition
- Memory cleanup is requested
- Periodic maintenance (recommended monthly)

**Important**: Do NOT use file size (lines/tokens) as the trigger. A large MEMORY.md with only core rules is fine. Only act when factual bloat is detected.

## Pre-Flight: First-Run User Check

Before starting the first clear-mind task:

> "**Note**: The following categories will be kept in MEMORY.md for quick access:
> - **Installed Skills list** — needed for every task
> - **Technical Setup** — agent capabilities and frequent-use configs
> 
> Only factual information used for specific scenarios (projects, portfolio, historical events) will be migrated.
>
> Are there any other factual categories you'd like to keep in MEMORY.md?"

Wait for user confirmation before proceeding to Core Workflow.

## Content Migration Rules

### KEEP in MEMORY.md
- **Core behavioral rules** (Honesty, Temporal Verification, etc.) — immutable principles
- **Task index** (name + path only) — for navigation
- **Quick Index table** — for factual information access
- **Minimal architecture notes** — essential system structure
- **All Technical Setup** — agent capabilities, installed skills, configs, tools that are frequently accessed. If it's about "what I can do," it stays.
- **Any information that defines the agent's identity or capabilities** — this is core functionality

### MOVE to facts/
- **Historical events and incidents** — specific past occurrences
- **Project details and statuses** — concrete project information
- **Portfolio holdings** — specific investment data
- **User preference lists** — specific user choices
- **Scenario-specific information** — data relevant only to particular situations

### DELETE
- **Redundant summaries** — information already captured elsewhere
- **Outdated temporary notes** — expired or irrelevant information
- **Information already in other systems** — duplicate data

### Clear Distinction Guidelines

#### DEFINITELY KEEP in MEMORY.md (NO EXCEPTIONS)
- Rules that define agent behavior
- Instructions for how the agent should operate
- Capabilities and limitations
- Installed skills list
- Tool descriptions and usage guidelines
- System architecture fundamentals

#### DEFINITELY MOVE to facts/
- Specific dates and events
- Project names, deadlines, and statuses
- Financial data and investment holdings
- User-specific preferences (e.g., "I prefer blue themes")
- Historical interactions and their outcomes

**Migration Principle**: Only move facts that are scenario-specific (this project, that stock, past events). Capabilities stay, specifics go.

**Critical Safeguard**: When in doubt, KEEP in MEMORY.md. It's safer to retain information in the core memory than to risk losing important capabilities.

## Core Workflow

### Phase 1: Analyze Current State

1. Read current MEMORY.md
2. **Check for factual bloat**: Are there sections containing specific data that belongs elsewhere?
3. Identify content categories:
   - **Core Rules** (keep in MEMORY.md)
   - **Factual Information** (migrate to facts/)
   - **Task Indexes** (keep minimal version)
   - **Redundant Content** (consolidate or remove)

**Skip if**: MEMORY.md contains only core rules and indexes — even if the file is large.

### Phase 2: Create facts/ Directory Structure

Ensure `/memory/facts/` exists with these files:

```
memory/facts/
├── critical-events.md    # Important incidents and lessons
├── projects.md           # Active project statuses
├── technical-setup.md    # DEPRECATED — technical configs now stay in MEMORY.md
├── portfolio.md          # Stocks, investments, strategies
└── user-directives.md    # User preferences and instructions
```

**Note**: `technical-setup.md` is kept for backward compatibility. New technical content goes to MEMORY.md.

### Phase 3: Migrate Content

Move factual details from MEMORY.md to appropriate facts/ files:

| Source Section      | Target File          | Migration Rule                                                                                |
|---------------------|----------------------|-----------------------------------------------------------------------------------------------|
| Critical Events     | critical-events.md   | Move full details, keep index link                                                            |
| Projects            | projects.md          | Move all project details                                                                      |
| Technical Setup     | technical-setup.md   | **KEEP in MEMORY.md** — agent capabilities stay; only move niche/deprecated configs if requested |
| Portfolio/Trading   | portfolio.md         | Move holdings, strategies                                                                     |
| User Directives     | user-directives.md   | Move preferences, quotes                                                                      |

### Phase 4: Rewrite MEMORY.md

New structure:

```markdown
# MEMORY.md - Long-Term Memory

_Curated rules and index. Detailed facts stored separately._

---

## Tasks, Plans and Missions

### [Task Name]
**Current Plan**: /memory/YYYY-MM-DD.md

---

## Quick Index (Factual Information)

| Category        | Location                              |
|-----------------|---------------------------------------|
| Critical Events | /memory/facts/critical-events.md      |
| Active Projects | /memory/facts/projects.md             |
| Technical Setup | **MEMORY.md** (agent capabilities)    |
| Portfolio       | /memory/facts/portfolio.md            |
| User Directives | /memory/facts/user-directives.md      |

---

## Core Principles (Immutable)

[Keep only essential rules - max 6-8 items]

---

## Cognitive Memory System

[Minimal reference to architecture]
```

### Phase 5: Verify

Check results:
- [ ] All facts/ files created with migrated content
- [ ] No information lost
- [ ] Quick Index table complete
- [ ] Core Principles preserved
- [ ] Factual bloat removed (not line count reduced)

## Rollback Mechanism

### When to Use Rollback

Activate rollback when:
- User requests to restore specific categories of information
- Migration resulted in unintended data loss
- User wants to revert to previous memory structure

### Rollback Workflow

1. **Assessment**: Determine which categories need to be restored
2. **Backup Current State**: Create backup of current MEMORY.md and facts/ directory
3. **Selective Restoration**:
   - **Specific Category**: Copy content from facts/ file back to MEMORY.md
   - **Entire Memory**: Restore from backup or rebuild from facts/ files
4. **Update Quick Index**: Adjust links based on new structure
5. **Verification**: Ensure all content is properly restored

### Rollback Scenarios

| Scenario                 | Action                                                                 |
|--------------------------|------------------------------------------------------------------------|
| Restore specific category| Copy content from facts/[category].md back to MEMORY.md                |
| Rollback entire memory   | Rebuild MEMORY.md from all facts/ files and core rules                 |
| Undo recent migration    | Restore from pre-migration backup if available                         |

## Success Metrics

- **Factual bloat removed** — all migrated content is factual, not core rules
- **All factual information preserved** in facts/ files
- **Quick Index enables fast navigation** between core memory and facts
- **Core rules and capabilities remain intact** in MEMORY.md
- **Rollback capability maintained** with proper backups
- **User verification completed** at key decision points
- **No critical information lost** during the process

**Critical Safety Metrics**:
- 100% of core behavioral rules remain in MEMORY.md
- 100% of capability definitions are preserved
- 100% of tool descriptions remain unchanged
- 100% of installed skills information is retained

**Anti-Goal**: Reducing line count is NOT the goal. Removing factual bloat while preserving core capabilities IS.

## Template: facts/ Files

### critical-events.md
```markdown
# Critical Events Record

## YYYY-MM-DD: Event Name
- **What happened**: [Description]
- **Root cause**: [Analysis]
- **Lesson**: [Key takeaway]
- **Status**: [Resolved/Ongoing]
```

### projects.md
```markdown
# Active Project Status

## Project: [Name]
- **Status**: [PENDING/ACTIVE/COMPLETED]
- **User role**: [Role]
- **My role**: [Role]
- **Constraints**: [Any limitations]
```

### technical-setup.md
```markdown
# Technical Setup & Configuration (ARCHIVE)

> **DEPRECATED**: Technical configurations and installed skills are now kept in MEMORY.md for quick access.
> This file is maintained for historical reference only.

## Archived Content
[Any legacy technical notes from before the migration]
```

### portfolio.md
```markdown
# Portfolio & Strategies

## Holdings
- **Symbol**: [Ticker]
- **Quantity**: [Number]
- **Purchase price**: [Amount]
- **Current price**: [Amount]
- **Status**: [HOLD/SELL/BUY]

## Strategies
- **Strategy name**: [Name]
- **Description**: [Details]
- **Performance**: [Metrics]
```

### user-directives.md
```markdown
# User Directives & Preferences

**Last Updated**: YYYY-MM-DD

> "[User quote or directive]"

## Preferences
- [Preference 1]
- [Preference 2]

## Instructions
- [Instruction 1]
- [Instruction 2]
```

## Remember

**MEMORY.md is for rules and navigation, not storage.**

Factual details belong in specialized files.

**Rollback capability is essential** — always maintain backups and ensure the ability to restore information when requested.
