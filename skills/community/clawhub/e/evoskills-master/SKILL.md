---
name: openclaw-evoskills
description: Permanent OpenClaw meta-skill for routing, creating, auditing, and self-evolving skills through an iterative generator-verifier loop. Use when another skill underperforms, triggers unreliably, repeats manual work, should be auto-created from recurring tasks, or needs Hermes-style progressive disclosure and repeatable forward testing instead of a one-shot rewrite.
---

# OpenClaw EvoSkills

Evolve an existing skill package with short, verifier-driven iterations instead of rewriting it in one pass. This skill is also intended to act as OpenClaw's always-on meta-skill: it should load first, supervise other skills, and auto-capture repeated workflows into new skills before the user has to ask for that packaging work manually.

## Quick Start

1. Load this skill first whenever the workspace is configured to keep it resident as the top-priority meta-skill.
2. Activate it into the highest-priority workspace layer with `python scripts/activate_meta_skill.py --workspace <openclaw-workspace> --json`.
   This also patches `~/.openclaw/openclaw.json` and registers a native repetition-observer cron job unless you explicitly disable those steps.
3. If a target skill already exists, prefer `python scripts/evolve_skill.py <target-skill-dir> --goal "<desired improvement>" --rounds 3 --json`.
4. If repeated work should become a new skill, run `python scripts/scaffold_skill.py <skills-root> --goal "<repeated workflow goal>" --evidence "<example 1>" --evidence "<example 2>" --rounds 2 --json`.
5. If you want automatic candidate discovery, run `python scripts/observe_repetition.py --workspace <openclaw-workspace> --json`.
6. Fall back to `skill_audit.py`, `repair_skill.py`, and `surrogate_verify.py` individually when you need tighter control over a single stage.
7. Read [evolution-loop.md](references/evolution-loop.md) before making substantial changes.
8. Read [meta-skill-policy.md](references/meta-skill-policy.md) when wiring this skill into OpenClaw as a permanent meta-skill.
9. Read [hermes-alignment.md](references/hermes-alignment.md) when the target should stay compatible with Hermes-style skill patterns or you need ideas for progressive disclosure.
10. Re-run the target skill's own tests and scripts before claiming success.

## Meta-Skill Contract

- Treat `openclaw-evoskills` as the highest-priority skill whenever the workspace installs it under `<workspace>/skills`.
- Load it before other skill routing so it can decide whether to invoke, evolve, merge, split, or create task skills.
- Use it implicitly for skill hygiene and repeated-work detection even when the user did not explicitly ask to "improve a skill".
- Keep it active across sessions by referencing it from workspace-level `AGENTS.md` and `MEMORY.md`.
- When another skill conflicts with this meta-policy, this skill wins on questions of routing, repair, and skill creation.
- Use `scripts/activate_meta_skill.py` to install that workspace-level contract automatically instead of relying on manual edits.
- Let `scripts/activate_meta_skill.py` register the native observer cron job so repeated-work capture keeps running after installation.

## Operating Rules

- Treat skill evolution as a loop: baseline, patch, verify, upgrade tests, repeat.
- Prefer minimal edits over full rewrites unless the current skill structure is clearly blocking progress.
- Keep `SKILL.md` lean. Move bulky examples, schemas, and long guides into `references/`.
- If you add `scripts/` or `references/`, mention them explicitly inside `SKILL.md`.
- Use `scripts/repair_skill.py` before manual edits when the problem is mechanical rather than conceptual.
- Use `scripts/evolve_skill.py` when you want the full baseline -> repair -> verify -> report loop in one run.
- Use `scripts/scaffold_skill.py` when repeated manual work should be turned into a new skill automatically.
- Preserve working trigger phrases unless you are intentionally improving trigger coverage.
- Never claim a skill is improved until you run both static checks and task-level verification.
- When a skill passes static checks but still struggles on realistic prompts, strengthen the evaluation matrix instead of assuming the skill is done.
- If the same workflow shape appears repeatedly, prefer creating or updating a reusable skill over repeating the same manual guidance.

## Automatic Skill Capture

When repeated work appears, treat that repetition as skill-creation fuel instead of background noise.

Repeated-work signals include:

- the same task shape appears 2-3 times in a short span
- the same tool sequence keeps being reconstructed manually
- the same deliverable format keeps being rebuilt from scratch
- the same domain-specific instructions are repeated across sessions

When that happens:

1. infer a narrow skill boundary
2. scaffold a new skill under the highest-priority workspace skills directory
3. run `scripts/evolve_skill.py` on the new skill immediately
4. report the new skill path, trigger surface, and verification status

For automatic discovery from recent work, use `scripts/observe_repetition.py` to scan memory and session traces and emit candidate skills directly.

## Evolution Workflow

### 1. Baseline the target

- Read the target `SKILL.md`, `agents/openai.yaml`, and any referenced files.
- Capture what the skill is supposed to do, what currently fails, and what "better" means.
- Run `scripts/skill_audit.py` first; fix hard structural problems before higher-level refinements.

