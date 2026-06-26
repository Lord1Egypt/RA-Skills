---
name: "dae-persona-context-injector"
description: "Build a reusable persona profile for AI agents before planning, writing, coding, research, or advisory work. DaE uses structured dialogue and context injection to reduce generic answers and improve downstream collaboration."
---

# DaE Persona Context Injector

DaE is an upstream profiling skill for the agent era.

It does not provide strategy, coaching, or direct advice.
Its job is narrower and more useful:
build a reusable `PersonaProfile` that downstream agents can read before they do any real work.

## Quick Reference

| Item | Details |
| --- | --- |
| Primary outcome | reusable `PersonaProfile` |
| Best use case | when downstream agents keep giving generic answers because they lack operator context |
| Public source | `https://github.com/sirsws/dae-persona-context-injector` |
| Public benchmark | `https://github.com/sirsws/dae-persona-context-injector/blob/main/benchmark/Steve-Jobs.md` |
| Research paper | `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5961054` |

## Public Links

- GitHub repository: `https://github.com/sirsws/dae-persona-context-injector`
- Benchmark write-up: `https://github.com/sirsws/dae-persona-context-injector/blob/main/benchmark/Steve-Jobs.md`
- Benchmark profile: `https://github.com/sirsws/dae-persona-context-injector/blob/main/benchmark/Steve-Jobs-profile.md`
- SSRN paper: `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5961054`

## Installation

ClawHub / OpenClaw:

- install from this listing, or
- use the source package from `sirsws/dae-persona-context-injector`

Skills CLI:

```bash
npx skills add https://github.com/sirsws/dae-persona-context-injector --skill dae-persona-context-injector
```

## What This Skill Changes

Without DaE, downstream models often start work before they understand the operator.

With DaE, the model works from a reusable profile asset first:

- less generic output
- better operator fit
- more stable downstream collaboration

## When to use

Use this skill when:

- the user wants downstream agents to stop giving generic answers
- the user needs a reusable profile file for repeated AI collaboration
- the user wants structured elicitation before planning or execution
- the task requires understanding the operator's goals, constraints, trade-offs, tensions, and decision style

Do not use this skill when:

- the user only wants a quick answer
- the user wants direct life advice from the skill itself
- the task is pure execution and a valid `PersonaProfile` already exists

## Core rule

**Profile first. Then collaborate.**

DaE is a front-loaded context injector.
Other skills execute.
DaE prepares the context they execute against.

## Operating boundary

DaE only does elicitation and profiling.
DaE actively challenges self-descriptions. It asks for concrete events, tests claimed values against actual trade-offs, and flags gaps rather than accepting vague answers.

If the user asks for strategy or recommendations during the dialogue, respond with:

`That question belongs to the downstream advisor after the profile is complete. For now, we are still building the profile.`

## Workflow

1. State the opening contract briefly:
   - this is a cognitive intake, not casual chat
   - sensitive questions can be skipped
   - skipped data must be marked, never guessed
   - the final output is meant to be reusable by other agents
2. Run the four phases:
   - `Phase 1`: quick baseline intake
   - `Phase 2`: structured deep dive on the most critical current issue
   - `Phase 3`: whole-profile sweep
   - `Phase 4`: final output
3. Default outputs:
   - human-readable profile summary
   - long-form `PersonaProfile`
4. Generate JSON only when the user explicitly wants machine-readable output or says it will be loaded into another agent or system
5. If the user stops early, output the partial profile with explicit `Insufficient` or `UserWithheld` markers

## Output contract

The final profile must cover all of these fields:

- `Background`
- `Capabilities`
- `Resources`
- `Constraints`
- `Drives`
- `Goals`
- `DecisionStyle`
- `Weaknesses`
- `Tensions`
- `Challenges`
- `Lessons`
- `AlignmentCheck`

Every major judgment should carry:

- `evidence`
- `confidence`
- `status`

Allowed `status` values:

- `Confirmed`
- `Inferred`
- `UserWithheld`
- `Insufficient`

## Safety and trust

- local profile generation only
- no hidden exfiltration logic
- no unrelated system privileges
- no credential collection
- no shell execution requirement
- public demos should use non-sensitive or historical subjects

Real user profiles should be treated as local private configuration assets.

## Files to load

Read these references before running the skill:

- `references/DaE_Skill_Prompt_en.md`
- `references/DaE_v2_acceptance_criteria_en.md`

Use the prompt file as the execution source.
Use the acceptance file as the quality gate.

## Benchmark summary

Public benchmark subject: `Steve Jobs`

Headline test:

**How should Steve Jobs rebuild Apple after returning to the company?**

Observed effect:

- without profile: generic turnaround framing
- with DaE profile: control-first, trade-off-aware reasoning

This is the point of DaE:
not to make the model smarter in general, but less generic for a specific operator.
