# Company Roster — FounderClaw

## Agents

| ID | Name | Emoji | Role | Model Tier | Workspace |
|---|---|---|---|---|---|
| founderclaw-main | FounderClaw Main | 🎯 | CEO / Orchestrator | Best | founderclaw/ceo/ |
| strategy | Strategy | 📐 | Product thinking, design | Best | founderclaw/strategy-dept/ |
| shipper | Shipper | 🚀 | Code review, deploy | Fast | founderclaw/shipping-dept/ |
| tester | Tester | 🔍 | QA, browser testing | Vision | founderclaw/testing-dept/ |
| safety | Safety | 🛡️ | Security, guardrails | Fast | founderclaw/security-dept/ |
| observer | Observer | 📊 | Debug, retro, second opinion | Best | founderclaw/history-dept/ |

## Model Tiers

| Tier | Model | Use |
|---|---|---|
| Fast | (user configures) | Shipper, Safety — quick tasks |
| Best | (user configures) | CEO, Strategy, Observer — deep thinking |
| Vision | openrouter/xiaomi/mimo-v2-omni | Tester, spawned sub-agents |

## Skills per Department

| Department | founderclaw Skills | OpenClaw Built-in |
|---|---|---|
| CEO | all 29 + install-founderclaw | clawhub, skill-creator |
| Strategy | office-hours, plan-ceo-review, plan-eng-review, plan-design-review, design-consultation, design-review, design-shotgun, autoplan | — |
| Shipper | review, ship, land-and-deploy, canary, benchmark, document-release | github, gh-issues |
| Tester | qa, qa-only, browse, setup-browser-cookies, connect-chrome | video-frames |
| Safety | cso, careful, freeze, guard, unfreeze | healthcheck |
| Observer | investigate, retro, codex | summarize, session-logs |

## Tool Policy

See docs/founderclaw-design.md for full tool policy matrix.
