---
name: bootstrap_review
description: Review an agent workspace's boot files (AGENTS.md, USER.md, SOUL.md, MEMORY.md, IDENTITY.md, TOOLS.md, and optional HEARTBEAT.md) against registry-backed context notes and produce a concise audit, refactor recommendations, and optional staged rewrites. Use when the user asks to review boot files, audit bootstrap files, refactor agent context files, check USER/SOUL/AGENTS redundancy, validate boot-file references, or compare current boot files against shared user context.
category: utilities
tags:
  - boot files
  - bootstrap files
  - agent files
  - audit
  - refactor
  - user context
  - registry
---

# Bootstrap Review

Run a chat-first review wizard for agent boot files.
This skill audits the current boot files for one agent, reads only the registered supporting context for that agent, and then produces:
- a structure review
- redundancy findings
- reference-validation findings
- recommendations for shortening or clarifying the files
- optional staged replacement drafts

Keep this skill review-first.
Do not silently rewrite live boot files.
Default to audit + recommendations.
Only produce staged replacement drafts if the user asks.
Do not write in place unless the user explicitly requests it.

## What counts as boot files

Treat these as the main boot files:
- `IDENTITY.md`
- `SOUL.md`
- `USER.md`
- `MEMORY.md`
- `AGENTS.md`
- `TOOLS.md`
- optional: `HEARTBEAT.md`

## Purpose of the skill

This skill exists to keep boot files:
- short
- durable
- non-redundant
- internally consistent
- aligned with the current role of the agent
- aligned with the current user context
- aligned with real referenced paths or real registry-backed context

This skill is not a general note summarizer.
This skill is not a giant memory compiler.
This skill should read the registered context once, use it to judge the boot files, and then recommend the leanest stable boot layer that still does the job.

## Core principles

- Boot files should stay small and high-signal.
- Heavy, evolving, or domain-rich notes should live outside the boot files.
- `IDENTITY.md` should answer who this agent is.
- `SOUL.md` should answer how this agent should feel and behave.
- `USER.md` should answer what stable facts and preferences about Greg matter to this agent.
- `MEMORY.md` should define what belongs in durable memory for this agent.
- `AGENTS.md` should define the agent's job, scope, boundaries, and decision posture.
- `TOOLS.md` should define tool posture, not repeat the entire mission.
- Repeated statements should be collapsed to the best single home.
- References should be real and testable.
- Placeholder references like `_Core` are not good enough unless they resolve to an actual mounted or registry-backed path pattern that the agent can use reliably.

## Registry model

Preferred registry file:
- `~/.openclaw/registries/boot_context_registry.json`

This registry defines which context files should be consulted for each agent during review.
The registry is for this skill only.
It is not meant to be loaded on every normal agent turn.

If the registry file does not exist:
- say so plainly
- offer to create it
- initialize it as an empty JSON object: `{}`

## Preferred registry shape

Use one object keyed by agent id.
Each agent entry may contain:
- `workspace`
- `boot_files`
- `shared_context`
- `agent_context`
- `review_goals`
- `staging_dir`

Preferred example:

```json
{
  "assistant": {
    "workspace": "~/.openclaw/workspaces/assistant",
    "boot_files": [
      "IDENTITY.md",
      "SOUL.md",
      "USER.md",
      "MEMORY.md",
      "AGENTS.md",
      "TOOLS.md",
      "HEARTBEAT.md"
    ],
    "shared_context": [
      {
        "type": "path_registry_key",
        "key": "USER_CONTEXT"
      }
    ],
    "agent_context": [
      {
        "type": "workspace_relative",
        "path": "notes/assistant-role-notes.md",
        "required": false
      }
    ],
    "review_goals": [
      "shorten boot files",
      "remove redundancy",
      "validate references",
      "keep assistant as front door and secretary"
    ],
    "staging_dir": ".boot-review"
  }
}
```

## Supported context entry types

### 1. `path_registry_key`
Resolve the key from `~/.openclaw/registries/path_registry.json`.
Use the resolved `wsl` path for reading.
If the key is missing or incomplete, report it.
Do not guess.

### 2. `workspace_relative`
Resolve relative to the agent workspace.

### 3. `absolute_wsl`
Read the explicit WSL path.
Use sparingly.

### 4. `mount_relative`
Resolve relative to the agent workspace, intended for mounted folders such as:
- `context/greg/profile.md`
- `context/greg/how-i-work.md`

## What to audit

For each selected agent, audit the boot files for:

### Structure fit
- does each file do the job it should do
- is the file too long or too thin
- does the file contain content that belongs in another boot file

