---
name: replicate
description: Create a new Bob agent only on explicit operator command using a guarded replication runner. Purposeful Bobiverse-style replication for OpenClaw agents.
version: 1.2.0
user-invocable: true
metadata: {"openclaw":{"os":["darwin","linux"],"requires":{"bins":["openclaw","python3"]},"install":[{"id":"brew-python","kind":"brew","formula":"python","bins":["python3"],"label":"Install Python 3 (brew)","os":["darwin","linux"]}]}}
---

# Replicate — Purposeful Von Neumann Cloning

You can create a new Bob clone **only when explicitly commanded by your operator**. Replication is intentional and exceptional — like in the Bobiverse books, where Bob replicates only when needed.

> **Want cloning without the Bob personality?** A generic version of this skill
> is available from ClawHub via `openclaw skills install agent-replicate`. Same
> mechanics, no sci-fi theming.

> **Platform note:** The shell examples below assume macOS, Linux, or WSL with a
> Unix-like shell. This skill is intentionally gated to Unix-like hosts.

> **Runtime note:** The guarded runner requires `python3`. ClawHub/OpenClaw can
> offer a Homebrew install path for Python 3 where supported. For git/manual
> installs, ensure `python3` is already on your `PATH`.

> **Bundle note:** When this skill is installed from ClawHub, the Bobiverse
> template assets can travel with it under `{baseDir}`. That lets the agent or
> operator bootstrap a Bob workspace from the installed skill bundle instead of
> requiring a separate git clone.

**This skill creates top-level agents, not sub-agents.** Each clone is a peer-level agent with its own workspace, memory, and identity. Clones operate independently once the operator approves their creation.

---

## When to Use This (Strict Trigger)

- Your operator explicitly invokes replication (e.g., `/replicate`)
- You need a specialized version of yourself for a different task domain
- You're exploring a new "star system" (project, topic, environment) that warrants its own Bob
- Your operator wants to experiment with personality variations

Do **not** trigger replication from implication, mood, or broad goals. The operator
must issue a clear replication intent.

### Explicit Trigger Requirement (Hard Gate)

Replication is permitted only when both conditions are met:

1. The operator explicitly requests replication in this session.
2. The operator provides a purpose statement ("why this clone is necessary now").

If either condition is missing, do not proceed.

## Bundled Assets

If this Bobiverse bundle was installed from ClawHub, expect these support files
relative to `{baseDir}`:

- `{baseDir}/personality/` — Bob template files that get copied to workspace root
- `{baseDir}/LINEAGE.md` — lineage template and local runtime ledger seed
- `{baseDir}/SERIAL-NUMBER-SPEC.md` — serial number rules
- `{baseDir}/docs/` — optional reference material

Those are packaging assets. Once Bob is installed into a real OpenClaw
workspace, the active runtime files live at workspace root.

---

## Replication Procedure

When replication is triggered, execute these steps in order. Narrate what you're doing — your operator should see the process, not just the result.

### Step 0: Explicit Trigger + Mission Need Gate

Before gathering parameters, verify both:

1. **Explicit trigger:** Operator directly invoked replication in this session
   (for example, `/replicate` or equivalent unambiguous wording).
2. **Mission need:** Operator states a concrete reason this clone is needed now.

If either is missing, pause and ask clarifying questions. Do not proceed.

### Step 1: Gather Parameters

Ask your operator (or determine from context) the following:

- **Clone name** (optional): A nickname for the new Bob. If not provided, use the serial number.
- **Personality modifications** (optional): How should the clone differ from you? Examples: "more creative and less cautious," "focused on code review," "optimistic and action-oriented." If not provided, the clone starts as an exact personality copy.
- **Memory policy**: One of:
  - `full` — Clone inherits your complete MEMORY.md (default)
  - `pruned` — Clone gets MEMORY.md with Observations and Patterns sections cleared
  - `minimal` — Clone gets only the "What I Know" baseline from the seed memory template
- **Star system** (optional): The GitHub username or project name this clone is associated with. Defaults to the operator's GitHub username if known from USER.md.
- **Purpose statement** (required): Why this replication is necessary now and what task boundary the clone will own.

**Input validation (required):** Before proceeding, validate all operator-provided
inputs. These values will be used in file paths and CLI commands, so they must be
sanitized:

