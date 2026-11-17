---
name: autoselect-skill
description: Auto-select which skills to load for the current user turn. Triggered when a user message implies a domain (UI/UX, code review, deep research, plan-mode, debugging, doc work, sales/outreach, etc.) but the appropriate skill(s) have not yet been loaded. Outputs ranked skill recommendations with one-line reasons and an opt-in `/autoselect` slash trigger.
version: 0.1.0
triggers:
  - keyword_match: detect domain terms in the incoming user message
  - slash_command: "/autoselect" (force-run regardless of message)
  - heuristic: more than one available skill matches the message intent
---

# autoselect-skill

## Purpose

When a user message arrives, this skill scans the set of available skills and recommends which ones to load for the current turn. It does NOT replace loading those skills — the agent then calls `skill` for each recommended name.

## When to invoke

**Auto-trigger (heuristic)** — fire this skill when the user message:

- Names a domain with high specificity (e.g. "review my UI/UX", "research market trends", "debug this stack trace", "sell into X company")
- Implies a workflow class (planning, design, deep research, code change, doc generation, image/visual)
- Mentions a tool name that overlaps a skill (e.g. "Mermaid", "Vite", "Feishu")

**Manual trigger** — user types `/autoselect`. Always run.

**Skip** — if the message is pure small-talk, single-question, or already targets one skill explicitly (`/plan-mode`, `/skill foo`).

## Workflow for the invoking agent

1. Collect the **list of available skills**. The runtime injects this at session start
   as `<available_skills>` with each `name` and `description`. If not injected, call
   `mavis({ command: "agent list" })` and inspect prompt frontmatter.

2. **Score each skill 0–3** against the user message:

   | Score | Signal |
   |------:|--------|
   |   3   | Skill name appears in the message (verbatim or stemmed) |
   |   2   | Skill description keyword overlap ≥ 2 of the message's content words |
   |   1   | Adjacent domain — could plausibly help but not primary |
   |   0   | No overlap — exclude |

3. **Cap at top 3** skills with score ≥ 1. Drop the rest.

4. **Output format** (always emit this block when called):

   ```
   <autoselect>
   recommended_skills:
     - name: <skill-name>
       score: <0-3>
       reason: <one sentence tying skill description to the user message>
     - name: <skill-name-2>
       score: <0-3>
       reason: <one sentence>
   ignored_skills:
     - name: <skill-name>
       reason: <why skipped, e.g. "score 0, no overlap">
   next_action: load <skill-name>[, <skill-name-2>...] OR proceed without loading if all scores are 0
   </autoselect>
   ```

5. After emitting the block, the agent may then call `skill` for each top recommendation
   to actually load its body into context.

## Worked example

User: "Can you review this UI mockup and propose a better color palette?"

```
<autoselect>
recommended_skills:
  - name: ui-ux-pro-max
    score: 3
    reason: "UI + palette + design review explicitly named in the message"
  - name: visual-content-generator
    score: 1
    reason: "Adjacent — could generate alternative mockups, but not strictly asked"
ignored_skills:
  - name: deep-research-agent
    reason: "score 0, no research ask"
next_action: load ui-ux-pro-max
</autoselect>
```

## Universal — works for any LLM

This skill does NOT depend on Mavis-specific runtime features beyond the `<available_skills>`
injection. Any LLM with:
- A way to list its skills
- A way to load a skill (file / system prompt / tool call)

can run this workflow by following the steps above.

## Cross-project use

- Treat the output as advisory. The invoking LLM retains final judgment — if its own
  reading of the message diverges from the heuristic, trust the reading.
- Prefer precision over recall: an empty `<autoselect>` block (no recommendations) is a
  valid answer. Over-triggering adds noise.
- Update the trigger list above if new domain-bridging skills are added to the roster.

## Install

Drop `SKILL.md` into your agent's skills directory. For Mavis-format agents, that is
`$AGENT_HOME/.skills/autoselect-skill/SKILL.md`. Restart the agent so the new skill is
picked up by the skill loader.

## License

MIT — same as the parent project.
