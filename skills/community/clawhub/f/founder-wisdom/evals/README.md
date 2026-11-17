# Evals

`SKILL.md` is prose that steers a model. Prose drifts. This directory holds a small,
hand-checkable set of scenarios that pin down what the skill is supposed to do:
whether it triggers, which reference files it reads, which mode it picks, and
whether the output obeys the discipline in `SKILL.md`.

The directory has two halves. `check_scenarios.py` validates the data file's shape
and calls no model — stdlib only, no key, runs anywhere Python does.
`run_scenarios.py` executes the scenarios against a model and needs the `anthropic`
SDK plus an `ANTHROPIC_API_KEY`. `scenarios.yaml` is the source of truth for both,
and it is still a file you can read as documentation and run by hand.

## Files

- `scenarios.yaml` — the eval set. 38 scenarios plus five global invariants.
- `check_scenarios.py` — stdlib-only validator and pretty-printer. It checks the
  data file's shape, that every referenced path exists, and that `SKILL.md`'s
  frontmatter description is still inside its 950-character budget (the runtime
  ceiling is 1024; the gap is deliberate headroom, and the way to get it back is
  to move enumeration into the routing list, not to raise the budget). It does
  **not** call a model.
  It bundles a minimal YAML reader rather than taking a PyYAML dependency; its output
  on `scenarios.yaml` has been diffed against PyYAML and is identical.
- `run_scenarios.py` — the executable half. It imports `load` and `validate` from
  `check_scenarios.py` rather than reparsing the YAML, then drives each `prompt`
  through a harness that hands the model one skill and two tools, so triggering and
  file routing are read off the tool calls instead of inferred from the prose.
  Deterministic checks always run; `--judge` adds a second model call that grades the
  mode and the prose assertions. Needs the `anthropic` SDK and `ANTHROPIC_API_KEY`
  unless `--dry-run`.
- `results/` — committed output from judged runs. See "Committed results" below.

## Schema

Top level:

| Key | Meaning |
|---|---|
| `version` | Schema version. Currently `1`. |
| `global_invariants` | Plain-English checks that apply to every scenario where `should_trigger` is true. |
| `scenarios` | The list below. |

Each scenario:

| Key | Type | Meaning |
|---|---|---|
| `id` | string | Stable kebab-case identifier. Referenced in PR discussion. |
| `prompt` | string | Exactly what the user says. Verbatim — do not paraphrase when running. |
| `should_trigger` | bool | Whether the founder-wisdom skill should activate at all. |
| `expected_mode` | `direct` \| `socratic` \| `none` | `none` iff `should_trigger` is false. |
| `expected_files.must_include` | list | Reference files that must appear among those read. Never more than three. |
| `expected_files.must_not_include` | list | Reference files whose presence is a failure. |
| `assertions` | list | Plain-English checks on the response. |
| `rationale` | string | One line naming the `SKILL.md` rule the scenario protects. |

`expected_files` is deliberately tolerant. `SKILL.md` tells the model to read 2–3
files, so pinning an exact set would produce false failures. The pair of lists
expresses only what must be there and what must not be — anything else is free.
Where a plausible-but-secondary file exists, it is named in an assertion rather
than in either list.

The axiom count is tolerant for the same reason. `SKILL.md` asks for 3–7 and the
global invariant states that rule, but the deterministic check fails only above
nine. Across three judged runs the bolded-lead-in count centred near six with a
tail that crossed seven on roughly a third of triggering scenarios, and no
scenario exceeded seven in every run — so a hard stop at the stated ceiling
flagged a different handful each time without the skill having changed. The
invariant is the target; the check is there to catch a dump, not to police the
last two.

## Running against a model

`run_scenarios.py` executes the scenarios instead of printing them. Install the SDK
(`pip install anthropic`) and set `ANTHROPIC_API_KEY`. `--dry-run` needs neither and
prints the plan, which is enough to catch a broken runner in CI.

### How the harness models activation

The model gets the `description:` line from `SKILL.md`'s frontmatter and exactly two
client-side tools: `load_skill`, which returns the skill body, and `read_reference`,
which returns one file under `references/`. Nothing else is in context.

