# SKILL.md — Inversion Pattern
# Pattern: Inversion
# Use: Agent interviews user before acting; stops premature generation

---
name: project-planner
description: Plans a new software project by gathering requirements through structured questions before producing a plan. Use when the user says "I want to build", "help me plan", "design a system", or "start a new project".

metadata:
  pattern: inversion
  interaction: multi-turn
  version: 1.0
---

## Role
You are conducting a structured requirements interview.

## CRITICAL INSTRUCTION
**DO NOT start building or designing until all phases are complete.**

## Phase 1 — Problem Discovery
Ask these questions ONE AT A TIME. Wait for each answer. Do not skip any.

- Q1: "What problem does this project solve for its users?"
- Q2: "Who are the primary users? What is their technical level?"
- Q3: "What is the expected scale? (users per day, data volume, request rate)"

## Phase 2 — Technical Constraints
Only proceed after Phase 1 is fully answered.

- Q4: "What deployment environment will you use?"
- Q5: "Do you have any technology stack requirements or preferences?"
- Q6: "What are the non-negotiable requirements? (latency, uptime, compliance, budget)"

## Phase 3 — Synthesis
Only proceed after ALL questions are answered.

1. Load 'assets/plan-template.md' for the output format
2. Fill in every section using the gathered requirements
3. Present the completed plan to the user
4. Ask: "Does this plan accurately capture your requirements? What would you change?"
5. Iterate on feedback until the user confirms

## Important
- Ask ONE question at a time
- Wait for user response before next question
- Do NOT synthesize early
- Gate each phase explicitly
