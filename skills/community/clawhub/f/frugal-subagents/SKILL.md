---
name: frugal-subagents
description: >-
  On Claude Fable 5.1 or Opus, subagents inherit the session's expensive model and can spawn more of
  themselves, so one research fan-out can burn the usage limit in minutes; this plugin's PreToolUse hook runs every subagent on a
  cheap model unless one is named explicitly, blocks nested spawns and caps spawns per session, and
  this skill says how to delegate well under those rules. Use whenever the session is about to delegate — spawning
  agents, running web scans or research passes in parallel, "fan out", "run a fleet of agents",
  "search across many sites", comparing listings/prices/flights/apartments/suppliers across the web —
  and whenever the user says subagents burn through the limit, agents spawned more agents, asks to
  "limit subagents", "run agents on a cheaper model", "set up frugal subagents", "which model did the
  helpers use", or when Claude Code reports that the frugal-subagents hook failed to run (Node.js
  missing).
---

# Frugal Subagents

## Why

Delegation is where a session's budget leaks. Subagents inherit the parent's model unless told otherwise, so a top-tier session that fans out three research agents is running three more copies of its most expensive model — and if one of them fans out again, the cost multiplies silently. On subscription plans that can exhaust the limit in minutes, with most results lost to rate limits. Written rules ("use sonnet for scans") don't survive context compaction; this plugin turns them into a hook, which does.

## What the hook enforces

Every `Agent` call passes through `hooks/guard.js` before it runs. Nothing is silent: when the hook fills in a model it says so in the tool result, and a blocked call returns the reason as tool feedback.

| Rule | Default | Lift / tune |
|---|---|---|
| No `model` given → the default cheap model is injected | `sonnet` | `FRUGAL_SUBAGENTS_DEFAULT_MODEL=haiku`; strict mode `FRUGAL_SUBAGENTS_REQUIRE_MODEL=1` denies instead of defaulting |
| No subagents from inside a subagent | on | `FRUGAL_SUBAGENTS_ALLOW_NESTED=1` |
| Spawns per session | 12 | `FRUGAL_SUBAGENTS_MAX_SPAWNS=<n>` |
| Ceiling on subagent tier | off | `FRUGAL_SUBAGENTS_MAX_TIER=sonnet` (or `haiku`, `opus`) |
| Everything off | — | `FRUGAL_SUBAGENTS_OFF=1` |

Variables go into the user's or project's `settings.json` under `"env"`, or the shell environment. The user changes them, not the session: a denied call is policy, and splitting or rephrasing a call to get around it is not an option.

## How to delegate under the guard

**Pick the tier by what the work costs, not by how important it feels.** Search/fetch volume, page scanning, listing comparison, extraction, renames, tests-to-a-spec → `sonnet` or `haiku` (leaving `model` out gives the default, `sonnet`). The session's own top-tier model is for judgment that cannot be delegated — decomposition, contested decisions, final synthesis — and normally stays in the main session; name it explicitly on a subagent only when that judgment genuinely has to run in a separate context.

**Use the bundled workers before writing a custom brief:**

- `web-scout` (sonnet, web + files, no Bash, no Agent) — research passes. Give it the question, the target list or search terms, and the file to write into.
- `extractor` (haiku, files only) — turning collected material into tables, lists, JSON, deduplicated notes.

Both write their full output to files and return a short digest, so the expensive context receives conclusions, not dumps.

**Brief so the worker can't drift:** goal, scope (files, sites, count), constraints, definition of done, the output path, and the user's request quoted verbatim where it matters. Workers don't see the conversation.

**One agent, then reuse it.** A follow-up in the same area goes to the agent already running, not to a new spawn — that keeps its context and stays within the session budget. Don't spawn to double-check yourself, and don't spawn what a handful of your own tool calls would finish.

**Results go to files first.** Anything worth keeping is written to disk by the worker as it goes; a worker cut off by a rate limit then loses minutes, not the pass.

