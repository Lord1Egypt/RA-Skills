# Documentation governance framework — distilled from a large protocol project

The source project kept iterating for the better part of a year with twenty-plus documentation directories, hundreds of ADRs, and dozens of rules, and its documentation system didn't fall apart.
What held it together wasn't discipline; it was seven decidable components. `governance.py audit` checks these seven one by one; `init` installs the missing ones.

Every criterion is written as "a shape a machine can check" — components that can't be checked aren't listed, because listing them would just be an opinion.

The "real cases" below come from the source project and from two mid-sized product repos that later installed this system; project names, dates, and people's names are removed,
numbers are kept as-is (they don't point to anyone).

---

## G1 Source-of-truth layering (who is authoritative for what)

**How the source project does it**: four layers — L1 protocol spec (definitions/formulas/§ numbering), L2 vision roadmap (version themes),
L3 implementation roadmap (priorities), L4 codebase (current state). Each layer states "what to look up here" and "what must be obeyed".

**Why it comes first**: without this layer, the other six have nothing to stand on — if "whose word is final" is undecided, no conflict can be resolved.

**Don't pre-model the number of layers; they grow on their own.** "Deliberately not ported" once said "four-layer modeling not ported, two layers is enough for a small project" —
item-by-item verification overturned that: a mid-sized product repo now **has all four layers**, and they roughly line up with the source project's
(L1 spec → `SPEC.md` + `spec/`, L2 strategy → `PRD`, L3 implementation reference → the `PLAN.md` TODO queue, L4 code truth → the code itself).
More importantly, **L4 has already been ported**: the source project's rule for L4 is "the 'current status' column in a Plan must match the code",
and that is exactly what the `contract` mode does.

Every layer was forced into existence by a specific incident; none was pre-built from a template:
the tech/product split came from a PRD/SPEC conflict; the code layer came from measuring that two endpoints declared in the spec didn't exist in the code.
**So the half-sentence "the number of layers is an outcome, not a goal" holds; the half-sentence "two layers is enough" was a guess at the time, and it has been falsified — a guess shouldn't be written down as a reason.**

**Criteria** (two sub-items):
- The repo has a document that explicitly declares "information of type X is authoritative in document Y"
  (English keywords: “source of truth”, “authoritative”, “takes precedence”; the Chinese equivalents are recognized too)
- **`contract_checks` is configured**, meaning something actually cross-checks the docs against the code

> **The second item was added later.** Declaring "the code is the technical source of truth" with nothing checking it makes the declaration an empty sentence.
> Measured: a product repo's `docs/spec/api.md` declared `/api/v1/help/ask`, which doesn't exist in the code at all (the real endpoint is called `chat`).
> The source project has a prose rule "architecture tables must mark implementation status"; **`contract` is its machine version: unmarked and mismatched goes straight to red.**

**What goes wrong without it**: real case — **the PRD doesn't reference the SPEC** (the reverse direction has 2 references; it's one-way),
the PRD **went 34 days untouched**, and its tech stack section was stuck on an old description, because "whose word is final on technical matters" was never written down.

---

## G2 Decision record system (ADR)

**How the source project does it**: `adr/NNN-slug.md`, frontmatter requires `id/title/domain/visibility/status/date`,
status is limited to `draft|accepted|deprecated|superseded`, plus an index README.

**Criteria** (four items scored separately):
- A decision directory exists and its files are numbered `NNN-slug.md` (an `ADR-` prefix is accepted: a repository's `ADR-0017-xxx.md` files were once missed as a batch — the prefix is only surface spelling)
- Numbering is sequential with no gaps
- An index exists, and index and directory fully cover each other (= `check index`)
- **Uses the standard frontmatter**: required `id/title/domain/visibility/status/date`,
  `status ∈ {draft, accepted, deprecated, superseded}`, `visibility ∈ {public, internal, confidential}`,
  optional `type ∈ {decision, memo, postmortem, contrastive-analysis}` and relationship fields
  `supersedes / superseded_by / supersedes_partially / derives_from / extends / related`
- **`domain` has an allowlist configured**: valid values vary by project and live in `adr_domains` in `.doc-governance.json`.
  Not configured = this cell wasn't checked, and `domain: prd` (missing an o) stays silent all the way through
- Relationship field names may not be near-miss spellings (`derives` / `superceded_by` / `related_to` …) —
  mismatched key names are silently ignored, and "declared" and "not declared" look identical to the machine
- `status: superseded` must state `superseded_by`; the first heading in the body must be `# ADR-NNNN` with a number matching the filename

> **The settled principle: no longer "consistent conventions are enough", but "use this one set".**
> The earlier position was "each project just needs internally consistent conventions"; that was corrected: a solo developer runs multiple projects,
> and the cost of non-standardization is "a separate mental model per project" — that is what really eats attention.
> This field set has been battle-tested on hundreds of ADRs; adopting it directly is less hassle than every project inventing its own.
>
> **Prose isn't lost**: frontmatter holds what machines need to read (enums, relationships); details stay in blockquotes in the body.

**Validate the index, don't generate it** (this is this skill's own design choice, not a trade-off ported from the source project):
`check index` only verifies that "decisions in the directory" and "rows in the index" fully cover each other; it doesn't generate index content.
The reason was found by looking — **both the source project's ADR index of several hundred lines and the product repo's 8-line one are made of hand-written rich summaries**
(one row lists the trigger, four resolutions, the cascade, and review corrections; another lists all five layers of guardrails).
None of that can be generated: a generator can only emit the `title` from frontmatter, and generating would throw away all the judgment.

