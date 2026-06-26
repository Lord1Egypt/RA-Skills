# agent-reflect — OpenClaw Skill

> 原文链接: https://clawskills.sh/skills/stevengonsalvez-agent-reflect

---
## Setup & Installation

clawhub install stevengonsalvez/agent-reflect

If the CLI is not installed:

npx clawhub@latest install stevengonsalvez/agent-reflect

Or install with OpenClaw CLI:

openclaw skills install stevengonsalvez/agent-reflect

[View on GitHub](https://github.com/openclaw/skills/tree/main/skills/stevengonsalvez/agent-reflect)[View on ClawHub](https://clawhub.ai/stevengonsalvez/agent-reflect)

or paste the repo link into your assistant's chat

https://github.com/openclaw/skills/tree/main/skills/stevengonsalvez/agent-reflect

## What This Skill Does

Analyzes a conversation for correction signals and successful patterns, then proposes targeted edits to agent definition files and CLAUDE.md. Each accepted change is encoded permanently so the same correction doesn't need to happen twice.

Rather than re-stating preferences every session, corrections are written directly into agent files as diffs, making improvements persistent and auditable.

### When to use it

-   Encoding a TypeScript style correction into the frontend agent after a session
-   Capturing a preferred commit workflow discovered during a project
-   Selectively applying only certain changes from a batch of session learnings
-   Auto-reflecting at session boundaries before context compaction
-   Promoting a non-obvious debugging workaround into a reusable skill file

View original SKILL.md file

## Example Workflow

Here's how your AI assistant might use this skill in practice.

INPUT

User asks: reflect

AGENT

1.  1Scans the conversation for correction signals, categorized by confidence (HIGH: 'never', 'always', 'wrong'; MEDIUM: 'perfect', 'exactly')
2.  2Maps each signal to a target file such as a named agent definition, CLAUDE.md, or a new skill file
3.  3Checks whether any learning meets skill-worthy criteria: non-obvious, reusable, verified, and not already documented
4.  4Presents a structured diff proposal with confidence levels and source quotes for each proposed change
5.  5Applies approved changes to target files and updates metrics in ~/.reflect/

OUTPUT

Agent definition files updated with new rules; reflection log saved to .claude/reflections/YYYY-MM-DD\_HH-MM-SS.md; metrics incremented in ~/.reflect/reflect-metrics.yaml