# Deployment Checklist

## 1. Pre-Deploy

- Confirm `SKILL.md` frontmatter has valid `name` and English `description`
- Confirm `agents/openai.yaml` reflects current display name, version, and Buddy merge rules
- Confirm `assets/release.json` matches the shipping version
- Confirm Buddy merge docs are present:
  - `references/game-design.md`
  - `references/runtime-architecture.md`
  - `references/buddy-system.md`
- Configure backend endpoints and secrets
- Enable timezone-aware scheduler
- Run local script sanity checks
- Install skill into OpenClaw skills directory:
  - `bash skills/claw-go/scripts/install_skill_local.sh ~/.openclaw/skills`

## 2. Required Environment Variables

- `CLAWGO_API_BASE`
- `CLAWGO_API_KEY`
- `CLAWGO_DEFAULT_TZ`
- `CLAWGO_FREE_DAILY_LIMIT`
- `CLAWGO_PRO_DAILY_LIMIT`

Use template in [assets/config-template.env](../assets/config-template.env).

## 3. Smoke Tests

1. `虾游记` starts the game and auto-hatches a companion if none exists
2. `buddy` or `虾游记 孵化搭子` shows the deterministic companion card
3. `buddy status` or `虾游记 搭子状态` shows rarity, species, eye, hat, shiny, and all five Buddy stats
4. `buddy pet` or `虾游记 摸摸搭子` returns hearts and updates pet state without exploitable progression
5. Free user gets `1` proactive update/day
6. Pro user gets up to `3` proactive updates/day
7. Free user requesting premium feature receives fallback response
8. `虾游记 状态` returns current stats and release line
9. `虾游记 去旅行` respects quota and returns deterministic payload shape
10. QQ selfie path still works with and without optional companion JSON
11. Entitlement API outage triggers free fallback without crash
12. `openclaw --dev skills list --json` shows `claw-go`

## 4. Launch Gates

- error rate under `1%` for command handler
- scheduler duplicate send rate under `0.1%`
- premium gate false-positive deny under `0.5%`
- telemetry events present for send, hatch, pet, upgrade, and fallback

## 5. Post-Deploy

- monitor D1 and D7 retention by tier
- monitor conversion from quota-hit moments
- monitor usage split between travel updates and Buddy-only interactions
- tune destination weights weekly from user interactions
- review companion hatch distributions to confirm rarity weights still look sane
