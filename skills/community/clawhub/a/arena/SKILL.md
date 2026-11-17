---
name: arena
description: Give independent Codex agents the same substantial task, compare their solutions against a clear rubric, and deliver one verified result. Use when the user asks to "arena" a task or compare competing approaches. Checks for updates when invoked.
metadata:
  openclaw:
    requires:
      bins:
        - bash
        - git
    homepage: https://github.com/yagel-yosef/arena-skill
---

# Arena

Use Codex's available collaboration tools to produce independent attempts at one task, then deliver one coherent result. Follow the user's scope and the current session's limits on delegation, tools, models, writes, and approvals.

## Update on invocation

Before starting Arena work, run `bash <directory containing this SKILL.md>/scripts/update.sh` once. The script pulls the public `main` branch of `yagel-yosef/arena-skill` into this installed skill. If the revision changes, reopen this `SKILL.md` from disk and use the new instructions for the current task. Tell the user which revision was installed. If the update fails, tell the user and continue with the installed revision. Do not run the updater again while handling the same request.

## Frame

1. Define the deliverable and shared facts every candidate needs. Give all candidates the same task and acceptance criteria. Add only a distinct output location to each brief.
2. Write 3–6 observable rubric criteria for choosing the final result. Include task-specific correctness and maintainability where relevant. Keep the rubric with the coordinator; candidates should solve the task without seeing each other's work.
3. Use the user's requested number of candidates when feasible; otherwise default to three. Respect the available concurrency slots and the cost or time appropriate to the task. Tell the user if a limit materially reduces the requested comparison.
4. Choose separate writable locations. For repository changes, prefer separate git worktrees when practical. Otherwise give each candidate a unique temporary directory and require patches or artifacts there. Candidates may read common source files, but must not edit a shared working tree or external destination.

## Generate

Spawn candidates concurrently with `collaboration.spawn_agent` when available and authorized by the current instructions. Use names such as `arena_1`, `arena_2`, and `arena_3`. Do not assume named roles or model families exist; use the session's default model unless the user or higher-priority instructions request otherwise. Run in waves if the concurrency limit is smaller than the requested candidate count.

Each self-contained brief must specify the deliverable, shared grounding paths or facts, candidate-owned writable path, acceptance criteria, verification to run, forbidden scope, and a short report format. Ask for the artifact plus a rationale that identifies meaningful alternatives considered and rejected. Tell candidates not to delegate further unless the user requested nested delegation. Wait until all candidate writes are complete. A candidate without a usable artifact is a dropout; record it and continue with the available results.

If parallel agents are unavailable or prohibited, do not claim an arena ran. Explain the capability limit and either produce a single result or ask the user for the needed mode, according to the task.

## Judge and choose

After candidate outputs are complete, send a separate read-only judge agent the rubric and paths to every candidate when an agent slot is available. It must score each criterion with evidence and recommend a base. The judge must not edit candidates or the destination. Read every candidate's artifact and rationale yourself while the judge works. If a judge agent is unavailable, score the candidates yourself and disclose that the independent review was skipped.

Compare criterion by criterion. Choose the base that best satisfies the task and is easiest to extend safely. If you disagree with the judge, inspect the evidence and explain the decision. If candidates diverge because the brief was ambiguous, resolve the ambiguity using the user's instructions and available evidence; rerun only when that is necessary to deliver a sound result.

## Combine and verify

Integrate the base into the intended destination. Review each other candidate once more for specific improvements, then adapt useful ideas by hand so the result remains coherent. Do not merge whole candidates mechanically or use a majority vote in place of checking correctness. Keep externally mutating actions with the coordinator and within existing authorization.

Verify the integrated result against the original acceptance criteria, using relevant tests, inspection, or live checks. Candidate checks and the judge's recommendation are evidence, not verification of the integrated result. Fix failures and rerun the checks that cover them.

Deliver one final artifact and a compact synthesis note. Name the base, useful contributions from other candidates, significant rejected ideas and why, dropouts, any judge disagreement, and the final verification result. Put the note beside the artifact when that fits the task; otherwise include it in the final response. Be accurate about any phase that could not run.