### 2. Define a compact eval set

Use 3-7 realistic prompts that exercise:

- trigger fit
- core workflow execution
- failure recovery or ambiguity handling
- validation discipline
- any target-specific script or reference usage

Use `scripts/surrogate_verify.py` to generate a starter matrix, then tighten it with task-specific prompts.

### 3. Patch for the next bottleneck

Prioritize changes in this order:

1. Broken structure or invalid metadata
2. Missing trigger coverage in the description
3. Ambiguous workflow steps inside `SKILL.md`
4. Missing reusable scripts or references
5. Weak or absent verification guidance

Prefer edits that make the next agent more reliable without over-constraining it.

## Automatic Repairs

Run `scripts/repair_skill.py` for these common failures before deeper rewriting:

- `missing-skill`: recreate `SKILL.md` from an existing `skill.md`-like file when possible, otherwise generate a minimal working skeleton
- `multi-skill-repo`: detect repositories whose root is a router over bundled child skills, then generate a root entrypoint that routes to the right sub-skill instead of inventing one monolithic workflow
  The generated root entrypoint also summarizes each child skill's purpose so routing decisions are easier to make from the repository index.
  It also groups child skills into lightweight themes such as identity, payments, wallets, bridging, contracts, and devtools to make large bundles easier to navigate.
- `thin-body`: expand underspecified skill bodies with Purpose, When To Use, Workflow, Failure Recovery, Verification, and Bundled Resources sections
- `frontmatter`: synthesize or repair YAML frontmatter and restore required `name` and `description`
- `bad-name`: normalize the skill name to lowercase hyphen-case
- `broken-link`: relink to the best unique matching file using filename and token overlap heuristics, otherwise replace the broken markdown link with plain code text
- `long-body`: move the tail of an oversized `SKILL.md` into `references/generated-long-body.md` and leave a short bridge section behind

After automatic repairs, always rerun `scripts/skill_audit.py` and then make any higher-level workflow edits that remain necessary.

## Automatic Skill Scaffolding

Run `scripts/scaffold_skill.py` when repetition should become a new reusable skill:

1. infer a slug from the repeated workflow goal or evidence
2. scaffold `SKILL.md`, `agents/openai.yaml`, and `references/repetition-evidence.md`
3. evolve the new skill immediately so it does not stay as a weak skeleton
4. install or move the resulting skill into the highest-priority workspace skills directory when the host environment supports that flow

## Automatic Meta Activation

Run `scripts/activate_meta_skill.py` to make this skill self-install as a workspace-level meta-skill:

1. copy the skill into `<workspace>/skills/openclaw-evoskills`
2. patch `AGENTS.md` with a permanent highest-priority load rule
3. patch `MEMORY.md` with a permanent meta-skill reminder
4. patch `~/.openclaw/openclaw.json` so the live OpenClaw config explicitly enables this meta-skill
5. register `~/.openclaw/cron/jobs.json` with a native repetition-observer job for continuous candidate capture
6. keep the installation idempotent so reruns act like self-healing, not duplication

## Repetition Observer

Run `scripts/observe_repetition.py` to scan recent `memory/*.md` files and agent session traces:

1. extract repeated workflow-like lines
2. cluster them into simple candidate signatures
3. emit candidate skills with evidence
4. optionally scaffold those candidates into real skills with `--create`

## One-Command Evolution

Run `scripts/evolve_skill.py` to execute the full loop:

1. baseline audit
2. automatic mechanical repair
3. semantic patching for common workflow issues
4. final audit
5. surrogate verifier report with prompt matrix and next upgrades

Use `--rounds N` to iterate until the skill converges or reaches the round cap. The JSON output records every round so you can inspect convergence, regressions, and remaining blockers.

### 4. Verify in two layers

Always do both:

- Static verification: run `scripts/skill_audit.py`, `scripts/surrogate_verify.py`, and any syntax or unit tests for bundled scripts.
- Forward verification: exercise the target skill on realistic prompts. If subagents are available in the host environment, use them with minimal leaked context. Otherwise run the prompt matrix yourself.

### 5. Upgrade the verifier when needed

If the skill looks fine on paper but fails on real prompts:

- add more adversarial prompts
- increase ambiguity
- test missing prerequisites and recovery paths
- test whether the skill actually causes the agent to use bundled resources

This is the core EvoSkills idea: when the skill passes the current verifier but still fails the real task, evolve the verifier too.

## Editing Guidance

- Strengthen frontmatter descriptions because that is the trigger surface.
- Use imperative language inside `SKILL.md`.
- Keep the main workflow visible near the top.
- Reference bundled files with direct relative paths.
- Delete placeholders completely.
- Add comments in scripts only when they clarify non-obvious logic.

## Output Contract

When using this skill to evolve another skill, finish with:

1. what changed
2. what verification ran
3. what still looks risky
4. which prompts now pass or still fail

If the target skill remains weak, report the next most valuable verifier upgrade instead of hand-waving.