**What goes wrong without it**: status fields become free-form and nobody knows which decisions are still in force; a decision written but not indexed = nobody can find it.

---

## G3 Cascade discipline (which documents a decision lands in)

**How the source project does it**: after writing an ADR, four steps — ① write the file ② update the index ③ update the roadmap ④ cascade the memo routes
(grep each target file to confirm `ADR-NNN` was written into it). This rule was promoted from "load on demand" to "always on",
because the same lesson was learned three times.

**Criteria**: the decision file has a cascade section (`## Cascade memo`, `## Cascade notes`, `## Propagation`, `## Downstream updates`, or the Chinese equivalents); ✅ entries in that section carry verifiable paths.

**What goes wrong without it**: in the source project, all three times it took the user asking follow-up questions to discover the routes hadn't landed;
in the product repo, the first drafts of two ADRs left this section out, three PRD conflicts sat for a day, and after it was added, PLAN.md and SPEC were missed again.

---

## G4 Planning system (what is being done now, how far along)

**How the source project does it**: plan-writing discipline + Spec Gate (a spec review before writing a plan) + § references must be verified with grep.

**Criteria**: a plan directory exists; plan files (starting with `PLAN-` or `TASK-`, where `D` marks finished) have a status field — the status line is `Status:` or a `| Status |` table row, **not** a bare Chinese 状态： line (often ordinary prose; considered and rejected); there is an index answering "what goes first";
**there is no second, abandoned answer** — if a scaffold ledger (`.autopilot/`, `PROGRESS_SNAPSHOT.md`, and the like)
is more than 30 days behind the repo's latest commit, then "what are we doing now" has two answers and one of them has rotted.
The list and threshold are configured in `scaffold_ledgers` / `scaffold_stale_days`; set it to `[]` to turn it off.

**What goes wrong without it**: the product repo's planning layer wasn't missing, it had **stalled** — the plan directory and its index README had existed for a long time,
but the plan files went **15 days without updates while main got 366 commits**. The plans were there; nobody came back to update them, so "what should we do now" couldn't be looked up.

> ⚠️ **This paragraph itself was once wrong.** The first version said "the directory wasn't created until very late" —
> it used `git log --diff-filter=A -1` to get the "earliest", but that command returns the **most recent** one.
> A new error introduced while fixing an old one, on the same day.

**Same repo, second answer**: four root entry files generated by an AI collaboration scaffold overlapped in responsibility with the project's own four family READMEs;
checked pair by pair, **all four pairs had drifted**; two of them weren't "stale" but **pointed the wrong way**
— the doc said "status is authoritative in `PLAN.md`", and `PLAN.md` was exactly the one that had stopped being updated; following that rule would change the correct table back to the wrong one.
Removing it took five PRs.

**This item was added to the criteria because nothing could see it**: that time too, it surfaced only because the owner happened to ask.
Measured: 10 projects on the same machine have the same scaffold installed, and 3 of them have ledgers **one to two months behind** — worse than the repo that first forced its removal;
two others have ledgers dated the same day as their commits, healthy, and they **shouldn't be reported and indeed aren't**.

---

## G5 Checkpoints bound to actions (when checks are mandatory)

**How the source project does it**: three checkpoints —
CP-1 before writing a new plan, a **reverse** Code→Spec audit; CP-2 before a release, a forward Spec→Plan→Code verification;
CP-3 after a bulk rename, a broken-link scan. **Checkpoints are bound to actions, not to the calendar.**

