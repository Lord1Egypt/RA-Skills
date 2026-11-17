---
name: clawpatch-supervise
description: New and fucking improved with more cursing. Install, run, recover, or explain the standalone ClawPatch queue supervisor when someone needs a whole repair queue, exact stopped-finding recovery, or real completion proof.
---

# ClawPatch Supervise

> **🤬🦶💥 NEW AND FUCKING IMPROVED — NOW WITH MORE CURSING 🔨🗑️🔥**

Use the standalone supervisor as the outer runtime for a ClawPatch repair queue.

## Contract

- ClawPatch owns review, finding selection, repair, revalidation, and finding status.
- The supervisor owns ordering, watchdogs, exact checkpoints, commits, optional pushes, and completion proof.
- A zero-feature heuristic map is not completion; the supervisor must run ClawPatch's agent mapper before accepting an empty repository.
- Run the supervisor outside the target repository's implementation environment, even when the target is Manageroo itself.
- Never skip, triage, hide, or manually repair an unresolved ClawPatch finding.
- Never discard dirty source unless an exact supervisor checkpoint proves ownership.
- Treat both open and uncertain sandbox-limited revalidation as candidates for the bounded workspace-write and authorized trusted-host retry ladder before another fix call.
- Preserve every genuinely new exact repair tree and let the next same-finding fix use the validator's concrete evidence. When an open or uncertain revalidation adds evidence but no file edit on top of an already checkpointed repair, retry that same finding within the supervisor's two-attempt evidence budget without saving the identical tree or advancing the queue.
- When configured project gates fail while resuming a provenance-verified stopped `open` or `uncertain` repair, preserve the exact checkpoint and re-enter only that finding with the gate failure as evidence. Keep fixed, false-positive, ownership-mismatched, and ambiguous states fail-closed.
- Treat untracked `node_modules/**` package-install output as runtime noise, while retaining tracked files there as source. Resume a legacy dependency-heavy checkpoint only when its full fingerprint still matches and the remaining paths exactly match one applied repair.
- Do not call an active queue complete. Require the final `COMPLETE` line and proof file.

## Workflow

1. Read the target repository's instructions and current Git state.
2. Verify `git`, Python 3.11+, `clawpatch --version`, and `clawpatch-supervise --version`.
3. Check for another supervisor or ClawPatch process targeting the same repository.
4. Choose one start mode:
   - normal invocation to preserve and process the existing `.clawpatch` queue;
   - accept the interactive reset prompt only when the existing queue and project source are clean;
   - `--fresh` only as an explicit non-interactive clean-source reset;
   - `--resume-stopped` for the exact stopped checkpoint already on disk.
5. Run one repository at a time with an explicit absolute path, branch policy, push policy, and watchdog.
6. If it stops, preserve the printed finding, paths, checkpoint, and source exactly. Relaunch normally or with `--resume-stopped`; the supervisor can adopt a later applied ClawPatch repair only when its finding, base SHA, and complete source-path set match the stopped checkpoint boundary. If later committed work cleanly advances HEAD, it may retire only a verified obsolete recovery wrapper while preserving `.clawpatch` and continuing the queue.
7. On completion, verify the proof file, clean Git state, local HEAD, and remote SHA when pushes were enabled.

Linux or macOS:

```bash
clawpatch-supervise --repo /absolute/path/to/repo --branch current \
  --push each --timeout-minutes 15
```

Windows PowerShell:

```powershell
clawpatch-supervise --repo "C:\absolute\path\to\repo" --branch current `
  --push each --timeout-minutes 15
```

Resume only an exact stopped attempt:

```text
clawpatch-supervise --repo <absolute-path> --branch current --push each --timeout-minutes 15 --resume-stopped
```

Find the external checkpoint and proof directory:

```text
clawpatch-supervise --repo <absolute-path> --print-state-path
```

## Output

Human-facing phase banners are intentionally blunt, profane, and emoji-heavy. Exact commands,
finding IDs, paths, commits, errors, JSON, exit classes, and completion proof stay unchanged.

Return:

- repository and branch;
- supervisor and ClawPatch versions;
- fresh or resumed mode;
- current finding and phase, or final `COMPLETE` result;
- exact stopped paths and exit class when incomplete;
- proof path, clean/dirty Git state, local SHA, and remote SHA when complete.

## Anti-patterns

- Do not replace the command-owned queue with a report-derived loop.
- Do not run `clawpatch next` to get around a stopped finding.
- Do not blindly rerun the same fix against an unchanged source tree. Open and uncertain revalidation first use the bounded writable/trusted-host ladder; a clean checkpointed repair gets at most two evidence-informed same-finding attempts, while further repair continuation requires a genuinely changed exact tree.
- Do not reset an existing open queue. Default invocation preserves it. If `fix` exits `6` after source progress, the supervisor must checkpoint and revalidate that repair before another fix.
- Do not call completion unverifiable: successful completion retains `.clawpatch`, and `clawpatch status --json` must still work afterward.
- Do not commit unrelated or pre-existing changes.
- Do not run ClawPatch against Git submodule contents owned by third parties; fresh supervisor runs exclude Gitlinks automatically.
- Do not claim Windows or Linux support from source inspection alone; use the repository's cross-platform test results.

## Proof

Project and install instructions: https://github.com/uncmatteth/clawpatch-supervise

ClawHub page: https://clawhub.ai/uncmatteth/skills/clawpatch-supervise

The run is complete only when the supervisor exits `0`, writes a `status: COMPLETE` proof, reports zero open or uncertain findings after a fresh review generation, and leaves the repository in the expected Git state.
