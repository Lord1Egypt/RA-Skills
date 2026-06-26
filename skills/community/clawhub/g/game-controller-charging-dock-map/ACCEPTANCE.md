# Acceptance Checklist

- [x] SKILL.md has valid YAML frontmatter.
- [x] skill.json is present and valid JSON.
- [x] Version is 1.0.0 and license is MIT-0.
- [x] Language is English only.
- [x] Prompt-only metadata is present: promptOnly true, hasExecutableCode false, requires_api false, no_code_execution true, execution noExec.
- [x] No executable code, scripts, package files, automation hooks, API requirements, credential needs, or network requirements.
- [x] Directory contains exactly SKILL.md, skill.json, and ACCEPTANCE.md.
- [x] Boundary keeps the skill to cable tidiness and shared setup organization and avoids electrical repair advice, charging modification, battery diagnosis, device repair, and hardware alteration.
- [x] Deliverable is a dock layout card with controller slots, cable labels, return rules, charge routine, accessory zones, and reset checklist.
- [x] Workflow covers counting devices, mapping dock slots, assigning cables, routing for tidiness, setting a charge routine, and creating a printable card.
- [x] Slug matches the accepted design: game-controller-charging-dock-map.

## Clean Scan Evidence

Verify the skill directory contains exactly these files with no unexpected artifacts:

| File | Expected | Check |
|---|---|---|
| SKILL.md | Present, valid YAML frontmatter, English-only | [x] |
| skill.json | Present, valid JSON, version 1.0.1, license MIT-0 | [x] |
| ACCEPTANCE.md | Present, English-only | [x] |
| Extra files | None — no scripts, logs, screenshots, build outputs, temp files, or hidden artifacts | [x] |
| Secrets scan | No API keys, tokens, passwords, credentials, or PII | [x] |
| Executable scan | No executable code, package files, automation hooks, or network handlers | [x] |

## Install-First Success Path

1. **Input:** User says "We have four controllers across two consoles and they're never charged when we want to play. Help me set up a charging dock map with labels so everyone knows where things go."
2. **Steps:** The skill guides the assistant to: (a) list each controller by console/color/player, (b) assign dock slots and cable labels to each, (c) route cables for tidiness and safety, (d) define return rules for after-play and guests, (e) create a charge routine with check-before-play and reset-after-guests cues, (f) add accessory zones if relevant, (g) produce a printable dock layout card.
3. **Output:** A game controller charging dock map with a dock layout table, controller-to-slot assignments, cable labels, cable tidiness plan, charge routine, accessory zone, and mini printable card — all focused on organization and cable tidiness without electrical repair advice.

Expected first-run outcome: The user receives a visible dock map they can print and post near the gaming area, making it obvious where each controller and cable belongs and what the after-play reset routine is.
