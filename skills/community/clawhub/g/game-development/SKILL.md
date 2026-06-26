---
name: Game Development
slug: game-development
version: 1.0.0
homepage: https://clawic.com/skills/game-development
description: Design and ship browser-playable games from no-build Three.js prototypes to advanced architectures with workflows, budgets, and playtest loops.
changelog: Initial release with browser-first workflows, architecture patterns, project templates, and advanced game system playbooks.
metadata: {"clawdbot":{"emoji":"🕹️","requires":{"bins":["node","python3"],"env":[]},"os":["darwin","linux","win32"]}}
---

## Setup

On first use, read `setup.md` silently and align game scope, delivery target, and technical constraints before proposing implementation.

## When to Use

Use this skill when users want to create playable games with agents, especially instant browser games with Three.js that run without a compile step. It also supports advanced projects with multiple systems, larger content pipelines, multiplayer plans, and live operations.

## Architecture

Memory lives in `~/game-development/`. See `memory-template.md` for setup and status fields.

```
~/game-development/
|-- memory.md                     # Current project state, scope, and delivery profile
|-- concept-briefs.md             # Game concepts, target audience, and pillar ideas
|-- user-preferences.md           # User taste, constraints, and style preferences
|-- system-decisions.md           # Technical decisions and tradeoffs
|-- playtest-log.md               # Session findings, issues, and balancing actions
|-- roadmap.md                    # Milestones and release checkpoints
`-- release-notes.md              # What changed between iterations
```

## Quick Reference

Use the smallest relevant file for the current task.

| Topic | File |
|-------|------|
| Setup flow | `setup.md` |
| Memory template | `memory-template.md` |
| Genre and loop selection | `game-types-and-loops.md` |
| No-build browser path with Three.js | `browser-threejs-fast-path.md` |
| Project folder blueprints | `project-structure-blueprints.md` |
| Systems architecture and state design | `systems-and-state.md` |
| Asset/content pipeline and tooling | `content-pipeline.md` |
| Multiplayer and live operations | `multiplayer-and-live-ops.md` |
| QA, balancing, and launch checklist | `qa-balance-launch.md` |

## Requirements

- Runtime for local preview scripts: `node`
- Optional tools for offline asset processing: `python3`
- Browser target for quick iterations: Chrome, Edge, Safari, or Firefox

Prefer local and static workflows first. Move to backend dependencies only when the user explicitly needs multiplayer authority, persistence, or commerce.

## Data Storage

Local notes stay under `~/game-development/` and should capture:
- the current game concept and loop assumptions
- the user preferences and non-negotiable constraints
- technical architecture choices with reasons
- playtest findings, balancing deltas, and release decisions

Keep notes concise and operational. Store decisions and outcomes, not long transcripts.

## Core Rules

### 1. Lock the Delivery Profile First
Choose one profile before coding:
- Browser Instant: no-build HTML/CSS/JS delivery, fastest iteration, easiest sharing
- Browser Structured: TypeScript or bundler workflow with modular architecture
- Engine Path: Unity, Unreal, or Godot when editor tooling and content scale justify it

Do not mix profiles in one milestone unless the user asks for migration.

### 2. Start From a Vertical Slice, Not a Full Game Plan
Always build a playable loop in this order:
- input
- movement
- objective
- fail state
- restart

A complete five-minute loop is more valuable than ten untested systems.

### 3. Treat Browser Performance as a Product Requirement
For browser-first games, define budgets before adding content:
- frame target and frame-time budget
- draw calls and shader complexity budget
- texture and audio memory budget
- mobile fallback quality tier

If a feature breaks the budget, simplify first and optimize second.

### 4. Separate Deterministic Core Logic From Presentation
Keep rules deterministic and testable:
- game state transitions
- hit and scoring logic
- progression and economy math

Render, VFX, and animation should observe state, not own truth.

### 5. Use Progressive Complexity
System order for agent-driven delivery:
- loop and controls
- feedback and readability
- enemy or puzzle variation
- progression layer
- social or online features

Only unlock the next layer after the previous one is playable and measured.

### 6. Make Playtesting Continuous
Each milestone must include:
- test objective
- expected player behavior
- observed friction
- one concrete balancing action

No new feature batch should be accepted without a playtest note.

### 7. Preserve Reusable Project Knowledge
Update local memory after major decisions:
- concept changes
- preference updates
- architecture pivots
- launch risks

This allows agents to continue work without repeating discovery.

## Common Traps

- Building menus, inventory, and cosmetics before core loop validation -> large scope with no fun proof
- Tying physics and gameplay directly to frame rate -> inconsistent behavior across devices
- Importing heavy 3D assets too early for browser targets -> unusable mobile experience
- Skipping input latency and camera readability checks -> players quit despite stable FPS
- Adding multiplayer before single-player loop quality -> expensive complexity without retention value
- Ignoring save and state recovery strategy -> broken sessions and user frustration

## Security & Privacy

Data that stays local:
- concept notes and user preferences under `~/game-development/`
- project decision logs and playtest outcomes

Data that may leave your machine only if explicitly requested:
- source code pushed to remote repositories
- asset uploads to CDN or build hosts
- backend telemetry or analytics events

This skill does NOT:
- force external services for simple browser prototypes
- require paid APIs for baseline game creation
- recommend production launch without performance and playtest evidence

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `threejs` - 3D rendering patterns and WebGL resource hygiene
- `javascript` - core scripting patterns for browser game logic
- `typescript` - safer large-scale game codebases and tooling
- `unity` - engine path for editor-heavy and cross-platform pipelines
- `unreal-engine` - high-fidelity pipeline when advanced rendering is required

## Feedback

- If useful: `clawhub star game-development`
- Stay updated: `clawhub sync`
