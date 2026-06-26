---
name: defragmenter
description: "Structural knowledge defragmentation for OpenClaw workspaces. Finds information, rules, and operational facts that are spread across the wrong files or embedded in the wrong layer, then rewrites them into the proper files without deleting source material. Use when the workspace feels fragmented, logic is embedded in cron/jobs instead of flow files, preferences are scattered, or facts exist but are not assembled into one coherent working structure."
---

# Defragmenter

`defragmenter` is a structural reorganization skill for OpenClaw workspaces.

It does **not** behave like a cleaner, trash collector, or memory compressor.
It does **not** delete information.

Its job is to find knowledge that already exists, but is fragmented across the wrong places, and reassemble it into the correct structural locations.

## What It Does

Defragmenter looks for situations like:
- logic living inside a cron message instead of a flow file
- operational facts existing in chat or notes but not in `CONTAINER_STATE.md`
- preferences mentioned in conversation but not recorded in the right preference file
- workflow rules spread across multiple files without a clear source of truth
- facts that exist, but are not assembled into one coherent working structure

Then, after user confirmation, it:
- copies or rewrites that knowledge into the proper file (from the Allowed Targets list only)
- preserves the existing information rather than deleting it
- makes the workspace more structurally coherent

## Core Principle

**Reorganize, not destroy.**

Defragmenter may:
- move logic to the correct file
- duplicate essential context into the correct source-of-truth file
- rewrite instructions into a cleaner structure
- connect fragmented pieces of working knowledge

Defragmenter does **not**:
- delete source material by default
- prune history
- compress memory for brevity
- behave like a cleanup/trash skill

## Typical Use Cases

Use this skill when:
- the workspace feels architecturally messy
- the right information exists, but in the wrong place
- a workflow is half in chat, half in cron, half in files
- operational state has drifted away from documentation
- multiple files describe the same process, but no file is the clear source of truth

## Examples

### Example 1: Cron logic is too smart
A cron message contains detailed workflow logic.

Defragmenter should:
- extract that logic into a flow file
- reduce the cron to a simple trigger
- preserve the intent without deleting history

### Example 2: Operational facts are stranded
A container repair decision exists in chat or daily notes, but not in `CONTAINER_STATE.md`.

Defragmenter should:
- rewrite the important fact into `CONTAINER_STATE.md`
- add or update restore instructions if appropriate

### Example 3: Preferences are scattered
Food, browser, or workflow preferences exist in conversation history but not in their proper file.

Defragmenter should:
- gather them into the correct preference/source-of-truth file

## Allowed Targets

Defragmenter may only reorganize knowledge into files within the current workspace that match these patterns:
- `MEMORY.md`
- `memory/*.md`
- `CONTAINER_STATE.md`
- `flows/*.md`
- preference files within the current workspace root

Defragmenter must **not** modify:
- Any file under `skills/` or any `SKILL.md` file (including its own)
- Shell scripts, executables, or files outside the workspace root
- `.env`, credentials, or configuration files not listed above
- Any file belonging to another skill's directory

## Output Style

First, return a dry-run structural report for user review:

```text
Defragmentation scan complete. Proposed changes:
- MOVE workflow logic from cron text → flows/deploy.md
- COPY operational facts → CONTAINER_STATE.md
- COPY scattered preference rules → preferences.md
- No deletions proposed

Awaiting confirmation to apply.
```

After the user approves, apply changes and return a confirmation report.

## Safety

- **Dry-run by default.** When invoked, Defragmenter first produces a proposed change list (files to modify, what will be added/moved) without making any changes. Changes are only applied after the user confirms.
- **Confirmation required.** Every file write must be presented to the user for approval before execution. Do not batch-apply changes silently.
- **Read-only scan first.** Always begin by scanning and reporting what fragmentation was found. Never jump straight to writing files.
- **No deletions.** Defragmenter must not delete content from source files, even if the content has been copied to its correct location. The user may choose to clean up sources separately.

## Rules

- Prefer creating a clear source of truth
- Preserve information rather than deleting it
- Structural coherence matters more than brevity
- If something is already in the right place, leave it alone
- Make minimal, high-value reorganizations
- **Only write to files listed in the Allowed Targets section above**
- **Never modify skill definitions, SKILL.md files, or files outside the workspace**
- **Always present a dry-run summary and wait for user approval before writing any file**

## Design Goal

Defragmenter exists to restore structural coherence across workspace knowledge.

It is focused on placement, source-of-truth repair, and reassembly of fragmented context across files and layers.