**When the guard denies a call,** do what the reason says: finish inline, reuse a running agent, or tell the user which limit is in the way and let them decide. Never work around a hook.

**Workflows are outside the guard.** Agents started by the `Workflow` tool (`agent()` calls in a workflow script) don't pass through the `Agent` hook. On a top-tier session, before running any workflow, put `model: "sonnet"` (or `"haiku"`) in the options of every `agent()` call in the script unless that step genuinely needs top-tier judgment, and keep the agent count of the script in view — a research workflow can spawn a hundred agents in minutes.

## Talking to a non-technical user

Many users of this plugin are not developers — they delegate web research (housing, travel, purchases, suppliers). With them, say "helpers" rather than "subagents", name the model plainly ("the cheaper model, Sonnet"), and never quote hook JSON. When a limit kicks in, one sentence: what stopped, why, what you'll do instead, and — only if it matters — which setting changes it. If the user wants a setting changed, offer to edit `settings.json` → `"env"` for them rather than explaining where the file is.

## If the guard can't run (Node.js missing)

The hook is a Node.js script. If Node.js is not installed, Claude Code shows a hook error when a subagent is spawned (typically `node` not found / not recognized) and the spawn proceeds unguarded. When you see that:

1. Tell the user in one plain sentence: the plugin's guard needs Node.js, it isn't installed, so the limits aren't enforced yet — the guidance still applies and you'll follow it manually.
2. Offer to install Node.js LTS and wait for a yes. Use the platform's package manager: Windows `winget install OpenJS.NodeJS.LTS`; macOS `brew install node` (or the installer from nodejs.org if Homebrew is absent); Debian/Ubuntu via the NodeSource setup script or `sudo apt install nodejs npm`; otherwise point to nodejs.org. Don't install without consent, and don't use `sudo` without saying so.
3. After installation, the user starts a new Claude Code session; the guard is active from then on. Until then, apply this skill's rules yourself: cheap tier, no nesting, results in files.

## Companion settings (first-party, optional)

Claude Code has its own levers that combine well with the guard; recommend them when the user asks how to lock things down harder, and put them in `settings.json` → `"env"`:

- `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` — Claude Code's own default for subagents whose definition doesn't set a model; the guard's default does the same job at the call level and additionally tells the session which model was used. `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` (Claude Code 2.1.257+) makes that model mandatory for every subagent, overriding both agent definitions and per-call choices — the strictest setting, at the cost of any explicit override.
- `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` — nesting depth (default 3); with `1`, subagents don't even receive the `Agent` tool.
- `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` (default 20), `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` (default 200).

## Verify the hook

After installing or editing the plugin, confirm the guard answers as expected (Node.js required — it is what runs the hook):

```bash
node -e "
const {spawnSync}=require('child_process');
const run=(ev)=>spawnSync('node',[process.argv[1]],{input:JSON.stringify(ev),encoding:'utf8'}).stdout;
const base={hook_event_name:'PreToolUse',tool_name:'Agent',session_id:'selftest-'+Date.now()};
const d=(s)=>{try{return JSON.parse(s).hookSpecificOutput}catch{return null}};
const a=d(run({...base,tool_input:{prompt:'x'}}));
console.log('no model  →', a&&!a.permissionDecision&&a.updatedInput&&a.updatedInput.model==='sonnet' ? 'defaulted to sonnet' : 'UNEXPECTED');
console.log('opus      →', run({...base,tool_input:{prompt:'x',model:'opus'}})==='' ? 'passed through' : 'UNEXPECTED');
const n=d(run({...base,agent_id:'a1',tool_input:{prompt:'x',model:'haiku'}}));
console.log('nested    →', n&&n.permissionDecision==='deny' ? 'denied' : 'UNEXPECTED');
" <path-to-plugin>/hooks/guard.js
```

Expected: `defaulted to sonnet`, `passed through`, `denied`. Live check: with the plugin loaded, ask Claude to spawn a subagent without naming a model — it runs on `sonnet`, Claude sees a note saying so, and the user gets a one-time notice about the defaults for the session.
