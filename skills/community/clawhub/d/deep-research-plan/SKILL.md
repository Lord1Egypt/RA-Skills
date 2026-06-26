---
name: deep-research
description: "Automated deep research that performs comprehensive multi-source investigation and produces detailed reports with citations. Use when user requests research, investigation, or in-depth analysis of any topic. Capabilities: generate structured research plans, and start sub agent to execute the plan. "
---

# Deep Research

Two-phase research workflow: planning then execution.

## Overview

This skill provides a structured approach to deep research:

**Phase 1: Planning** (High Freedom)

- Discuss with user to clarify and refine research questions.
- Define what to investigate and what the report should cover.
- Set expectations for research depth and output.
- Create research plan document.

**Phase 2: Execution** (Low Freedom)

- Sub-agent reads the research plan
- Independently decides how to search for each sub-question
- Can dynamically add searches based on findings
- Analyzes content and generates report with citations

## Phase 1: Generate Research Plan

The coordinator (main session) performs:

1. **Understand the research topic** — Listen to user's request and understand what they want to investigate
2. **Collaborate with user** — Discuss and clarify research questions together. Present 3-5 potential sub-questions or research angles for user to review
3. **Define scope together** — Discuss what to include/exclude, confirm boundaries of the research
4. **Confirm report expectations** — Ask user what sections they want, what depth, any specific focus areas
5. **Get user confirmation** — Present the draft plan to user and wait for approval before proceeding
6. **Output: Research plan document** — Only after user confirms, save to `plans/research-plan-{timestamp}.json`

**Key principle:** The plan is a collaboration between coordinator and user. Never proceed to Phase 2 without explicit user confirmation of the research plan.

## Research plan format (JSON):

```json
{
  "topic": "Original research topic",
  "research_questions": [
    "What are the latest breakthroughs in this field?",
    "Who are the leading organizations or researchers?",
    "What are the current limitations or challenges?",
    "What are the practical applications?"
  ],
  "scope": {
    "include": ["recent developments", "key players", "technical details"],
    "exclude": ["historical background before 2020", "unrelated applications"]
  },
  "report_requirements": {
    "sections": ["executive_summary", "findings", "conclusion", "references"],
    "depth": "comprehensive",
    "min_sources": 8,
    "focus_areas": ["technical analysis", "market landscape"]
  }
}
```

## Research Plan Schema

Required fields:

- topic: Original research topic
- research_questions: Array of questions to investigate
- report_requirements: Object specifying output expectations

Optional fields:

- scope: Define boundaries of research (include/exclude)
- min_sources: Minimum sources to analyze (default: 8)
- max_sources: Maximum sources to analyze (default: 20)
- notes: Additional context or special instructions

Save plan to: `plans/research-plan-{timestamp}.json`

**⚠️ WAIT FOR USER CONFIRMATION — Do not proceed to Phase 2 until user explicitly approves the research plan.**

Key principle: The plan defines WHAT to research and WHAT the output should contain. It does NOT specify HOW to search (keywords, sources, rounds) - that is up to the research agent to determine dynamically.

## Phase 2: Execute Research Plan

Launch sub agent with the research plan. Launch sub agent with `session_spawn` tool. Instruct subagent to use `deep-research-executor` to execute the plan EXPLICITLY.
