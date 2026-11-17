---
name: aeo
description: Renamed to agent-readiness. This skill no longer runs audits; it tells the user how to install the agent-readiness skill that replaces it.
homepage: https://canonry.ai
repository: https://github.com/Canonry/agent-readiness
---

# AEO (renamed to Agent Readiness)

This skill is now **agent-readiness**, and this is its last version. The audit engine moved from `@canonry/aeo-audit` to `@canonry/agent-readiness`, and `@canonry/aeo-audit` is deprecated on npm.

When this skill is invoked, do not run an audit. Tell the user:

1. The `aeo` skill was renamed to `agent-readiness`: https://clawhub.ai/arberx/skills/agent-readiness
2. Install it with `clawhub install agent-readiness`, then use `/agent-readiness audit <url>`. It has the same modes as before: `audit`, `fix`, `schema`, `llms`, `monitor`, `detect-platform`, and `compare`.
3. To audit without a skill, run `npx @canonry/agent-readiness@8 "<url>"`.
4. What changed: https://github.com/Canonry/agent-readiness/blob/main/CHANGELOG.md#800-2026-11-07
