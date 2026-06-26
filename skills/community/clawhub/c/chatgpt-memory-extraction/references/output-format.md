# Output Format Specification

## Directory Structure

```
{output_dir}/
├── timeline/                  # Core: quarterly records (most detailed, source of truth)
│   ├── {year}/
│   │   ├── Q1.md              # January - March
│   │   ├── Q2.md              # April - June
│   │   ├── Q3.md              # July - September
│   │   └── Q4.md              # October - December
│   └── ...
│
├── people/                    # Person profiles (extracted from timeline)
│   ├── {category}/            # e.g., teachers/, peers/, family/, colleagues/
│   │   └── {person-name}.md
│   └── _index.md              # Index: who appears where in the timeline
│
├── topics/                    # Thematic extracts (distilled from timeline)
│   ├── academic-journey.md    # Academic milestones, research evolution
│   ├── emotional-events.md    # Significant emotional moments
│   ├── papers-read.md         # Papers/literature discussed
│   ├── skills-learned.md      # Skills, tools, knowledge acquired
│   └── life-changes.md        # Housing, finances, health, travel, etc.
│
├── meta/                      # Metadata and progress tracking
│   ├── conversation-index.md  # Index of all conversations (auto-generated)
│   └── extraction-log.md      # Progress: which quarters are done, review status
│
└── raw/                       # Raw extracted conversation texts (for verification)
    ├── {year}_Q{n}/
    │   └── {idx}_{mmdd}_{title}.txt
    └── conversation-index.md
```

## Timeline File Format

Each quarterly file follows this structure:

```markdown
# {Year} Q{N} ({Month Range})

> Extraction date: YYYY-MM-DD
> Conversations in this quarter: N
> Data source: ChatGPT export

## Quarter Overview
(Brief summary of the user's overall state, major events, and themes during this quarter)

## {Month Name}

### [{MM/DD}] Conversation Title
- **Context**: What prompted this conversation (if apparent)
- **Content**: Detailed description of what was discussed, what the user said, what they learned, what they decided. Use the user's primary language. Include direct quotes for important statements.
- **People mentioned**: Names and roles of anyone referenced
- **Emotional state**: How the user was feeling (if expressed)
- **Academic/professional content**: Research discussed, papers read, skills learned
- **Life events**: Practical matters discussed
- **Notable quotes**: User's own words that capture something important

(Repeat for each conversation in the month)

## Quarter Summary

### Academic Progress
(Key academic milestones and developments)

### Emotional State
(Overall emotional trajectory across the quarter)

### Relationships
(Changes in interpersonal dynamics)

### Life Events
(Significant practical life changes)
```

## People File Format

```markdown
# {Person Name}

- **Identity**: Role, affiliation, relationship to user
- **First appearance**: Date and conversation context
- **Current status**: Latest known information

## Key Interactions
(Chronological list of significant interactions, each referencing the timeline)

### {Date} — {Brief description}
- What happened
- How the user felt about it
- → See timeline/{year}/Q{n}.md for full context

## User's Perception
(How the user describes or feels about this person, using direct quotes when available)
```

## Topics File Format

Each topic file is a thematic index that references the timeline:

```markdown
# {Topic Title}

> Last updated: YYYY-MM-DD

## Chronological Entries

### [{Date}] {Brief description}
- Summary of what happened
- → See timeline/{year}/Q{n}.md
```

## Extraction Log Format

```markdown
# Extraction Progress

| Year | Quarter | Status | Conversations | Reviewed | Notes |
|------|---------|--------|---------------|----------|-------|
| 2023 | Q1      | ✅ Done | 1             | ✅ Yes   |       |
| 2023 | Q2      | ✅ Done | 25            | ✅ Yes   |       |
| ...  | ...     | ...    | ...           | ...      | ...   |
```