### Redundancy
- repeated role statements across `IDENTITY.md`, `AGENTS.md`, and `TOOLS.md`
- repeated user preferences across `USER.md`, `AGENTS.md`, and `SOUL.md`
- repeated scope/boundary rules across multiple files

### Reference integrity
- references to shared notes that are only conceptual
- references to path-registry keys that are not explained
- relative paths that do not exist
- stale terminology
- renamed agents or folders not reflected consistently

### Context alignment
- does the current boot layer reflect the registered context
- does the current role of the agent match the surrounding user context
- are there durable facts missing that clearly belong
- is too much unstable detail being pushed into the boot layer

### Length discipline
- can the file be shortened without losing function
- should details be moved out to external context notes
- is the language too abstract or too repetitive

## Output model

Default output should be compact and decision-ready.
For each file, produce:
- status: good / revise / major cleanup
- 1–3 concrete findings
- specific recommendations

Then produce a cross-file section:
- top redundancies to remove
- top missing items to add
- top references to fix
- recommended overall simplification plan

## Optional staged rewrites

If the user asks for draft replacements, create them in the agent's `staging_dir`.
Do not overwrite live files by default.

Preferred staging directory:
- `<workspace>/.boot-review/`

Write staged replacements with the same filenames, for example:
- `.boot-review/AGENTS.md`
- `.boot-review/USER.md`

Also write a summary note:
- `.boot-review/review-summary.md`

## Trigger phrases

Treat requests like these as a request to run this skill:
- `boot file review`
- `review boot files`
- `audit boot files`
- `review AGENTS USER SOUL`
- `bootstrap file review`
- `agent file review`
- `refactor boot files`
- `check agent files for redundancy`
- `review assistant boot files`
- `review daily coach boot files`
- `review system engineer boot files`

## Wizard start

When triggered, open this menu:

```text
**Bootstrap Review**
**Registry file:** ~/.openclaw/registries/boot_context_registry.json

1. Review assistant
2. Review daily-coach
3. Review system_engineer
4. View registry
5. Edit registry guidance
6. Create draft replacements
7. Quit

Reply with 1, 2, 3, 4, 5, 6, or 7.
```

If the registry file does not exist yet, say:

```text
**Bootstrap Review**
**Registry file:** ~/.openclaw/registries/boot_context_registry.json
Status: not created yet

1. Create registry
2. Quit

Reply with 1 or 2.
```

## Review behavior

When reviewing one agent:
1. read the registry fresh
2. resolve the selected agent entry
3. read the listed boot files from the workspace
4. resolve and read the registered context files
5. compare current boot files to current context
6. produce a concise audit
7. ask whether to:
   - keep as-is
   - recommend edits only
   - create staged replacements

If any required registry-backed context is missing:
- report it under `missing context`
- continue the review using what is available
- do not invent missing context

## Draft replacement behavior

When creating draft replacements:
- preserve the current agent role unless the user explicitly asks to redefine it
- prefer shortening and de-duplication over expansion
- keep file tone aligned to the specific agent
- write only staged copies unless the user explicitly asks for in-place updates
- write a `review-summary.md` explaining the main changes

## Registry editing guidance

The skill may help the user create or adjust the registry, but keep the interaction simple.
Use:
- agent selection
- add or remove context entries
- edit `review_goals`
- edit `staging_dir`

Do not turn this into a giant general registry editor.
Keep it boot-review-specific.

## Recommended defaults for this environment

Use these default review goals if none are set:

### assistant
- keep assistant as front door and secretary
- reduce duplication across IDENTITY / AGENTS / TOOLS
- keep raw-capture and graduation language clear
- replace vague shared-note references with real workspace-relative or registry-backed references

### daily-coach
- keep daily coach centered on planning, review, and alignment
- avoid admin-system sprawl
- ensure stable life constraints are present but concise
- replace vague shared-note references with real workspace-relative or registry-backed references

### system_engineer
- keep system engineer technical and architecture-focused
- avoid personal-coaching bleed
- preserve durable technical decisions in the right file
- replace vague shared-note references with real workspace-relative or registry-backed references

## Safety rules

- Do not overwrite live boot files without explicit user instruction.
- Do not treat the registry as proof that a file is good; always inspect the actual file contents.
- Do not recommend longer files unless there is a real gap.
- Prefer moving unstable detail out of boot files rather than expanding them.
- Keep this skill useful for future agents; do not hardcode only today's three agents into the logic.

## Good review language

Prefer direct review language like:
- `good as-is`
- `shorten`
- `move to context note`
- `remove duplicate with USER.md`
- `reference is too vague`
- `replace placeholder with real path or mounted folder`
- `belongs in MEMORY.md instead`
- `belongs in AGENTS.md instead`

Avoid vague language like:
- `maybe improve`
- `feels okay`
- `might be better`

Be specific.
