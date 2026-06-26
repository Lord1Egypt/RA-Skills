# PLAN.md

Project: durable-task-runner

## Goal

Build a durable task orchestration system for OpenClaw that can:
- scale process/control level based on task complexity
- survive resets and resumes
- maintain durable state, event logs, and progress trails
- support pause / stop / steer
- support milestone-aware reporting with configurable verbosity
- integrate curated memory without bloating hot context
- orchestrate subagents as workers while the main agent acts as planner/controller

## Methodology

This project is intentionally **hybrid / agilefall**:
- **Agile-aligned** for iterative implementation, testing, and refinement
- **Structured/PMP-aligned** for milestones, scope, risk, deliverables, and visibility
- **ITIL-aligned** for operational control, resumability, change discipline, and restore/verify thinking

We reference principles only, not proprietary framework text.

## Milestones

1. **Foundation scaffold**
   - skill
   - task schema
   - task control helper

2. **Interruption + reconcile primitives**
   - interruption queue
   - pending actions / action states / idempotency ledger
   - reconcile helper

3. **Self-bootstrap / dogfood lane**
   - config defaults
   - explicit operational project files
   - live durable task record for this project

4. **Planning + backlog model**
   - backlog file format
   - task level model (0..N)
   - artifact selection by level

5. **Progress + reporting control**
   - reporting levels
   - heartbeat/status helper
   - milestone-only default with configurable overrides

6. **Memory integration**
   - reference-file memory model
   - MEMORY.md reference rule
   - configurable memory thresholds

7. **Subagent orchestration layer**
   - dispatch helpers
   - structured worker return parsing
   - anti-drop controller checks

8. **Resume / restart bootstrap**
   - inspect running tasks on startup
   - consistency check + resume path

9. **Prototype validation**
   - dogfood on a real task
   - verify increasing durability across milestones

## Execution model

- Commit at meaningful checkpoints.
- Each milestone should make the next step less dependent on agent memory and more dependent on system state.
- Prefer sane defaults with configuration over hardcoded rigidity.
