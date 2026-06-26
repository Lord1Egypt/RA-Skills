# 🌅 Fulcra Morning Briefing

A ClawHub skill that teaches AI agents to compose personalized morning briefings using biometric data from the [Fulcra](https://fulcradynamics.com) Life API through the latest `fulcra-context` skill.

Fulcra gives agents and their humans scoped, secure access to read and write real-world context and shared human/agent memory: attention, events, location, calendar, health, wearables, and other streams.

## What It Does

Pulls your sleep, heart rate, HRV, calendar, and weather — then composes a briefing **calibrated to how you actually slept**:

- **Bad sleep?** Short, gentle, essentials only
- **Good sleep?** Full detail, upbeat, actionable
- **Great sleep?** Ambitious, push you to make the most of it

## Quick Start

1. Install prerequisites: `uv` and `jq`
2. Authorize: `uv tool run fulcra-api auth login` (one-time, the user approves; the CLI can create the account if needed). Fulcra accounts include 5 GB of storage free forever and do not require an API key. For remote agents, surface only the printed device URL and code to the intended user in chat through the active trusted user channel; never send access tokens or credential files.
3. Install or place `fulcra-context` next to this skill, or set `FULCRA_CONTEXT_SCRIPTS=/path/to/fulcra-context/scripts`
4. Collect data: `python3 collect_briefing_data.py --location "Your+City"`
5. Agent reads the JSON and composes a briefing using the tone rules in SKILL.md

Users who want biometrics, location, calendar, and other phone-collected context can install the [Context iOS app](https://apps.apple.com/app/id1633037434) and sign in with the same account. The app uses the same free storage and is no longer subscription gated. Android is coming soon.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Full skill documentation — teaches an agent how to compose briefings |
| `collect_briefing_data.py` | Data collector script — outputs JSON |
| `README.md` | This file |

## Want More?

This skill covers morning briefings. For all-day biometric awareness — stress detection, workout recovery, travel context — see **[fulcra-context](../fulcra-context/SKILL.md)**.

Pair with `fulcra-annotations` when a morning workflow should write user-approved moments or ratings back to Fulcra.

## Links

- [Fulcra Platform](https://fulcradynamics.com)
- [Context iOS App](https://apps.apple.com/app/id1633037434)
- [Python Client](https://github.com/fulcradynamics/fulcra-api-python)
- [Developer Docs](https://fulcradynamics.github.io/developer-docs/)