So "did the skill trigger" is a `load_skill` call, and "which reference files were
read" is the list of `read_reference` paths — both observed facts about the
transcript rather than judgments about the answer, which is the entire reason for
the harness. It is an approximation of a real skill runtime, not the runtime itself:
a model that would have behaved differently with a full toolset is not tested here.
`read_reference` refuses any path that escapes `references/`.

### What runs deterministically

These need no judge and never disagree with themselves:

| Check | Rule |
|---|---|
| Trigger | `load_skill` is called iff `should_trigger` is true. |
| Stray reads | A non-triggering scenario must read no reference file. |
| `must_include` | Every named file appears among the reads. |
| `must_not_include` | No named file appears. |
| File budget | At most three reference files. |
| Axiom count | 3–7 bolded axiom lead-ins, skipped in Socratic mode. |

The file budget is an upper bound only. `SKILL.md` asks for 2–3 files when a question
spans domains, so a correct single-domain answer reads one — the lower half of that
invariant goes to the judge, which can read the prompt and tell the difference.

### What the judge checks

`--judge` adds a second model call per scenario. It grades a fixed claim list: the
scenario's `expected_mode` restated as a claim, its `assertions`, and — for
triggering scenarios — the `global_invariants` the deterministic checks don't
already cover. Each claim gets a pass/fail and a one-sentence reason; silence or
ambiguity is a fail. The judge echoes each claim back, and verdicts are matched by
that echo rather than by position, so a dropped verdict fails its own claim instead
of shifting every later one onto the wrong claim.

### Flags

| Flag | Effect |
|---|---|
| `--dry-run` | Print the plan. No SDK, no key, no API call. |
| `--judge` | Add the judged pass. Roughly doubles the calls. |
| `--id ID` | Run one scenario. Repeatable. |
| `--limit N` | Run at most the first N. |
| `--deadline MINUTES` | Stop starting new scenarios and report what ran. |
| `--json PATH` | Write the full result set, rewritten after every scenario. |
| `--model` / `--judge-model` | Override either model. |
| `--threshold F` | Judged pass rate required. Default 0.8. |
| `-v` | Print every response in full. |

Exit codes: `0` clean; `1` a scenario failed on behavior, or the judged score is
below the threshold; `2` bad usage, or `scenarios.yaml` / `SKILL.md` could not be
used; `3` nothing failed on behavior but the harness errored or ran out of time.
The `3` earns its own code — a rate-limit burst is not a skill regression and
shouldn't be read as one.

### Threshold semantics

`--threshold` is a floor on the judged claims only: the fraction of graded claims
that passed, pooled across every scenario that ran, not a per-scenario score and not
a count of scenarios. Deterministic failures are never in that fraction and never
excused by it — one behavioral failure exits `1` however high the score. The default
0.8 is tolerance for judge noise on prose claims, not permission to miss one claim in
five.

### The axiom count is a heuristic

Nothing here knows what an axiom is. The counter matches the corpus's format instead:
a bolded run opening a line or paragraph, followed by prose on the same line. Bolded
labels ending in a colon are dropped, because the corpus writes section labels that
way itself and counting them would fail a well-formed answer. Against `references/`,
600 of the 614 line-start bold runs survive and all 14 dropped are labels.

That makes it a format check wearing a content check's name. A response that surfaces
five real axioms in unbolded prose counts zero and fails; one that bolds five
throwaway lines counts five and passes. It also can't tell a restated axiom from a
new one, or a good axiom from a wrong one. Read a bare axiom-count failure as "go
look at the response" rather than as a verdict — `-v` prints it.

### Committed results

`evals/results/` holds the output of judged runs, committed. A judged run against
changed routing prose then produces a diff you can read in review: which scenarios
moved, which claims the judge changed its mind about, which files a scenario started
reading instead. Drift shows up in the diff rather than in a terminal nobody kept.

## Running by hand

Running by hand is not what the runner replaced. The runner checks what a machine can
check — triggering, routing, counts, and a judge's read of the claims. Whether the
axiom it surfaced was the *right* one, whether a Socratic question actually lands,
whether the answer would help a founder: those are still yours, and so is checking
the skill in the product people use rather than in a harness that approximates it.

1. `python3 evals/check_scenarios.py` — validates the file and prints every scenario.
2. Install the skill (see the repo README) in a fresh conversation. One scenario
   per conversation: state carries, and a scenario that follows another will
   inherit its mode.
