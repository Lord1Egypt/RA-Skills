# Incident list — the failure behind every check

This list is the soul of the skill. Every check mode in `governance.py` maps to at least one real incident below.
Of the 181 tests in `test_governance.py`, **141** name the incident they guard against in their docstring
(the other 37 are positive cases that verify what shouldn't be reported isn't, with no incident to name).
**Whether anyone reads SKILL.md doesn't matter: run the tests once and the “why” gets restated 141 times.**

After installing in a new project, add your own under § “Project-specific additions” — the more incidents, the more accurate this ruler.

> **About sources**: the incidents below come from three real repos — **the source project** (the large protocol project this framework was distilled from),
> **Product repo A**, and **Product repo B** (two mid-sized products that later installed this system). Project names, dates, people's names, and business details are removed;
> numbers are kept as-is, because magnitudes like "8 rows", "34 days", and "36 direct pushes" are themselves the argument.

## Master principle (the core diagnosis from a real project postmortem)

> What the system actually does and what the team believes it does have diverged, **and no measurement anywhere lets anyone see the divergence**; every fix starts by making it visible.

Every mode that follows is a concrete instance of that sentence.

## The nine modes and their source incidents

### `pending` — the X in "change it after X" happened long ago, and nobody came back to change it

| Project | Incident |
|---|---|
| Product repo A | A PRD's "rewrite mapping table" had **8 rows** saying "rewrite once … is confirmed" (7 of them verbatim "rewrite once Plan B is confirmed"). Plan B had long since been confirmed and completed; **the condition was met and nobody touched it for six weeks**. The top of the doc still said "Plan B Spec current status is draft" |
| Product repo B | A doc said "the next step is designing the solution with the partner" — the solution had long since been designed and implemented |

**Why a machine can check it**: "after X" is a recognizable sentence pattern; with a date you can compute how long it has been hanging. It can't check whether X has happened, but **anything hanging for more than 30 days deserves someone taking a look**.

### `cascade` — a decision became an ADR, but the documents that should follow didn't change

