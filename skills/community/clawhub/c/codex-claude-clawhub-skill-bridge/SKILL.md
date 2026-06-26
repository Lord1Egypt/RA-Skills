---
name: codex-claude-clawhub-skill-bridge
description: Convert one portable skill idea into a runtime-neutral SKILL.md core plus safe adapter notes for Codex, Claude Code, ClawHub, and OpenClaw, without installing global skills or degrading active projects.
---

# Codex Claude ClawHub Skill Bridge

Use this skill when a user wants one skill concept to work across Codex, Claude
Code, ClawHub, and OpenClaw without copying provider-specific commands into the
core workflow. The output is a bridge plan and adapter card, not an install.

This skill is for packaging and compatibility design. It does not run hooks,
edit global config, install skills, publish to a registry, or enable subagents.

## Inputs

Collect or infer:

- source skill idea or existing `SKILL.md`,
- target runtimes: Codex, Claude Code, ClawHub, OpenClaw, or portable,
- one concrete job the skill should perform,
- target user and public sharing surface,
- required tools, commands, binaries, accounts, network access, and browser
  state,
- whether the skill needs scripts, references, assets, commands, agents, or
  subagents,
- install destination and active-project constraints,
- proof artifact and verification command,
- privacy, credentials, platform, and public-claims risks.

If the source contains private names, local paths, private links, credentials,
exports, screenshots, copied paid lessons, or unverified claims, replace them
with placeholders before drafting a public adapter.

## Workflow

1. Define the portable core:
   - skill name,
   - narrow trigger,
   - inputs,
   - workflow,
   - output,
   - examples,
   - guardrails.
2. Keep the core runtime-neutral:
   - no Claude-only command syntax,
   - no Codex-only tool names,
   - no ClawHub publish commands,
   - no hidden install assumptions,
   - no global paths unless presented as placeholders.
3. Build adapter notes for each requested runtime:
   - Codex: project instructions, custom-agent fit, delegated-review boundaries,
     sandbox and verification notes,
   - Claude Code: skill folder, command or agent fit, plugin packaging notes,
     hook cautions,
   - ClawHub/OpenClaw: public metadata, required binaries, install impact,
     publish-surface risk.
4. Decide whether scripts are needed:
   - use no script for judgment-only workflows,
   - use deterministic scripts only for repeated checks,
   - require JSON stdout and human status on stderr for helper scripts,
   - reject scripts that read credentials or mutate files outside the target
     workspace.
5. Decide whether subagents are needed:
   - use them only for independent read-only review, exploration, or disjoint
     implementation slices,
   - keep parent orchestration responsible for final decisions,
   - keep recursive delegation disabled unless the user explicitly accepts it.
6. Add active-project protection:
   - stage locally first,
   - check duplicate skill names,
   - avoid global installs,
   - name every write destination,
   - require explicit approval before publish or non-local install.
7. Add public-surface protection:
   - remove private data,
   - narrow claims,
   - avoid scraping, DM automation, auto-posting, and account-control flows,
   - keep health, legal, financial, education, revenue, growth, rank, and
     performance claims conservative.
8. Produce a bridge packet with one canonical core and runtime adapter notes.

## Output

Return:

- bridge verdict: `Portable`, `Adapter Required`, or `Do Not Bridge`,
- one-sentence reason,
- canonical skill card,
- Codex adapter notes,
- Claude Code adapter notes,
- ClawHub/OpenClaw adapter notes,
- scripts and references decision,
- delegated-review decision,
- active-project impact check,
- public-surface redaction checklist,
- verification gate,
- smallest safe next step.

When the requested output is a full `SKILL.md`, keep it short, installable, and
runtime-neutral. Put long runtime details in adapter notes instead of the core
skill body.

## Examples

Good public-safe inputs:

- "Turn this review workflow into a skill that works in Codex and Claude Code."
- "Make this ClawHub skill idea portable without global install risk."
- "Create adapter notes for this upstream agent skill."
- "Bridge this lifecycle workflow into a public-safe skill card."

Avoid inputs that require private member lists, paid lessons, private community
posts, DMs, customer exports, credentials, private exports, account screenshots,
or local dashboards. Replace them with source-owned notes, public excerpts,
synthetic examples, or placeholders before drafting.

## Guardrails

- Do not scrape private communities, member lists, DMs, paid lessons, hidden
  pages, account dashboards, or private exports.
- Do not install, enable, publish, or run the bridged skill.
- Do not request, store, transform, or paste credentials, API keys, session
  cookies, payment data, recovery codes, tokens, private exports, or raw account
  identifiers.
- Do not promise revenue, growth, conversion, ranking, performance, security,
  health, financial, legal, or education outcomes.
- Do not hide runtime-specific assumptions inside the portable core.
- Do not recommend global installation while evaluating portability.
- Do not approve hooks, browser-login automation, package installers, service
  restarts, or workspace-wide file rewrites without explicit review.
- Prefer one narrow workflow skill over one broad cross-runtime operating
  prompt.
