---
name: game-dev-start
description: >
  Project onboarding for game development. Detects project state, asks guided
  questions to determine user context, and routes to the correct workflow.
triggers:
  - "/start"
  - "I want to start making a game"
  - "What should I work on first?"
  - "onboard me"
  - "init game project"
---

# Game Dev Start — Project Onboarding

## 🎯 Purpose

Get a developer from zero to a running game project in the right engine with
the right scope, without assuming anything about their experience level or
platform.

## 🤖 Multi-Platform Notes

| Platform       | Notes |
|----------------|-------|
| **OpenClaw**   | Relies on workspace files (`*.md`, `*.json`, `*.gd`, `*.cs`). Creates persistent artifacts in the workspace. Can read/write engine project files natively. |
| **Claude Code** | Terminal-focused. Reads project files, runs engine CLI commands, edits source. Best for hands-on coding in the engine project directory. |
| **Cursor/Windsurf** | Similar to Claude Code: IDE-integrated. May have LSP/IntelliSense available for Godot/GDScript or Unity/C#. |
| **GitHub Copilot** | Inline completions and chat. Best for micro-tasks once project structure exists. Less suited for full onboarding flow. |
| **Generic LLM Chat** | Provide partial outputs and ask the user to copy-paste. Works best with template-based onboarding. |
| **Any AI**      | All can handle the question-asking and routing phase. File operations vary. |

### Platform Adaptation

- **If the AI can read/write files:** Show context questions → ask → create files.
- **If the AI cannot write files (chat-only):** Output the complete file content in
  a code block and tell the user to save it themselves.
- **If the AI can run CLI commands:** Try to detect project state automatically
  (e.g. `ls *.csproj` for Unity, `ls project.godot` for Godot).

## 🔍 Detect Project State

Look for these files in the current/project directory:

| Engine | Detection File |
|--------|---------------|
| Godot 4.x | `project.godot` |
| Unity 6/7 | `*.csproj` (root), `Assets/` directory |
| Unreal 5.x | `*.uproject` |
| Custom | Custom project file, `package.json`, `CMakeLists.txt` |

## ❓ Phase 1: Onboarding Questions

Ask these questions **one at a time** unless the user provides a rich answer upfront.

### Question 1: Context

> **"Where are you starting from?"**
>
> ```
> 1) No idea — I just want to make a game but don't know where to start
> 2) Vague idea — I have a concept but no project set up
> 3) Clear vision — I know what I want to build and need help setting up
> 4) Existing project — I have a project already started
> ```

### Question 2: Experience (if 1-3)

> **"What's your experience level?"**
>
> ```
> 1) First time — never made a game
> 2) Beginner — made a few small things
> 3) Intermediate — shipped something or worked on a team
> 4) Advanced — experienced but using a new engine
> ```

### Question 3: Engine preference (if applicable)

> **"Any engine preference?"**
>
> ```
> 1) Godot 4.x (great for 2D, FOSS, lightweight)
> 2) Unity 6/7 (great for 2D/3D, C#, huge ecosystem)
> 3) Unreal 5.x (AAA 3D, Blueprints/C++, steep learning)
> 4) Custom/other (SDL, Bevy, Phaser, etc.)
> 5) Not sure — recommend for me
> ```

### Question 4: Scope (if clear vision)

> **"What's the scope?"**
>
> ```
> 1) Micro — 1-2 week prototype, jam game
> 2) Small — month-long vertical slice
> 3) Medium — 3-6 month polished project
> 4) Large — 6+ month commercial release
> ```

## 🗺️ Phase 2: Routing

Based on answers, route to the correct workflow:

| User Answer | Route To |
|-------------|----------|
| No idea, first time | → `brainstorm` skill: Creative Discovery phase |
| Vague idea, first time | → `brainstorm` skill: Concept Generation → Core Loop Design |
| Clear vision, no project | → `brainstorm` → `game-design-doc` → `setup-engine` |
| Existing project | → Detect engine → check for GDD → `sprint-dev` or `architecture` |
| Experienced, clear vision | → `architecture` → `setup-engine` (skip brainstorm unless needed) |

## 🏗️ Phase 3: Onboarding Output

After routing, create a **project context file**:

```
game-dev-studio/
├── context.md          ← this onboarding output
└── skills/             ← skill folders
```

**context.md template:**

```markdown
# Game Project Context

## Identity
- **Project:** [project name or "TBD"]
- **Engine:** [Godot / Unity / Unreal / Custom]
- **Genre:** [genre]
- **Platform targets:** [PC / Mobile / Console / Web]

## Team
- **Developer count:** [1 / 2 / small team]
- **Experience:** [beginner / intermediate / advanced]

## Status
- **Phase:** [onboarding / concept / prototype / GDD / dev / release]
- **Engine setup:** [not started / configured / running]
- **Next step:** [link to skill or task]

## Scope
- **Estimated duration:** [2 weeks / 1 month / 3 months / 6+ months]
- **Team size:** [solo / small / large]
```

## 🔗 Next Steps

After onboarding, chain to the appropriate skill:

- `brainstorm` — if concept needs development
- `setup-engine` — if engine is chosen but not configured
- `game-design-doc` — if concept is clear and needs documentation
- `architecture` — if tech design is needed
- `prototype` — if validating a risky mechanic quickly
- `sprint-dev` — if entering active development
