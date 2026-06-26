# Mission Control — AI Agent Task Tracking System

A task tracking and plan confirmation system for AI agents. Implements a **5-stage workflow with 3-iteration Qiushi (求是) analysis** for every task before execution.

## Core Philosophy

- **Plan-First**: All code/file/agent tasks require Boss confirmation before execution
- **Qiushi Iteration**: Every plan goes through 3求是→analysis→revision cycles
- **Single-Agent Execution**: Handled entirely by the main agent (Moss), no sub-agents

## Workflow

```
Stage 1: Task Reception & Triage
Stage 2: Task Definition + Plan Generation (3 iterations)
Stage 3: Boss Confirmation
Stage 4: Execution (with live logging)
Stage 5: Report & Delivery
```

### Auto-Triage Criteria

Automatically determine if a task needs mission-control:
- File operations (.py/.sh/.js/.md/.yaml/.json)? → Yes
- Code/script generation or modification? → Yes
- SubAgent delegation? → Yes
- Web research? → Yes
- Terminal/CLI operations? → Yes
- Pure Q&A (<1min)? → No

## File Structure

```
mission-control/
├── SKILL.md                          # Main skill documentation
├── templates/
│   └── project-intake.md             # Project intake template (Boss fills)
├── references/
│   ├── 2026-05-19-static-spec-conversion.md  # Conversion case study
│   └── project-intake-case-studies.md        # Template usage examples
└── scripts/
    ├── generate_report.py
    ├── next_number.py
    ├── save_plan.py
    └── update_progress.py
```

## Key Concepts

### Task ID Format
`T-YYYYMMDD-NNN` — e.g. `T-20260519-001`

### Task Lifecycle Files
- `t-requirement.md` — Task requirements
- `t-plan.md` — Plan with 3-iteration Qiushi analysis
- `t-log.md` — Execution log (step-by-step status)
- `t-report.md` — Completion report

### Project Intake
When Boss fills `project-intake.md` before task start, Moss reads it and skips straight to plan generation — no repeated confirmation needed.

## Qiushi Integration

| Stage | Skill Used |
|-------|-----------|
| Plan generation (Stage 2) | qiushi — 3 iterations required |
| Report (Stage 5) | qiushi — criticism & self-review |
| Other stages | mission-control itself |

## Prohibited Behaviors

- ❌ Skip mission-control without objective triage
- ❌ Start execution without Boss confirmation
- ❌ Skip the 3-iteration Qiushi analysis
- ❌ Execute without logging to t-log.md
- ❌ End task without t-report.md

## Citation

Designed and published by Huang Kai (huangjk8023@yeah.net).

Built for the Hermes Agent system. Part of the open-source AI agent workflow toolkit.
