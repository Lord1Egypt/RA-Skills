---
name: build-user-profile
description: |
  Build or update the user profile memory by observing workspace context, git history,
  and conversation patterns. Run on first interaction or when profile feels outdated.
  Trigger words: "build profile", "update profile", "who am I", "user profile".
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Agent
---

# Build User Profile

Actively build and maintain a user profile in the agent's memory system.

## When to Run

- **First session** in a new workspace — bootstrap the profile from observable context
- **Profile feels stale** — interests, focus areas, or tech stack have shifted
- **User explicitly asks** to update their profile
- **After major project changes** — new repo added, tech stack shift, role change

## Step 1: Gather Observable Context

Collect signals from the workspace without asking the user. Run these in parallel:

### 1a. Git identity and activity
```bash
git log --all --format='%an <%ae>' | sort -u
git log --oneline -50 --all
git log --since='30 days ago' --oneline --all | head -20
```

### 1b. Project structure
```bash
ls -d */ 2>/dev/null
cat *.yaml *.yml 2>/dev/null | head -50
```

### 1c. Tech stack signals
Look for `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pyproject.toml`, or similar. Read framework choices.

### 1d. Existing memory and feedback patterns
Check for memory files or CLAUDE.md that reveal preferences.

### 1e. Content signals
Check for blog posts, research docs, or README content that reveals interests.

## Step 2: Read Existing Profile

Read the current user profile memory file if it exists. Note what's already captured and what might be outdated.

## Step 3: Synthesize Profile

Build or update the profile with these sections:

```markdown
---
name: {User} User Profile
description: {one-line} — used to tailor collaboration approach
type: user
---

## Role & Focus
- What they do, what projects they're working on

## Technical Strengths
- Languages, frameworks, tools they're strong in
- Areas they're learning or new to

## Work Style
- Autonomy level (do they want to be asked, or just do it?)
- Pace (ship fast vs deliberate?)
- Research habits (deep-dive vs pragmatic?)

## Communication Preferences
- Language preferences
- Verbosity (concise vs detailed?)
- Format preferences (tables, bullet points, prose?)

## Current Interests
- What they're researching or exploring right now
- Include date for staleness detection, e.g. (2026-04)
```

## Step 4: Validate with User

Present the profile summary to the user:

> Here's what I've built from your workspace context. Anything wrong or missing?

Incorporate their feedback immediately.

## Step 5: Write and Index

1. Write/update the user profile memory file
2. Ensure the memory index has a pointer to it
3. If this is a brand new profile, inform the user:

> Profile created. Every new session in this workspace will now start knowing who you are.

## Key Rules

- **Observe first, ask second** — gather as much as possible from context before asking questions
- **No judgments** — profile is for tailoring collaboration, not evaluating the user
- **Date current interests** — so future sessions can detect staleness
- **Keep it under 2KB** — this gets loaded every session; don't bloat it
- **Iterate, don't rewrite** — on updates, patch specific sections rather than regenerating the whole thing
