# Ergonomic Chair Buying Consultant

> Turns any AI agent into an expert ergonomic chair buying consultant.

## What it does

Guides first-time and returning ergonomic chair buyers through a structured consultation to identify exactly which specs fit their body, work pattern, and setup — without relying on biased sales advice. Delivers a prioritised spec list (non-negotiable → recommended → optional) and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions grouped by topic (body measurements, daily hours, task type, posture concerns, desk height, floor type, climate, shared use, region)
2. Analyses answers using verified ergonomics standards: seat height targeting via ISO 9241-5 popliteal height rule, seat depth clearance (ANSI/HFES 100-2007), lumbar positioning (15–23cm above seat), armrest height standard, synchro-tilt vs basic tilt assessment, weight capacity and gas lift class, and caster type matching to floor surface
3. Proactively flags common first-time buyer mistakes where the user's answers suggest risk (e.g. seat depth too deep for short users, weight capacity not verified, gaming chair for office use, wrong caster type for floor, warm climate with foam-only build, tall user with inadequate backrest height)
4. Delivers a structured spec recommendation: non-negotiable → recommended → optional
5. Suggests up to 5 real products matching the user's confirmed specs, tailored to their region where possible

## Requirements

- No external APIs or environment variables required
- No runtime dependencies
- Works with any AI agent that supports SKILL.md (OpenClaw, ClawHub, etc.)
- Pure instruction-based — agent reasoning does the work

## Installation

Add via ClawHub or reference the SKILL.md directly in your agent configuration.

## License

MIT

## Homepage

https://github.com/arbazex/personal-tech-buying-consultants/tree/master/ergonomic-chair-buying-consultant
