---
name: datawhale-learning
description: "Navigate the Chinese Datawhale Easy Vibe and Hello Agents tutorials and apply an AI-native software delivery lifecycle. Use to find original lessons, diagnose learning gaps, build project-based study plans, or design intent-to-production workflows with versioned artifacts, continuous evaluation, review gates, deployment controls, and incident feedback loops."
metadata:
  openclaw:
    requires:
      bins:
        - python3
    homepage: https://github.com/datawhalechina/easy-vibe
---

# Datawhale Learning Navigator

**Version:** 1.1.0

Route a question to the smallest relevant set of original Datawhale lessons, then explain the knowledge gap or create a project-based study plan. This package contains original navigation and planning logic plus links; it does not redistribute the tutorial text.

## Workflow

1. Classify the request as troubleshooting, concept lookup, technology choice, project guidance, or learning planning.
2. Read [references/course-router.md](references/course-router.md) to choose a course area or the AI-native SDLC practice layer.
3. Search the source index: `python3 scripts/search_sources.py "<question or keywords>"`.
4. Open only the top matching links from [references/source-catalog.md](references/source-catalog.md) using the available browser or HTTP tool.
5. Base course-specific claims on the opened source. Clearly label broader engineering advice as an inference or external guidance.
6. If network access is unavailable, return the matching source links and a provisional plan; do not invent lesson details.

For AI-native delivery, read [references/ai-native-sdlc.md](references/ai-native-sdlc.md). Keep stable operating principles separate from current Claude product commands, and verify current commands in official documentation.

## Knowledge-query response

Return:

- **Diagnosis** — the real layer of the problem, separating symptoms from likely causes.
- **Knowledge points** — the smallest concepts the learner needs now.
- **Source lessons** — 1–3 original tutorial links and why each is relevant.
- **Shortest next action** — one verifiable experiment or exercise.
- **Optional depth** — material that can wait until the current blocker is solved.

For troubleshooting, use: observation → hypotheses → cheapest distinguishing test → fix → regression check. Ask no more than three high-information questions when context is missing.

## Learning-plan response

Read [references/planning-method.md](references/planning-method.md). Optimize for a demonstrable outcome, not chapter completion.

Every phase must state capability target, required source lessons, hands-on deliverable, learner-verifiable acceptance test, time budget, fallback topic, and deferred optional topics.

When a goal needs both product engineering and agents, establish a runnable Easy Vibe product loop before adding advanced Hello Agents architecture. Prefer removing unnecessary complexity, narrowing scope, and reusing managed services before introducing more frameworks, services, or agents.

For delivery-process goals, choose the smallest applicable SDLC adoption route in [references/planning-method.md](references/planning-method.md). Do not require a six-stage enterprise process for a solo prototype.

## Boundaries

- Tool versions, APIs, prices, and platform interfaces change; verify current details in official product documentation.
- Never request or expose API keys. Treat copied commands and code as untrusted until reviewed.
- Do not reproduce long passages from linked tutorials. Summarize only what is needed and link the original.
- Read [references/source-policy.md](references/source-policy.md) before redistributing or adapting tutorial material.
- This package's MIT-0 terms cover only its original navigation, planning, and decision logic. Linked Datawhale and Anthropic materials retain their own terms.