| Project | Incident |
|---|---|
| Product repo A | After two ADRs landed, three places in the PRD (product positioning, two risk tables) directly contradicted the decisions and **stayed that way for a day** — neither ADR had a cascade memo |
| Product repo A | After the cascade memo was added, **`docs/PLAN.md` was missed again** (the project's own rule says it is the single source of truth), along with SPEC §6.4 |
| Product repo A | Two deploy targets, only half updated — "the code is on main but production doesn't have the feature". The lesson was written into `BRIEFING.md`, but **without a date, and the commit can't be located in git**, so it can't be verified; that is stated plainly |
| The source project | Three authors **each committed an ADR but forgot to add the Recent row to the index**; an automatic backstop was added the next day that exits with code 1 on a missing row |
| Product repo A | A cascade memo said "✅ content moved into `[archive/old/](…)`", with the link pointing at a **directory**, not a file — `check_cascade` called `read_text()` directly, raised `IsADirectoryError`, and **the whole check crashed; not a single mode produced any result**. A crash is worse than a false positive: a false positive can still be read, a crash stops every other mode from running. It now reports one finding: "cannot verify, point to a specific file" |

**Why a machine can check it**: files marked ✅ in a cascade memo must actually exist and mention the ADR; items marked ⏸ must state a reason.

### `status` — two copies of the same fact, and one quietly goes stale

| Project | Incident |
|---|---|
| Product repo B | The admin repo's database schema was a hand-maintained mirror of the product repo's: the product repo had changed a field to nullable + `SetNull`, while the admin repo still said non-null + `Cascade`. **The consequence wasn't an error, it was misleading judgment** — the UI sorted a class of data in the wrong order because of it, complete with a confident, wrong comment |
| Product repo A | Three plan statuses were badly stale: one said "feature not started" while 3 backend files + 6 Android files had long been live; another said "scope confirmed only" while 7 files in the relevant layer were already running |
| Product repo A | The goal ledger's `execution_sequence` still contained 3 completed goals |
| Product repo A | Plan files went **15 days without updates while main got 366 commits**. The plans were there, the index was there; nobody came back to update them |
| Product repo A | A new controlled status word `blocked` was added, but `STATUS_LIVE_RE` wasn't extended — a plan changed from `plan_drafted_pending_owner_approval` (contains "pending", so recognized as a "live status") to `blocked` (contains no recognized word) and **silently dropped out of the staleness check**. The most stuck status became the one no longer watched — extending the status vocabulary must come with extending the recognition regex; they are one thing |

**Why a machine can check it**: if a plan's Status says "in progress" but the file hasn't been touched in 45 days, one of the two is false.

### `refs` / `links` — references pointing at things that don't exist

| Project | Incident |
|---|---|
| The source project | A bulk migration was "declared fixed"; **34 broken links sat for two days** before a manual audit found them |
| Product repo A | A docs cleanup turned up 10 broken links, 7 of them with the wrong path depth; **nobody had ever checked** |
| Product repo A | One commit renamed **13** plans; the first regex pass missed bare references without `.md`, and **the broken-link scan caught them on the spot** |

### `contract` — endpoints/fields the docs declare that simply don't exist in the code

| Project | Incident |
|---|---|
| Product repo A | The first time `contract` ran on a real repo, it caught two spec/code divergences: `docs/spec/api.md` said `/api/v1/help/ask` (actually `/chat`), and 5 places across three docs said `item-details/{id}.json` (actually `items/{id}.json`). **This kind of divergence has no symptoms** — the docs read perfectly normally; it only shows up when compared item by item against the code |
| Product repo A | The same day, this mode **itself** manufactured a falsehood: the `code_claim` regex missed `PATCH`, so the real `PATCH /api/admin/items/:id` was judged "not in the code", and on that basis "retired" was written into the spec — pure fabrication. The mode skips anything marked "retired", so the check turned green. **A checker bug, via the legitimate escape hatch of "honest labeling", became a false sentence in the docs**. Fixing it doesn't stop the whole class: the machine can't tell a true "retired" from a false one, so the warning was written into the error message itself — grep it yourself before labeling |

**Why a machine can check it**: endpoints written as `` `/api/...` `` in docs and object keys like `{id}.json` are extractable literals; the code side is extractable too. Intersect the two sides; whatever is missing is either the docs bragging, or code that was deleted with nobody coming back to update the docs.

### Self-check — the checking mechanism stops working without reporting it

| Project | Incident |
|---|---|
| Product repo B | A sync job failed but was marked `success`; a rate-limited search returning an empty array was indistinguishable from "searched properly and found nothing" — **every assertion degraded quietly, and everything looked fine** |
| Product repo A | When adding a monitoring cron, the cron nearly got added without the branch — the scheduled backstop would have regenerated that day's output and overwritten the already-published version. **Zero symptoms day to day** |
| Product repo A | If the alert webhook silently returns when it isn't configured, that is a monitor with the bell installed but not wired |

**Why it counts as a mode**: missing config, nonexistent directory, zero files scanned — all of these must be **red**, never "no problem".

### `sections` — §X.Y references pointing at sections that don't exist

| Project | Incident |
|---|---|
| The source project | An audit found that the v1.0 Plan's references to §9.1/§9.3/§9.4 **all pointed at the wrong sections**. Root cause: references written from semantic memory — after the spec was renumbered, references don't error, they just silently point at the wrong place (a rule was set afterward: every §X.Y must be verified with grep) |

### `index` — decision directory and index don't match

| Project | Incident |
|---|---|
| The source project | Three authors all missed the "Recent ADRs" row in the ADR index. A decision that was written but isn't in the index can't be found by anyone going through the index — as good as not written. This is Step 2 of the four cascade steps. **The source project's fix was also validation, not generation**: a freshness check was added that exits with code 1 on a missing link |

### `tables` — tables that break on render without any error

| Project | Incident |
|---|---|
| The source project | A roadmap's table got corrupted — a blank line truncated it, the second half became orphaned fragments, and GFM rendering broke outright |
| Product repo A | **Caused by the checker's own author**: a "⚠️ note" was inserted in the middle of the three-layer guardrail table in Plan B Spec §6.4, cutting layers 2 and 3 off into orphaned fragments. The tables mode caught it the day it was added |

### Architecture layer (checked by audit, not check)

| Project | Incident |
|---|---|
| Product repo A | Asserted "CI already blocks it; there are no cases CI can't catch" — **a conclusion without checking**. Measured: **36 of the last 80 commits were direct pushes to main** (the first write-up had a different number that couldn't be reproduced on re-measurement; corrected). G6 was split into "CI" and "local commits" because of this |
| Product repo A | Asserted "this repo's ADRs don't use frontmatter; forcing a schema on them is just imposing a shape" — also wrong. The 8 ADRs had a **strictly consistent** four-line convention (status/date/decider/related); what's validated is "consistent fields", not "must be YAML" |
| Product repo A | The first drafts of two ADRs **had no cascade memo section**, and three PRD conflicts sat for a day; after it was added, `docs/PLAN.md` (the project's own rule says it is the single source of truth) and SPEC §6.4 were missed again |
| Product repo A | Four root entry files from an AI collaboration scaffold, checked pair by pair against the project's own family READMEs: **all four pairs had drifted**, and two of them were "rules pointing the wrong way" (saying "status is authoritative in `PLAN.md`", which was exactly the one that had stopped being updated). Removing it took five PRs. **The killer is that nothing could see it** — it surfaced only because the owner happened to ask. On the same machine, 10 projects have the same scaffold installed, and 3 are already one to two months behind. So a G4 criterion was added: report any scaffold ledger more than 30 days behind the repo |

### The checker itself (each one produced a regression test)

Of the 26 findings reported on the first real-repo run, **7 were bugs in the checker itself**: quoted old text treated as a TODO,
estimated dates reported without stating their source, backtick paths not resolved against `docs_root`, heading lines treated as commitments,
the noun compound "pending-confirmation card", the UI label "awaiting your confirmation", and the word for "etc." in "product **etc.** stakeholders" (the same character also means "wait");
plus two § reference false positives (bold inline subsections aren't headings) and four table false positives (escaped pipes treated as column separators).

> **An inaccurate checker is worse than no checker** — people start distrusting its output, then ignore the real hits along with the false ones.
> The source project's table validation had long handled escaped pipes; the first version of the probe didn't.

### The checker itself, second pass (three findings from a later real-repo run)

One `audit` run reported 0/7. **Two of those verdicts were false and one was an unfillable prescription.**
All three share a root: the checker stated "what I checked under my default settings" as if it were fact.

**One — G2 looked in the wrong place.** The project kept its decision records in `docs/decisions/`;
the audit looked only at the default `docs/adr` and reported "no decision-record directory". There were three,
numbering continuous, H1 matching the filename, filenames matching the very regex the checker uses.
*The worse half is what came next*: `init` would have created `docs/adr/README.md` at the default path,
so the tool would **manufacture the very "second answer" it exists to detect** (the G4 failure mode).
Fix: with no config, discover the layout from file content, say in the output whether the path was discovered
or guessed, and have `init` write the discovered path.

**Two — G5 stated "I did not see it" as "it does not exist."** It asserted "not a single device" while a device
did exist: a scheduled task outside the repository. **The search scope is itself a blind spot.**
Fix: the wording became "no device found", and the output now always names the scope it searched.

> **A rejected fix, recorded so it is not re-attempted.** The first attempt also *scanned* the home-directory
> scheduled-task folder so outside devices would be counted. Three standing security tests caught it at once:
> it read every task definition on every audit — files this tool has no business opening, some of which may hold
> credentials — breaking the invariant that audit reads nothing outside the repository it was pointed at.
> The honest half (naming the scope) was kept; the scanning half was dropped, and the reader is told to judge
> outside devices by hand. **A fix that widens what a tool reads must be weighed against the boundary it crosses.**

**Three — G6 wrote a prescription that could not be filled.** The directory was not a git repository at all,
yet the audit reported "no docs gate in CI or on local commits" and offered to install a pre-commit hook.
**Cannot-install is not not-installed.** Fix: check for a repository first, say so plainly, and stop offering
a hook that cannot be attached.

> The third finding also exposed a fixture hole: `repo()` never created `.git`, so "not a git repository" —
> a real situation — had **never once been tested**, which is exactly what let the unconditional hook offer
> look correct. **A fixture's defaults are themselves untested assertions.**

## Project-specific additions

(New projects add their own incidents here, in the same format as above)

## The checker's own incidents

- **init crashed on a real repo**: once installed in a project, the script is a copy under `scripts/`, and `templates/` isn't next to it,
  so `FileNotFoundError` propagated all the way to the top of the stack. The unit tests all run inside the skill source directory and never hit this path —
  **you only run into it by actually running it once**. Fix: look for the templates directory in two places; if neither exists, report a clear self-check failure.
- **Source path hard-coded to the author's machine**: both the copy comparison and the template fallback looked for the skill source in a fixed local directory.
  Anyone who installed it elsewhere would never find the source — both protections **silently failed together**, no error, they simply ceased to exist.
  Fix: env var `DOC_GOVERNANCE_HOME` first, then the common skill install directories; the regression test was written first and confirmed red, then the fix went in.
  **Later narrowed** after a registry security audit: that same lookup also chose the code `init` copies into the project and the hook scripts it installs —
  code that runs on every commit — so an inherited environment variable could swap them out unchecked. `init` now copies only the script actually running
  (and prints its path and sha256 in the plan); the variable survives only in pre-commit's read-only drift comparison.
- **G5 was judging the sticky note, not the device**: the original criterion only checked "whether the docs mention checkpoints".
  The difference between a written rule and a device bound to an action is whether it ever fires.
- **settings.json got a duplicate registration on every install**: the comparison used `json.dumps` text,
  where the stored quotes were escaped as `\"` and didn't match the original command. Changed to compare the command strings directly.
- **A false positive collided with the labeling exemption, and the checker silenced itself** (`contract` mode's first real-repo run):
  the `code_claim` regex missed `patch`, a **real** endpoint was judged "not found in the code",
  and on that basis "retired" was written into the spec — **pure fabrication**. `contract` mode skips anything marked "retired", so the check went green.
  Fixing it doesn't stop the class: the machine can't tell a true "retired" from a false one. So the warning went into the error message itself —
  **grep it yourself before labeling**.
- **A sticky note hiding in "Deliberately not ported"**: the redaction row's reason was "there are no public releases yet" —
  **a reason with a precondition; when the precondition changes, nobody comes back to look**.
  Device added: red on the spot when an ADR is marked `visibility: public` and `public_content_scan` isn't configured.
  Hits on the term list report only "which entry / which category" and the line number, **never the matched content** —
  otherwise it would copy sensitive values a second time into CI logs (incidents of credentials printed verbatim into logs have really happened, more than once).
- **Things a regex scoops up look like evidence** (three of the same kind): missing `patch` → a real endpoint judged "missing";
  missing default-value syntax like `?? "topic-catalog"` → two of four candidates were false positives; while tallying schedule estimates, grep turned up "31 single-point estimates",
  but the context showed they were all business numbers (a metric up 3 days in a row, backfilling 122 days of history), and the real schedule table had been written in ranges all along.
  **Before treating a grep as evidence, check by hand what it actually caught.**
- **Treating memory as fact about an external system**: the "Deliberately not ported" table in `framework.md` once said
  "the source project maintains its index with a generation script", with a paragraph explaining why it wasn't ported.
  When asked "why isn't this ported?", a look showed **the source project has no generated index at all** —
  its ADR index is hand-written, just like the product repo's. The whole row described something that doesn't exist.
  **Before writing "system X does it this way", open system X and look.**
- **Verifying framework.md item by item: 25 falsifiable claims, 9 didn't hold**.
  1 fabricated (the nonexistent generator above); 6 wrong numbers (directory count, ADR count — which also contradicted itself within the text, repo age,
  number of meta-lessons, direct-push count, PRD staleness in days); 2 not reproducible.
  Two rules grew out of this:
  **① Numbers must carry a measurement date** — the direct-push ratio is a sliding window; the same repo measured at different points gives 33-44,
  an undated number is wrong a few days later, and nothing tells you it's wrong.
  **② `git log -1` gives the most recent, not the earliest** — while fixing framework.md it was used to get "when was the directory first created",
  and the most recent change was taken as the creation date. **A new error introduced in the process of fixing an old one, on the same day.** Verification itself needs verifying.
- **The docs drifted, and nothing was watching**: verifying SKILL.md item by item caught three "feature added, docs didn't follow" cases —
  the description listed 7 check modes (actually 9, missing `links` and `contract`),
  the list of what init installs omitted the two Claude Code hooks, and "eight modes" and "nine modes" coexisted in the same file.
  **The product repo has `contract` watching its spec against its code, while the skill's own docs ran naked.**
  A self-audit group was added (at the end of `test_governance.py`), triggered by running the tests.
  Mutation testing was done while writing it, planting one error per check — **the first check didn't go red**:
  it checked "the mode name appears somewhere in SKILL.md", and the deleted name still appeared in an explanation paragraph further down.
  It took two tightenings: first narrowed to that section, still not red (the explanation was in the same section), then narrowed to the first paragraph after the heading, and that caught it.
  **When writing a checker, "checking too broadly" lets things through just like "checking the wrong place".**
- **When installing the self-audit, the one most in need of checking was left out**: the same day the docs self-audit was installed,
  verifying `governance.py` item by item showed its module docstring had drifted in five places too,
  **and not one of those self-audit checks caught any of them — because they only read the three `.md` files**.
  Worse, three "what goes wrong without it" strings in `audit()` still carried numbers already verified as wrong — **that is output users actually see** —
  and they had only been fixed in `framework.md`, not in the code.
  Added: the docstring's mode table and usage lines, the "N modes" count in the docstring, the docstring's `init` line,
  and a **guard that pins known-wrong phrasings** (red if they reappear).
  **Lesson: a code docstring is documentation too, and it's the copy `--help` prints.**
- **Verifying tests isn't "run once and it's green", it's "does it go red when broken"**:
  `test_governance.py` was verified with mutation testing — break the code under test and see how many tests go red.
  Each of the nine check functions was gutted once, and **each was caught by at least one test** (`sections` by only 1 — thin).
  Then boundary conditions were changed, which exposed **two real gaps**:
  ① Changing the `pending` 30-day threshold to 35 days turned **zero tests red** — nobody had pinned the threshold, so it could be casually raised.
  ② Deleting the line that strips escaped pipes turned **zero tests red** — those are exactly the 4 false positives recorded above;
  **the bug was fixed without a regression test**. Every `\|` in the existing cases was inside inline code, and inline code gets stripped wholesale anyway,
  so the fix had effectively been installed for nothing. Tests were added for both, and mutation was rerun to confirm they go red.
  **A test written "in passing" and a test that actually catches regressions look exactly the same when they run.**
- **The template shipped with a broken table, so new projects started out red**:
  end-to-end verification of `templates/` — spin up an empty project, run `init --yes`, write one decision and one plan **strictly following the templates**, then run `check`.
  **It went red on the first try**: the index placeholder row in `adr-README.md` had a 2-column header and a 1-column placeholder row, and `tables` caught it immediately.
  **Starting out red teaches people to ignore the checker.** Fixed, and pinned with tests: a project installed from the templates must be fully green, the template files themselves must pass tables,
  "the enums the templates teach = the enums the checker accepts", and "the Status format the plan template teaches must be parseable by `STATUS_LINE_RE`".
- **The copy lagged the source by three days, found only because someone asked**: `scripts/governance.py` is a copy of the skill source,
  and the only thing between them was a one-line comment saying "re-cp when the source changes" — **nothing would raise an alarm when they diverged** (CI can't reach the skill directory on the local machine).
  For those three days `audit` kept showing users numbers already verified as wrong — **the copy meant for ourselves got fixed, the copy others see didn't**.
  A comparison was installed in `templates/pre-commit`: on mismatch it does `exit 1` and prints a fix command you can paste directly;
  when the source can't be found it silently skips (CI and other people's machines only have the copy anyway). All three paths were actually run.
- **Guesses written down as reasons: three "not ported" rows, one left after verification**: the "Deliberately not ported" table originally had three rows; pressed item by item —
  ① "auto-generated index" **was fabricated wholesale**; ② "four-layer source-of-truth modeling" didn't hold either: the product repo has all four layers,
  and **L4 has already been ported by `contract`**; ③ only redaction was genuinely not ported.
  ②'s reason was "two layers (product/tech) is enough for a small project" — **that is a prediction, not a reason**.
  In reality the product repo first grew to three layers (forced by a PRD/SPEC conflict), then to four (forced by spec endpoints not matching the code).
  Worse: the first review had already found three layers, yet wrote it up as "which confirms this reason exactly" —
  **the data overturned the conclusion, and it was read as confirmation.** **Rule: don't write guesses down as reasons.**
- **The docs couldn't answer "how do I ask it"**: a user asked "Do I need its commands, or can I just use plain language?" —
  SKILL.md had no answer at the time. The string of trigger words in `description` is **for matching, not for teaching people how to ask**.
  A "How to ask" section was added, and its first sentence is: once installed, you don't need to call it day to day.
  **The same day, a second problem was pointed out**: the example sentences were all jargon. **Real beginners describe symptoms**:
  "my docs are a mess", "my commit got blocked", "I don't understand this red error" — every example was rewritten into symptom shape.
  **Third**: the original plan was to list the options and then ask "which situation are you in right now?" — rejected: **"tutorial" is a reading intent, not an execution intent**,
  and a follow-up question turns a reading request into a commitment the other person never meant to make. Changed to plain statements that leave an exit; the trigger words were expanded into a family (tutorial / how do I use this / what is this for). **Later narrowed**: a bare "help" was on that list, and a security audit rightly pointed out it would fire in unrelated conversations — the trigger now requires the question to be about docs-gov itself.
  **Fourth**: someone proposed renaming the table heading to "Commands" — that would stitch back the "you must recite this exactly" implication; "Typical situation" was used instead.
  **Within the same section, "what to add" and "what to call it" are two independent decisions that can be approved or rejected separately.**
