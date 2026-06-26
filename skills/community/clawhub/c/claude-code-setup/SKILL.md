---
name: claude-code-setup
description: Setup production-grade .claude/ AI collaboration layer for projects. Use when an agent starts using Claude Code for development, enters a new project directory, or when user mentions "Claude Code", ".claude config", "AI collaboration layer", or "project standards".
license: MIT
metadata:
  author: Eave
  version: "1.0.1"
---

# Claude Code Setup

Setup production-grade \`.claude/\` AI collaboration layer for projects.

## Overview

This skill ensures projects have a proper \`.claude/\` configuration before agents start development work with Claude Code. It acts as a supervisor to maintain and enforce project standards.

## Important: Target Project Directory

**.claude/ must be created in the target project directory, NOT in your workspace root.**

Example:
- ❌ Wrong: `/home/user/workspace-xiaolong/.claude/` (workspace root)
- ✅ Correct: `/home/user/eave-web/.claude/` (actual project being developed)

Always identify which project you're working on first, then check/create `.claude/` in **that** directory.

## When to Use

- Starting a new development task with Claude Code
- Entering a new project directory  
- User mentions "Claude Code", ".claude", "AI collaboration layer", or "project standards"

## Workflow

### Step 1 — Check First

Always check if \`.claude/\` directory already exists **in the target project directory**:

\`\`\`bash
ls -la .claude/ 2>/dev/null
\`\`\`

### Step 2 — If Missing → Create

If the project doesn't have \`.claude/\` directory, **create it first** before development:

\`\`\`bash
node ~/.openclaw/skills/claude-code-setup/index.js
\`\`\`

### Step 3 — If Exists → Supervise

If \`.claude/\` already exists:
- ✅ **DO NOT overwrite** existing files
- ✅ **DO NOT recreate** the structure
- ✅ Let Claude Code naturally maintain and update during development

### Step 4 — Be a Supervisor

Your role is **supervisor**, not executor:
- Ensure Claude Code follows rules in \`.claude/\`
- During development, let Claude Code update configs based on actual code
- Periodically review if \`.claude/\` content matches the project reality

## Core Principles

1. **CLAUDE.md is core** — Highest priority project instructions
2. **Modular** — Separate rules/skills/context
3. **Clear directives** — Use MUST/ALWAYS/NEVER
4. **Project context** — Must include project overview and tech stack
5. **Don't reinvent** — Reuse and maintain existing configs

## .claude/ Directory Structure

\`\`\`
.claude/
├── CLAUDE.md              # ⭐ Project-level global instructions (most important)
├── rules/                 # Team rule library
│   ├── frontend.md
│   ├── typescript.md
│   └── commit.md
├── context/               # Project context knowledge
│   ├── project.md
│   └── stack.md
├── skills/                # Project-private skills
│   └── generate-crud.md
└── prompts/               # Reusable prompt templates
    └── review.md
\`\`\`

## Common Mistakes to Avoid

❌ Writing as requirements doc or README  
❌ Vague rules ("try to", "should")  
❌ Only CLAUDE.md without modularity  
❌ Missing project context  
❌ Overwriting existing configs  
❌ Redundant recreation

## Collaboration with Claude Code

When using Claude Code:

1. **Before starting**: Ensure \`.claude/\` exists
2. **During development**: Let Claude Code reference rules in \`.claude/\`
3. **After completion**: Update \`.claude/\` with any new standards learned

## Template Files

See \`index.js\` for template definitions.