**Criteria** (two sub-items):
- Repo docs (CLAUDE.md / AGENTS.md / README) state "before doing X, run Y"
- **Every checkpoint has a device bound to it** — pre-commit (at commit time) / CI (every PR) /
  Claude Code hook (before writing a new plan, after changing a decision) / Cursor rule.
  "Before writing a new plan" is mandatory; without it this item is judged partial

> **The criteria were revised.** Originally only the first item was checked — that checked the sticky note, not the device.
> "Bind the trigger line to an automatic trigger on the spot; a trigger line written only in docs, waiting for someone to remember it, is as good as not set" — G5 itself made exactly this mistake.
> After the change, one product repo's G5 dropped from ✅ to ⚠️, which was its real state.

**How the devices are installed**: `init` places two scripts in `.claude/hooks/` and registers them in the project's
`.claude/settings.json` (committed to git, same reasoning as `.githooks/`) —
`PreToolUse(Write)` runs the full check when a new `PLAN-*.md` / `TASK-*.md` is created and hard-blocks with `exit 2` on red;
`PostToolUse(Write|Edit)` runs `cascade refs` after a decision record is edited and reports on the spot.
**Cursor projects have to write an equivalent `.mdc` rule themselves** — no code was written for that path, so it was never verified, and we don't pretend it can be installed.

**What goes wrong without it**: CI can't catch "a new plan written on top of an outdated spec" — the new plan itself is compliant.
Only a reverse audit before starting work can catch it; and a reverse audit without a device bound to it is just a sticky note.
Same pattern elsewhere: after a credential-printing incident, what got added was a **text rule** hard-coded to "API responses";
the second time, a local config file was read, the rule didn't match and didn't fire, and credentials had to be rotated again; only switching to mechanical blocking based on the shape of the action worked.

---

## G6 Gates (not relying on people remembering)

**How the source project does it**: three pre-commit gates (ADR schema / table integrity / broken links), with the hook itself under version control
(`.githooks/pre-commit`; `.git/hooks` is just a forwarding shell, and it refuses the commit if the file is missing).

**Criteria**:
- CI has a docs-related gate
- **Local commits have one too** (pre-commit hook)

**Why both**: measured on a product repo, **36 of the last 80 commits were direct pushes to main** (no PR),
and CI never ran once on those commits — "having CI is enough" is false; it depends on whether the team goes through PRs.

> ⚠️ **This is a sliding-window number, and it changes on its own.** Measured on the same repo at each point across the last 100 commits,
> the number of direct pushes in an 80-commit window floats between **33 and 44**. So any citation of it must carry a measurement date —
> an undated number is wrong a few days later, and nothing will tell you it's wrong.

---

## G7 Incident traceability (every rule states the failure it guards against)

**How the source project does it**: the comments on every gate and every rule state the source incident and its date;
there is also a dedicated, maintained series of collaboration meta-lessons, twenty-plus entries, each with its origin.

**Criteria**: dates + incident descriptions appear in gate scripts / rule docs.

**Why this one looks least like a mechanism but matters most**: specs get bypassed as bureaucracy; incidents don't.
Nobody turns off a check that says "the table corruption incident of such-and-such month and year".

---

## Deliberately not ported

| Source project has | Why it's not ported |
|---|---|
| Public content redaction check | Only needed when there are public releases, **but the trigger line is already bound to a device**: if any ADR is marked `visibility: public` and the project hasn't configured `public_content_scan`, `check refs` goes red on the spot. Zero cost when there are no public ADRs |

**General principle**: install these seven as needed; it's not a bundle. `audit` reports what's missing and what goes wrong without it,
and whether to install is the project's call — **pre-building mechanisms for extensibility is exactly the disease this framework exists to stop**.

> **This table originally had three rows; after item-by-item verification only one is left.**
> "Auto-generated index" was fabricated wholesale — the source project has no generated index, so there was nothing to port or not port (the real design choice moved into G2).
> "Four-layer source-of-truth modeling" didn't hold either — the product repo has all four layers, and L4 has already been ported by `contract` (moved into G1).
> Only redaction was genuinely not ported, and its reason had a precondition ("there are no public releases yet");
> a precondition written in a doc never gets rechecked by anyone, so a device was bound to it.
>
> **Every decision of the form "we're not doing it because X doesn't exist yet" should come with a question: on the day X appears, who tells you?**
> **Another line worth just as much: don't write a guess down as a reason.** "Two layers is enough for a small project" was a prediction; from the day it was written, nobody came back to verify it,
> until someone pointed at it and asked "why isn't this ported?"