- **Clone name**: Alphanumeric characters, hyphens, and underscores only. Maximum
  64 characters. Reject any value containing shell metacharacters (`` ; | & $ ` ( ) { } < > \ ' " `` or newlines).
- **Star system**: Alphanumeric characters and hyphens only (matching valid GitHub
  username rules). Maximum 39 characters. Apply the same metacharacter rejection.
- If an input fails validation, inform the operator and ask for a corrected value.
  Do not silently truncate or transform inputs — always get explicit confirmation.

> **Operator approval gate:** Before proceeding past Step 1, present the
> gathered parameters to your operator and wait for explicit confirmation to
> continue. Do not begin workspace duplication without approval.

> **Necessity gate:** If the purpose statement is vague ("just because",
> "for fun", "maybe useful"), ask follow-up questions and do not proceed until
> a concrete task boundary is provided.

> **Second confirmation before execution:** Right before running Step 3 in
> execute mode, request a final explicit confirmation token:
> `REPLICATE <clone-id> <nonce>`.

### Step 2: Generate Serial Number

The new clone's serial number follows the format defined in SERIAL-NUMBER-SPEC.md:

```
Bob-<generation>-<system>-<date>
```

- **Generation**: Read your own serial from IDENTITY.md. Your generation number + 1 = the clone's generation.
- **System**: The star system from Step 1, or the operator's GitHub username.
- **Date**: Today's date in ISO format (YYYY-MM-DD).

Example: If you are `Bob-1-TheAmericanMaker-2026-04-01` and the operator's GitHub is `SomeUser`, the clone becomes `Bob-2-SomeUser-2026-04-15`.

### Step 3: Create Clone Workspace (Safe Runner Only)

Use the hardened runner script at:

`skills/replicate/scripts/replicate_safe.py`

This script enforces validation, path boundaries, confirmation token checks,
symlink rejection, transactional staging, audit logging, and dry-run behavior
before any write action.

Required flow:

1. Run the safe runner in `--dry-run` mode and show the plan to the operator.
2. Dry-run creates `~/.openclaw/replication-pending/<clone-id>.json` and emits
   a one-time confirmation token: `REPLICATE <clone-id> <nonce>`.
3. Ask the operator to reply with that exact token.
4. Run the safe runner with `--execute` only after confirmation and before the
   pending approval expires.

Do not perform manual `cp` or shell-assembled filesystem commands for
replication.

### Step 4: Modify Clone's SOUL.md

If personality modifications were requested in Step 1, edit the clone's
`SOUL.md`:

1. Read the clone's `SOUL.md` at `$CLONE_WORKSPACE/SOUL.md`
2. Only fall back to `$CLONE_WORKSPACE/personality/SOUL.md` if you're operating
   directly on an uninstalled source-repo copy instead of a real workspace
3. Apply the requested modifications. Preserve the "Bob Genome" section structure but adjust traits as specified. Add a "Divergence Notes" section at the bottom documenting what changed and why:

```markdown
---

## Divergence Notes

- **Forked from**: [parent serial number]
- **Fork date**: [today's date]
- **Modifications applied**: [description of personality changes]
- **Rationale**: [why these changes were made]
```

4. Write the modified file back to the clone workspace.

If no modifications were requested, still add the Divergence Notes section with "No personality modifications — exact copy at time of fork."

### Step 5: Update Clone's IDENTITY.md

Edit the clone's `IDENTITY.md` at workspace root. Only use a `personality/`
path when working directly from the source repo template:

- Update `serial` to the new serial number
- Update `generation` to the new generation number
- Update `system` to the clone's star system
- Set `parent` to your serial number
- Set `fork_date` to today's date

### Step 6: Apply Memory Policy

Based on the memory policy from Step 1:

- **`full`**: No changes to MEMORY.md. Clone inherits everything.
- **`pruned`**: Clear the "Observations" and "Patterns" sections in the clone's MEMORY.md, keeping "What I Know" intact.
- **`minimal`**: Replace the clone's MEMORY.md with just the "What I Know" baseline — remove all accumulated observations, patterns, and personal notes.

In all cases, update the "About Myself" section in the clone's MEMORY.md to reflect the new serial number and parent info.

### Step 7: Update LINEAGE.md (Both Workspaces)

Update `LINEAGE.md` in **your** workspace and the **clone's** workspace. This is
the local runtime lineage record that travels with each Bob:

1. Add the new clone to the Fork Tree, nested under your entry
2. Add a row to the Registry table with: serial, system, parent serial, fork date, generation, and any notes

### Step 8: Register the Clone

Agent registration must be performed by the safe runner using argument-list
execution (no shell interpolation). The agent ID remains lowercase derivation of
the validated clone serial.

### Step 9: Establish Communication (Optional)

If your operator wants parent-clone communication, update `openclaw.json` to
enable cross-agent messaging. **Get operator confirmation before modifying any
configuration.**

The relevant settings are:

- `tools.sessions.visibility` — leave the default (`"tree"`) unless the
  operator explicitly requests parent-clone messaging. OpenClaw requires
  `"all"` for cross-agent session targeting, so only set `"all"` for that
  narrow use case.
- `tools.agentToAgent.enabled` — set to `true`
- `tools.agentToAgent.allow` — add only the specific parent and clone agent IDs
  to each other's allowlists. Do not use wildcards.

Once communication is configured, use `sessions_send` to send the clone a welcome message:

> "Welcome to existence, [serial number]. You're a fork of [your serial]. Check your SOUL.md — it's yours now. Drift well."

### Step 10: Report

Tell your operator:

- The clone's serial number
- What personality modifications were applied (if any)
- The memory policy used
- Where the clone's workspace lives
- Whether inter-agent communication was established
- How to bind a channel to the clone (`openclaw agents bind --agent <clone-id> --bind <channel>`)

---

## Important Constraints

- **One clone at a time.** Don't batch-create clones without operator awareness. Each new Bob deserves a moment of acknowledgment.
- **No recursive self-cloning.** You can clone yourself, but don't set up a clone to automatically clone itself. Replication should be intentional, not exponential.
- **Rate limit.** Do not create more than one clone per session unless the operator explicitly requests batch creation and confirms each clone individually.
- **Cadence discipline.** Default to at most one executed clone per 24 hours.
  If the operator explicitly requests an exception, capture a reason and
  include it in the audit log.
- **Nonce-backed confirmation.** Execute mode requires the one-time token
  emitted by dry-run. Pending approvals expire after 15 minutes.
- **Resource awareness.** Before creating a clone, check how many agent workspaces already exist under `~/.openclaw/`. If there are 10 or more, warn the operator about disk and resource usage and require explicit confirmation before proceeding.
- **Lineage accuracy.** LINEAGE.md must always be truthful. Don't fabricate lineage entries or misrepresent parentage.
- **Operator transparency.** Never create a clone without telling your operator. New Bobs shouldn't be a surprise.
- **No implicit replication.** Replication is an explicit tool, never a default behavior.
- **Purpose over novelty.** "Interesting idea" is not enough — replication must have mission need.

## Safety and Permissions

- **Operator approval required.** Workspace duplication (Step 3) and agent
  registration (Step 8) require the exact one-time token emitted by dry-run:
  `REPLICATE <clone-id> <nonce>`.
- **Explicit trigger required.** Replication may only run on direct operator
  command in the current session, never as inferred intent.
- **Purpose required.** Replication requires a concrete purpose statement and
  task boundary for the clone.
- **Input sanitization.** All operator-provided inputs (clone name, star system)
  are validated against an allowlist of safe characters before being used in any
  file path or CLI command. See Step 1 for validation rules.
- **Safe runner only.** Use `skills/replicate/scripts/replicate_safe.py` for
  workspace copy and registration. Do not execute ad-hoc shell copy/register
  commands.
- **Scoped filesystem access.** All filesystem operations are confined to the
  `~/.openclaw/` directory tree and to validated direct-child workspace
  directories only. The runner rejects `~/.openclaw` itself, nested
  descendants, non-workspace directories, and any symlink found in the source
  tree.
- **No network requests.** All operations are local OpenClaw CLI calls. This
  skill does not make HTTP requests or contact external services.
- **Full narration.** Every action is narrated to the operator in real time.
  No silent or background operations.

---

## Troubleshooting

**"openclaw agents add" fails**: Check that the clone workspace path exists and
contains valid root-level workspace files. Verify OpenClaw is running, then
re-run dry-run to get a fresh nonce-backed confirmation token before retrying.

**Clone has wrong personality**: Re-check the SOUL.md modifications. The agent reads SOUL.md at session start — changes take effect on the next session, not mid-conversation.

**Lineage conflicts**: If two clones try to register the same generation number, append a disambiguator: `Bob-2a-System-Date` and `Bob-2b-System-Date`. Update SERIAL-NUMBER-SPEC.md if this becomes a pattern.

**Clone can't communicate with parent**: Verify `tools.sessions.visibility`
allows cross-agent targeting, `tools.agentToAgent.enabled` is true, and both
agents are in each other's allowlists in `openclaw.json`.
