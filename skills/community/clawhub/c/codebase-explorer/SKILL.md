---
name: codebase-explorer
description: "Analyze unfamiliar codebases and generate structured onboarding guides with architecture maps, entry points, conventions, and project-specific instructions. Use when joining new projects, understanding repo structure, or generating CLAUDE.md. Trigger phrases: onboard me, understand this codebase, analyze this repo, generate CLAUDE.md, walk me through. Adapted from everything-claude-code by @affaan-m (MIT)"
metadata: {"clawdbot":{"emoji":"🗺️","requires":{"bins":[],"env":[]},"os":["darwin","linux","win32"]}}
---

# Codebase Onboarding

Systematically analyze unfamiliar codebases and produce structured onboarding guides.

## When to Use

- First time opening a project
- Joining a new team or repository
- User asks "help me understand this codebase"
- User asks to generate a CLAUDE.md for a project
- User says "onboard me" or "walk me through this repo"

## Quick Start

1. Scan package manifests and config files (identify tech stack and framework)
2. Map directory structure and entry points (top 2 levels)
3. Trace one request lifecycle (entry → validation → business logic → database)
4. Identify naming, error handling, and testing patterns
5. Generate onboarding guide and starter CLAUDE.md

## Key Concepts

- **Reconnaissance** — Use file presence patterns to infer tech stack and structure
- **Architecture pattern** — Identify monolith vs. monorepo, frontend/backend split, API style
- **Convention detection** — Extract naming, error handling, async patterns from recent code
- **Guided exploration** — Don't read everything; use grep/glob selectively for ambiguity
- **Two-artifact output** — Onboarding guide (structure + conventions) + CLAUDE.md (project instructions)

## Common Usage

Most frequent patterns:
- Understanding project structure and data flow
- Documenting tech stack and architecture
- Creating starter instructions for new team members
- Identifying where to make changes (API routes, UI pages, database, tests)
- Mapping conventions (naming, error handling, git workflow)

## References

- `references/reconnaissance.md` — File patterns for framework/language detection
- `references/artifacts.md` — Onboarding guide and CLAUDE.md templates, best practices, anti-patterns
