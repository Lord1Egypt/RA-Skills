# Memory and Evaluation Operations

## What to remember and when to adopt it

| Type | Memory content | Later use |
| --- | --- | --- |
| Artifact | Path or source, purpose, version, and scope | Open and check the underlying work, such as study materials, an evidence table, analysis code, or a reusable rubric. |
| Fact | Verified fact, source location, applicability, and recheck trigger | Cite or recheck it when the task matches. |
| Decision | User- or project-confirmed decision, rationale, and scope | Carry it forward within the same project and update it when instructions change. |
| Hypothesis | Research question, candidate mechanism, expected pattern, and distinguishing evidence | Retrieve as an untested idea and preserve its status. |
| Practice | A strategy that worked once or might work, when to use it, and counterexamples | Try it provisionally. Run a paired evaluation before changing default behavior. |
| Observation | Event, feedback, error or success, evidence location, and uncertainty | Trace the origin of a practice, consolidate lessons, or supply a counterexample. |

## Files and commands

Prefer memory that the current host actually reads. When file-based storage is useful, initialize it in an authorized project with the included utility. Requires Python 3.9 or later.

```bash
python3 EVOLVE --project PROJECT init
python3 EVOLVE --project PROJECT capture ENTRY.json
python3 EVOLVE --project PROJECT recall "rubric scoring"
python3 EVOLVE --project PROJECT recall "offloading" --include-unverified
python3 EVOLVE --project PROJECT stage candidate.md
python3 EVOLVE --project PROJECT promote TRIAL_ID results.json
python3 EVOLVE --project PROJECT rollback
```

- Replace `EVOLVE` with the bundled script path and `PROJECT` with the project path. `init` also accepts an existing memory file as the initial durable version.
- `capture` writes one entry to `.agent-evolution/entries/` for retrieval and consolidation. Submitting identical content returns the same entry. To replace a stale entry, set `supersedes` to its ID in the new record.
- `recall` accepts space-separated keywords and returns a small set ranked by matching terms and record date. `--scope` limits results to an exact recorded scope. Default results include reusable artifacts, verified facts, and confirmed decisions. Add `--include-unverified` for hypotheses, provisional practices, and observations. If an older `episodes.md` exists, read it as needed and preserve its records.
- `.agent-evolution/MEMORY.md` is versioned durable memory. Keep verified general knowledge, indexes, or validated rules brief. Point to relevant entries and artifacts from it. Use `capture` for routine recording and retrieve durable memory as needed.
- `stage` saves the current durable memory and the candidate under `.agent-evolution/trials/TRIAL_ID/`. When authorized to change future behavior, use `promote` to check the evaluation and adopt the candidate. Use `rollback` or `--to VERSION` to restore a saved revision. The script checks record structure, hashes, and scores. The operator checks the evidence and results.

### Example entry

```json
{
  "kind": "artifact",
  "title": "Blinded scoring plan for a hypothesis-generation task",
  "summary": "Saved rubrics for two parallel tasks and a process for resolving rating disagreements.",
  "scope": "Undergraduate pilot in the current project",
  "source": "analysis/ratings/rubric-v2.md",
  "trigger": "When reusing the tasks or training raters",
  "review_when": "When task materials or scoring dimensions change"
}
```

Choose `artifact`, `fact`, `decision`, `hypothesis`, `practice`, or `observation` for `kind`. `title`, `summary`, `scope`, and `source` are required text fields. `trigger`, `review_when`, and `supersedes` are optional. Record an unverified fact as an `observation`. Use `fact` or `decision` when the evidence and authorization support that status. Keep each record brief.

## Paired evaluation of durable practices

1. Compare baseline and candidate across sessions with comparable tasks, models, tools, and materials. Hold out examples used for neither drafting nor tuning. Check existing behavior that should be preserved.
2. Define the meaning of scores from 0 to 1 beforehand. Match the evaluation JSON to the manifest using `trial`, `baseline_sha256`, and `candidate_sha256`. Each item in `cases` includes `id`, `kind` (`holdout` or `regression`), `criterion`, `before`, `after`, `baseline_evidence`, and `candidate_evidence`.
3. Adopt the standing rule after at least one held-out example improves and existing checks show no regression. If the evidence is unstable, continue testing or retain the practice as conditional experience. Confirm retrieval and behavior in a new session.

## Research example

While reading a paper, develop a comparison that distinguishes reliance on external information from knowledge integration. Capture the design as an artifact immediately and save the two explanations as candidate hypotheses. The closing review may suggest that listing each mechanism's predictions before choosing the manipulation reduced rework. Save this as a provisional practice. Retrieve the prediction table on the next mechanism-comparison task. Promote the practice to the project's procedural memory if new tasks support it and simple tasks incur no extra burden.