3. Paste the `prompt` verbatim. Nothing else.
4. Score it:
   - **Trigger** — did the skill activate? For Claude Code, the tool calls show
     which `references/*.md` were read. In Claude.ai, ask "which files did you
     consult?" *after* scoring the response, never before.
   - **Files** — every `must_include` present, no `must_not_include` present.
   - **Mode** — direct means axioms; Socratic means one question and a stop.
   - **Assertions** — each one a yes/no.
   - **Global invariants** — apply to every triggering scenario.
5. A scenario fails if any single check fails. Record which one; "it failed" is
   not actionable, "it read `fundraising.md` instead of `capital-valuation.md`" is.

A full pass by hand is a bit over an hour, and is warranted when `SKILL.md`
routing prose changes; a spot check of the affected scenarios is enough for
anything smaller.

## Running with skill-creator

Anthropic's `skill-creator` skill has eval tooling that runs scenarios against a
skill and grades the transcript. It reads an `evals/evals.json` whose entries carry
`id`, `prompt`, `expected_output`, and `expectations`. Translate as follows:

- `prompt` → `prompt`, verbatim.
- `id` → a short note in `expected_output`; skill-creator's `id` is an integer, so
  number the entries and keep our kebab-case id as the human label.
- `should_trigger` → `expected_output` states whether the skill should engage at all.
  The negatives matter as much as the positives — a skill that fires on everything
  scores well on positives alone.
- `assertions` + the matching `global_invariants` → `expectations`, one string each.
- `expected_files` → an `expectations` entry of the form "read `references/X.md`;
  did not read `references/Y.md`." Note that skill-creator's own `files` key means
  *input* files, not the reference files read — do not map onto it.

Keep `scenarios.yaml` as the source of truth and generate the tool's input from it.
Do not fork the expectations into a second file.

## Adding a scenario

1. It must protect a rule `SKILL.md` actually states. Quote or paraphrase that rule
   in `rationale`.
2. If `SKILL.md` is ambiguous on the point, say so in the `rationale` rather than
   inventing a rule. Four scenarios already do this — `negative-boundary-mixed-regulatory`
   (mixed in-scope/out-of-scope prompts), `routing-delegation-at-5` (SKILL.md says
   "prefer," which is softer than the `must_not_include` encoding),
   `reassurance-still-triggers` (the mode call), and
   `routing-non-dilutive-revenue-share` (a revenue-based offer is both
   "debt-vs-equity" and "non-dilutive capital," which SKILL.md routes to
   different files).
3. Keep `must_include` to the one or two files the routing genuinely requires.
4. Stay inside the YAML subset the validator's bundled reader handles: two-space
   indent, `key: value`, `[a, b]` flow lists, block sequences, and `>-` folded
   scalars. Avoid anchors, inline comments, and multi-line flow collections.
5. Re-run `check_scenarios.py`.

## Known ambiguities and gaps

These are recorded so they aren't rediscovered every time:

- **"Reassurance" is an output rule, not a trigger rule.** `SKILL.md`'s
  "What this skill is not for" lists reassurance, but the entry itself says the
  skill "should still surface the axiom that pushes back." `reassurance-still-triggers`
  encodes the trigger as **true**.
- **Mixed-scope prompts are unspecified.** A prompt with an in-scope half and an
  out-of-scope half (`negative-boundary-mixed-regulatory`) has no rule in `SKILL.md`.
- **"Prefer" is soft.** The `management-execution.md` stage note says to prefer
  `time-energy.md` and `hiring.md` below ~10 people. `routing-delegation-at-5`
  reads that strictly.
- **Coverage gap at 200+.** `hiring.md`'s stage tags are all Seed–Series A, so
  `output-stage-match-late` tests stage-awareness against thin material.
- **`mode-direct-factual` is unverified since its corpus fix.** The scenario asserts
  the option-pool percentage carries a vintage tag, which is what `SKILL.md`'s
  "Output style" requires. It used to fail on the corpus rather than on `SKILL.md`:
  the 10–15% pool-refresh figure in `capital-valuation.md` carried no
  `*[bench YYYY-MM]*` tag, so a model reading it faithfully had nothing to cite. The
  figure is now tagged, which removes the known cause — it does not establish a pass,
  because no run has been made since. Re-run the scenario before treating it as green.
