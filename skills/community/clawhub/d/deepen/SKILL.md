---
name: "deepen"
description: "Point at any topic to build a compounding, domain-general expertise knowledge base: a high-fidelity source corpus, track-record-weighted experts, reconciled falsifiable stances, failure modes, benchmarks, and a proven playbook — built as evergreen notes a future agent can load and reason over. Use when the user wants to deeply master, research, or build durable, defensible knowledge on a topic — not for a quick one-off answer or a single throwaway report."
license: "MIT-0"
---

# /deepen — build a 10,000-hour expertise compendium that compounds

Point this skill at any topic (`/deepen PPC`, `/deepen sleep apnea`, `/deepen paddle physics`). The goal is a **domain-general knowledge compendium** with the depth of someone who has spent 10,000+ hours in the field — built as cross-referenced evergreen notes that **compound across sessions** and are **optimized for a future LLM to load and reason over**. Run it again on the same topic and it deepens and widens the existing knowledge base rather than starting over.

This skill produces **pure domain reference only**. It does **not** apply findings to your specific situation, product, or person — that is a separate concern (a future `/apply <domain> to <situation>` step). Keeping the reference pure is what makes it reusable across every future context and immune to going stale when your specifics change.

The method is grounded in a verified research synthesis (Cooke's structured expert judgment, CFAR Double Crux, Matuschak evergreen notes, Anthropic orchestrator-worker), tuned to the AI-research evidence on retrieval, context engineering, the limits of intrinsic self-correction, and LLM-judge bias. Where a step rests on practitioner convention rather than verified evidence, it says so — match that honesty in the output.

## The three layers (read first)

A literature summary tells you what people say. **Expertise tells you what's true, what's contested, what to *do*, what goes wrong, and where the field is moving.** This KB is built in three layers plus a discoverability spine — never collapse them:

1. **Corpus (raw evidence trail).** High-fidelity digests of the actual sources — practitioners, podcasts, papers, courses, talks — each with a link back. This is the recall layer: it preserves the material so verdicts are auditable and future runs can dig deeper without re-scraping.
2. **Synthesis (judgment on top of the corpus).** Principles, the expert map, and the reconciliation of disagreements — all citing *into* the corpus. This is where conflicting findings get adjudicated and a defensible stance is taken.
3. **Mastery (the proven, operational layer).** The domain-general playbook, failure modes, benchmarks, and worked cases — the proof-filtered long tail an operator actually runs on.

The spine — `_index.md`, the glossary, dense cross-links, and per-file metadata — makes the whole thing discoverable and loadable.

> **Recall vs. proof are different jobs on different files.** The corpus is high-recall, lightly filtered (capture the material). The mastery layer is proof-filtered (only what survives the adversarial gate). Don't conflate them — that tension is resolved by layering, not by piling everything into one file.

## Core principle: track record, not credentials
**Expertise is measured track record, not fame.** Across 33 structured-judgment studies, <1/3 of credentialed experts were statistically accurate, and experts are *systematically overconfident* — their stated uncertainty is far too narrow. Never rank a source by fame, title, or follower count. Rank it by demonstrated, checkable accuracy. And widen your own confidence intervals — the honest answer is less certain than it feels.

> **Source authority ≠ source accuracy.** A high-authority source with a poor track record ranks below an independent one with checkable calls. Authority is a weak prior, never the ranking.

### Proxy ladder — how to weight a source when no Brier score exists
Most practitioner domains publish no calibration record. Do **not** silently fall back to fame. Use this ranked ladder and record which rung each source earned:
1. **Checkable past calls** — did their specific, dated public predictions/recommendations age well? (Strongest signal.)
2. **Shows work** — do they cite data, name mechanisms, reason transparently, vs. assert? Reproducible > authoritative.
3. **Calibration behavior** — do they state uncertainty, distinguish knowledge from guess, visibly update when wrong?
4. **Peer recognition by other high-track-record sources** — weak, flagged as weak. Fame/followers/title alone is **rung zero — not evidence.**
A source can be famous and rank low. Say so when it happens — naming a loud-but-unsubstantiated consensus is part of the value.

## Core principle: beat the consensus, don't reproduce it
A general LLM regresses to the **volume-weighted consensus** — the modal answer, weighted by how often it's written down. But written-a-lot ≠ true: the best answer is frequently **seldom-written, tacit, or closely-held** (the proven operator's edge, kept off the page). Expertise is the *alpha over consensus*, so this skill's job is to **beat the modal answer, not reproduce it**:
- **Volume is not evidence.** "Everyone says X" / "it's well established" is a prompt to *investigate*, never a reason to believe. Treat your own first-instinct answer as the **consensus baseline to beat**, not the output — it is literally the training-data mode.
- **Divergence is a deliverable.** The KB earns its cost where it moves *off* consensus to a better, defensible answer — or *honestly confirms* consensus only after a real attempt to break it. "More citations, same answer" on a settled topic is a weak result; label it as such.
- **The corpus ceiling (be honest).** Retrieval can elevate the rare-but-written above the popular-but-wrong; it **cannot** reach genuinely unwritten alpha. Where the edge is tacit, say so and route to primary sources — never launder consensus as expertise.

## Knowledge base location & structure
Each topic gets a folder under your knowledge-base root: `<KB_ROOT>/<topic-kebab>/`. **Resolve `<KB_ROOT>` once at the start of every run, in this order:** (1) if the user named a location in the request, use it; (2) else if a `DEEPEN_KB` environment variable is set, use it — on a shell runtime, read it explicitly (e.g. `echo "$DEEPEN_KB"`); (3) else default to **`./knowledge/`**, relative to where the skill is invoked. **State the resolved path in your opening line** so the user can redirect it before you write. Point it at wherever your durable notes already live — **including an Obsidian vault** (the notes use `[[wikilinks]]` and YAML front-matter, so they render and graph natively there). On a runtime with no shell or no persistent disk (e.g. a hosted chat sandbox), skip the env-var step: write to the working directory if one persists, otherwise return the notes inline for the user to save. Never silently skip writing because a path is unset — always fall back to the default and say where you wrote. If any of the knowledge base is sensitive, keep it out of public repos.

**Files scale to the domain** — a thin topic collapses several of these into one; a deep one splits them. The schema defines the slots; fill what the domain warrants. Don't force empty files.

- **`_index.md`** — the loadable map. The single entry point, **designed to fit one context window** so a future agent reads only this and then pulls what it needs (progressive disclosure, not load-everything). Contains: topic scope + aliases, the depth dashboard, a one-line descriptor per file/section, a **"to do task X, read these files" router**, last-updated date, and mode of last run. Read this *first* on any re-run.
- **`sources/`** — the corpus. One digest note per significant source (`sources/<author-or-org>.md`, `sources/<podcast-episode>.md`). See the fidelity rule below. This is the recall layer.
- **`principles.md`** — DURABLE first-principles knowledge: mechanisms, models, why-it-works, **with the field's history and key inflection points woven in where they're load-bearing** (origin → evolution → forks in the road and *why* each mattered — distilled and relevant, never a museum). Atomic, densely cross-linked `[[notes]]`. Each concept carries a `misconceptions:` line. Slow to change; must never rot.
- **`experts.md`** — the expert/KOL map. Canon (foundational) + frontier (current). Each entry: who, their actual track record / what they got right or wrong, the **proxy-ladder rung** justifying the weight, a credibility weight (H/M/L), and a `[[link]]` to their `sources/` digest. Fame is not a reason.
- **`disagreements.md`** — live debates. One entry per contested question: the **crux**, **my stance**, **calibrated confidence**, **explicit falsifier**, and a **survived-refutation** note. **This is the one file that uses claim-IDs** (see citations rule) — contested calls earn surgical traceability. Highest-value file; where judgment lives.
- **`playbook.md`** — the domain-general best-practice + **diagnostic** layer. Procedural craft ("how," not "why"): order of operations, decision trees ("if ROAS drops, check X→Y→Z"), the moves experts run on autopilot. Proof-filtered. Dated + decay-flagged.
- **`failure-modes.md`** — anti-patterns and expensive mistakes: what kills results, what looks right but isn't, the errors experts are defined by *not* making. (Highest-value addition over a plain summary.)
- **`benchmarks.md`** — the reference numbers an expert carries in their head (healthy ranges, thresholds, "normal"). Each `decays:`-flagged and `last-verified:` dated — these move.
- **`frontier.md`** — the open unknowns and where the field is actively moving. Doubles as the **loop's fuel**: the ranked list of where to dig and widen next.
- **`glossary.md`** — the ontology + jargon map (terms, acronyms, how insiders use them vs. textbook). Doubles as a **retrieval bridge** — fixes the query↔note vocabulary mismatch that is the #1 reason notes get missed.
- **`cases.md`** — a small library of canonical worked examples with numbers and outcomes. Experts reason by pattern-matching to cases; this is that material.
- **`changelog.md`** — append one line per session: date + what was added/changed/**superseded**. How accretion stays auditable.

Keep it lean. Atomic ≠ a hundred fragments — one idea per note, but no note that doesn't earn its place. Supersede in place; never append-and-bloat or leave two conflicting claims live.

### Corpus fidelity rule (no over-distillation)
A source digest is **high-fidelity, not a thin summary**. Capture *everything that carries information* and cut only filler, repetition, and banter. A meaty podcast is 8–15 substantive points; a practitioner's body of work is 10+ claims with their reasoning and standout verbatim quotes (with timestamps where available). The test: **could a future agent reconstruct the source's actual argument from this note?** If not, it's over-distilled — go back.

Store **digests + links, not verbatim transcripts.** Verbatim transcripts are ~95% filler, large, and a dead-archive risk. Full-text archive is by *exception only* — a load-bearing source that is paywalled or likely to vanish. Never blanket-scrape transcripts.

### Citations — source-level default, claim-IDs for contested claims
- **Default (everywhere): source-level citation.** Every claim links to its `sources/` digest (which holds the external link). 80% of the auditability at near-zero ceremony.
- **`disagreements.md` only: claim-level IDs.** Contested claims get a stable anchor in the corpus (`^pmax-cannibalizes-brand-2024`) and the stance cites it by ID — surgical traceability where it actually earns its keep.
- **Cite-or-flag (hard rule).** Every claim in `principles.md`, `experts.md`, `disagreements.md`, `benchmarks.md` either cites a fetched source or is tagged `[inference]` (your reasoning) or `[convention]` (practitioner norm, unverified). No bare unsourced assertion may read as fact. This is the line between expertise and confident hallucination.

### Built for future LLM loading (context engineering)
The KB must let a future agent **find and load the right slice without reading the whole thing**:
- **Front-matter metadata on every file** — `tags`, `aliases`, `last-verified`, `decays`, `confidence`, `depth-level`. Machine-filterable, and the hook for vector search later.
- **Lead every file with a 2–3 line abstract** so an agent can read the head and decide whether to load the rest.
- **Self-contained notes** — no "as discussed above." Each note must make sense pulled out of context alone (proper evergreen discipline; required for chunked retrieval).
- **Single source of truth** — one claim lives in one place; everything else `[[links]]` to it. Duplication bloats context and breeds contradiction.
- **The glossary is the retrieval bridge** — search by meaning *and* by the field's actual vocabulary.

### Depth-calibration dashboard (in `_index.md`)
Set a **target depth per sub-area** and track current depth — the map of what's solid and the loop's progress meter. Scale: **L1 Aware · L2 Familiar · L3 Competent · L4 Proficient · L5 Expert.** One row per sub-area:

| Sub-area | Target depth | Current depth | Confidence (H/M/L) | Sources count | Last-verified | Thinness / what's missing |
|---|---|---|---|---|---|---|

Because this skill builds *general* mastery (not goal-scoped to one situation), default targets are **L4 across the field's load-bearing sub-areas**, L2–L3 for peripheral ones. Re-runs target the largest target-minus-current gaps first.

### Topic canonicalization
Before creating a folder, check whether the topic is an alias of an existing one (`PPC`/`paid-search`/`SEM` overlap). Pick **one canonical kebab name** and list known aliases in `_index.md` so future runs route to the same KB instead of forking a silo.

## Workflow when pointed at a topic

### 0. Orient & reconcile
- If `<KB_ROOT>/<topic>/` exists, read `_index.md` + `changelog.md` first — you are *deepening and widening*, not restarting. Target the largest depth gaps and the top `frontier.md` items.
- **Reconcile with existing knowledge.** Search `<KB_ROOT>/` for related/overlapping topics **by keyword *and* by meaning** (try synonyms, aliases, and a *drafted answer* rather than the question — vocabulary mismatch is the #1 reason related notes get missed). If a search comes up empty, reformulate before concluding nothing exists. Cross-link related KBs; never silo a duplicate. If findings contradict an existing note, flag for supersede — don't quietly fork.
- If new: canonicalize the name, create the folder + `_index.md` scaffold, set target depths.

### Effort tiering — pick the mode first
- **Light pass (default):** single agent, existing knowledge + a handful of targeted searches. Produces/updates `_index.md`, a first-cut `principles.md`, a few `sources/` digests, and the top of the playbook. For a fast map or a low-stakes sub-area.
- **Deep pass (on request, or when targets are L4–L5 or the dashboard shows a big gap):** full orchestrator-worker fan-out (steps 1–6) with the adversarial gate. Reserve deep-research-scale fan-out for genuinely hard, high-value topics.

### Compute tiering — models + the decomposed runner (default for deep passes)
Run a deep pass as an **orchestrator with a fleet of cheap workers and an apex brain on top** — never as one monolithic context (a single context that reads the old KB + all sources + writes every file runs into the model's window ceiling and silently degrades mid-write; decompose so no one context holds the whole job).

Match the model to the *kind* of work, not uniformly cheap. (Tier names below are conceptual; map them to whatever model families your runtime exposes — e.g. a small/fast model, a mid model, and a frontier model.)

| Tier | Example role | Jobs | Parallelism |
|---|---|---|---|
| **Cheap** | small/fast model | fetch · clean HTML · pull transcripts · relevance Y/N triage · dedup · format | dozens at once |
| **Mid** | mid model | write high-fidelity `sources/` digests · first-pass claim extraction · the **skeptic swarm** (breadth of attacks, step 4.5) | many |
| **Apex** | frontier model | orchestrate/decompose · weight experts by track record · adjudicate disagreements · take stances · **final adversarial judge** · synthesize `principles.md` · supersede calls | 1 (few) |

**Why tiered, not uniformly cheap:** the recall/extraction layer is faithful compression — cheap models are correct there, so run them wide. The judgment layer (stances, adjudication, the judge) is the skill's entire edge over a summary, and cheap models there produce confident-but-wrong reasoning — the evidence is explicit that intrinsic self-correction is unreliable and cheap LLM-judges are more biased. **The final judge and synthesis stay apex, always.**

**Decomposed runner flow:** orchestrator (apex) decomposes → cheap/mid research workers fan out across distinct source pools (below) and each **writes its own `sources/` digest** (one file per worker = no write contention) → apex reads the `sources/` corpus and synthesizes the judgment files. **Synthesis writes stay single-threaded on the apex model** — workers may each write their own corpus note, but only one writer touches `principles.md`/`disagreements.md`/etc.

**Anti-hallucination scales with how cheap you go:** cheap workers get strict "**quote-and-link, never infer; obey cite-or-flag**" instructions, and a cheap verification pass checks each digest's claims against the fetched source before it's trusted. The corpus is the foundation everything rests on — a hallucinated digest poisons every layer above it.

> **Implementation note (portable):** if your runtime can spawn parallel subagents or run a multi-agent harness, use it and pass a per-worker model so only the workers drop to a cheaper tier while the orchestrator/judge stay frontier. If your runtime is single-agent, run the same flow sequentially — decompose, research each pool, write digests, then synthesize — the *structure* is what matters, not parallelism.

### 1. Decompose (orchestrator)
Break the topic into 4–6 sub-questions spanning: foundational mechanisms + history, current best practice, open controversies, failure modes, and the execution surface. Map each to a dashboard sub-area + target depth so effort tracks the target.

### 2. Research fan-out (parallel subagents)
Spawn one research subagent per sub-question (or work them sequentially if single-agent). Each mines BOTH **canon** (foundational texts/experts) and **frontier** (who's pushing it *now*, dated sources), and writes high-fidelity `sources/` digests as it goes. Do empirical research *first*; reserve "expert opinion" for genuinely frontier-of-the-unknowable questions.

**Minimum viable setup: a web search + fetch tool alone is enough to run this skill.** Every other pool below is *additive recall*, not a requirement — none needs to be installed for a valid run. Never block or abort because a pool is unavailable; use what your runtime has, and note in `_index.md` which pools you couldn't reach so a future run can widen there. Copy-paste request recipes for the keyless and keyed backends are in the bundled [`CONNECTORS.md`](CONNECTORS.md).

**Spread workers across DISTINCT source pools — not all at one search index.** Parallel fan-out only widens recall if workers draw from non-overlapping pools; ten workers on one index just resurface the same pages. Useful pools (use whichever your runtime can reach; all are public unless noted):
- **Web search + fetch** — your search provider + a fetch tool (fetch many URLs concurrently). The baseline.
- **Video & podcasts** — a caption/transcript tool (e.g. `yt-dlp` for captions/auto-subtitles, a speech-to-text fallback for caption-less audio) → talks, conference sessions, podcast episodes. The modality plain text-search misses.
- **Social / practitioner frontier** — read practitioner threads and dated public calls on whatever platform the field lives on (strong for *track-record* signal — what they predicted, and whether it aged well).
- **Code hosts** — GitHub/GitLab APIs for technical domains: code, READMEs, issues, discussions.
- **Academic (keyless APIs)** — arXiv API, Semantic Scholar API, PubMed E-utilities → primary research for the canon/empirical layer.
- **Forums (keyless APIs)** — Reddit JSON endpoints (`old.reddit.com/r/<sub>/search.json`), Hacker News Algolia API → practitioner ground truth and failure-mode signal.
- **Semantic search backends (key required)** — neural/embedding search indexes (e.g. Exa, Tavily, Brave) are each a *different* index → real recall diversity. Call their REST APIs directly rather than installing unvetted third-party plugins. Spread workers across these *and* the keyless pools.

> **Fan out only for decomposable breadth.** Parallel subagents help when sub-questions are independent; cost scales with total tokens across context windows at a steep multiple — spend knowingly. **Writes stay single-threaded:** never let parallel agents write the same KB file — one writer per file, always, or the notes corrupt.

> **Honesty note:** this skill synthesizes experts' *published record* — papers, talks, dated public calls. It does **not** interview live people and does **not** fabricate expert personas, credentials, or quotes. A "what would expert X say" view must be grounded in that person's actual sourced positions.

> **The tacit frontier:** the best operator alpha is often *unwritten or closely-held* — not in any corpus. Mine the **rawest primary record** to get as close as text allows (practitioner long-form, recent talks, niche forums/communities, teardown threads, proprietary-data writeups — not second-hand summaries), and weight it by track record. But you cannot conjure the unwritten. So per topic, **name the tacit gap explicitly** — what the best operators almost certainly know that isn't on the page — and flag that closing it needs a primary source: a practitioner interview, or *the operator's own data/experiments*. That flag is the handoff to `/apply <domain> to <situation>` + real numbers. Surfacing the gap honestly beats papering over it with consensus.

### 3. Map & weight the experts → `experts.md`
For every significant source, record demonstrated track record and assign a weight via the **proxy ladder** (record the rung), and `[[link]]` to its `sources/` digest. Separate genuine signal from popular-but-wrong consensus. Correct every confidence estimate for known overconfidence (assume intervals are too narrow).

### 3.5. Consensus-buster — find the strongest challenger (run before adjudicating)
The default LLM answer *is* the consensus; this step manufactures the contest that beats it. For each load-bearing question:
1. **State the consensus** — write down the modal, volume-weighted answer a vanilla LLM or textbook would give. Name it explicitly so it's a *target*, not an anchor.
2. **Hunt the challenger** — go find the **highest-track-record dissent** and the **seldom-written frontier** claim that beats it (proven operators, recent primary work, contrarians with checkable calls, niche communities). Weight by record, not by how common the view is.
3. **Run the contest** — adversarially test (reuse the §4.5 gates): does the challenger actually win on evidence, or is it contrarian noise? The challenger must *earn* the upset; default to consensus only after it survives a real attempt to beat it.
4. **Record the verdict** — every verdict resolves to **one of THREE outcomes**, never a forced binary:
   - **challenger wins** — the dissent/frontier beats consensus on evidence. The KB's highest-value output.
   - **consensus survives attack** — write "survived attack: <best challenger and why it failed>," never assume it.
   - **still-contested** — *neither* side wins after a genuine attempt. **This is a legitimate, required verdict** — do NOT manufacture a call where the evidence is honestly split. Record it as `contested` and name the **crux** (the finding that would resolve it) + what data is missing. Forcing certainty on a genuinely-open question (e.g. dietary salt, saturated fat) is a failure mode, not rigor.
   Write it in `disagreements.md` as `consensus → challenger → who-wins-and-why (or contested + crux)`, with calibrated confidence + falsifier.
5. **Retrieval is mandatory.** Each verdict must cite **≥1 dated source** found this run (the consensus-buster's whole point is beating parametric memory). A verdict resting only on the model's prior is marked **`parametric-only`** and treated as untrustworthy until a dated source backs it — never let an un-retrieved memory pose as a researched call.

### 4. Adjudicate disagreements → `disagreements.md`
For each live disagreement, run an adapted **Double Crux**: (1) state it concretely; (2) operationalize what the sides actually differ on; (3) find the **crux** — the load-bearing belief that, if false, flips the conclusion; (4) **take a stance** with calibrated confidence (+ *why*) and the **explicit falsifier**; (5) be method-pluralistic on aggregation — no single rule settles conflicting experts. Refusing to take a position is a failure; a wrong-but-falsifiable stance is recoverable, a mushy "both sides have merit" is not.

> **Adaptation note:** Double Crux is a two-person technique; here one agent adjudicates *others'* disagreement. Legitimate adaptation — don't present it as live dialectic.

### 4.5. Stress-test before committing (red-team + validation gates)
Before any stance is written to `disagreements.md`, and before a `principles.md` note is treated as solid, run three gates:
- **Adversarial self-falsification.** For each stance, spawn (or role-play, on a light pass) a **skeptic whose only job is to refute it** using the strongest *external* counter-evidence (re-search / re-fetch — bare "let me reconsider" doesn't count). Randomize presentation order when scoring competing claims (order alone can swing judgment >10%); never let one pass be both sole author and sole judge. Survives strong refutation → keep + note "survived: <best counter and why it failed>." Survives weakly → **downgrade confidence**, say why. Skeptic wins → flip or retract.
  - **Skeptic swarm (deep pass, budget permitting):** run several **cheap/mid** skeptics in parallel, each assigned a *different* angle of attack (empirical: is the data real/replicated? · mechanistic: does the causal story hold? · source: is the evidence an interested party? · base-rate: is this just regression/selection?). Cheap models supply *breadth* of attack; the **apex model is the sole judge** of which attacks land. Diversity of attack beats brilliance of any one attacker — but the final vote is never a cheap model's.
- **Teach-back.** Explainable simply, from mechanism, without jargon hand-waving? If not, mark it thin.
- **Prediction.** Does it correctly retrodict a *known* outcome (documented case, benchmark, historical result)? Can't retrodict → flag the gap.
A stance/principle that passes all three is earned; one never tested is not.

**Calibration discipline (the mid-band trap).** Measured failure mode: calls in the **0.6–0.8 confidence band are the least reliable** — "leaning but unsure" is where overconfidence hides (a backtest put that band near coin-flip accuracy while 0.85+ calls held). So: treat 0.6–0.8 as a **yellow zone** — before committing such a call, either (a) find the one piece of evidence that would push it ≥0.8, or (b) drop it to `contested`/≤0.55. Reserve 0.8+ for calls with a clear evidentiary backbone. Widen every interval for known overconfidence; the honest answer is less certain than it feels.

### 5. Knowledge-base write (evergreen notes)
Write durable findings into `principles.md` as **atomic, concept-oriented, densely-linked** notes (each with its `misconceptions:` line, history woven where load-bearing, and cite-or-flag tags). Populate `failure-modes.md`, `benchmarks.md`, `glossary.md`, and `cases.md` as the research surfaces them. Update the `_index.md` dashboard (bump depth, confidence, source count, last-verified) and the **read-first router**. Append to `changelog.md`.

**Supersede rule:** when new evidence contradicts an existing note, *replace the claim in place* and log `superseded: <old> → <new> (why)` in `changelog.md`. Never leave conflicting claims live; never silently delete the old one.

### 6. Distil the proven layer → `playbook.md` (domain-general)
Convert synthesis into a **domain-general** best-practice and diagnostic playbook — the proof-filtered long tail (only what cleared the adversarial gate). Procedural craft, decision trees, order-of-operations. Rank by leverage using **ICE/RICE** as a *forcing function for prioritization, not a precise score (convention, not verified)*. Each item: the move, when it applies, expected leverage, and how you'd know it worked. **No situation-specific specifics** — this is reusable field knowledge; applying it to your case is the separate `/apply` step.

## The loop — a frontier-expander, not a brake (for `/loop … /deepen`)
When run on a loop, each pass: **(a)** deepen the largest dashboard gaps → **(b)** when the core saturates, *branch* into the adjacent sub-topics ranked in `frontier.md` → **(c)** follow citation trails from existing `sources/` to new ones. Dig hard; widen naturally.

- A pass **only counts if it adds net-new sources or claims.** Rephrasing/polishing is not a pass — log it as `no-net-new` and move on.
- **Pause only when the *widened* frontier is dry** — no net-new sources for K consecutive passes (default K=2) even after branching. On pause, hand back the ranked list of what it *would* chase next (and how tangential it's getting) and ask: keep widening or call it?
- This is the tripwire against padding: it keeps mining and expanding scope as long as real value surfaces, and stops only when genuinely dry — not at an arbitrary count.

## Staying current without rotting the core (convention)
Split knowledge by decay rate:
- **Durable** (`principles.md`, much of `failure-modes.md`/`glossary.md`) — mechanisms, first principles, psychology. No decay flag.
- **Fast-moving** (`playbook.md`, `benchmarks.md`, platform notes) — algorithm/platform changes, current numbers. Each carries `last-verified: YYYY-MM-DD` + a decay flag (`decays: fast` for platform mechanics, `decays: slow` for buyer psychology). On any re-run, re-verify anything `decays: fast` older than ~90 days before relying on it; refresh the tactical note without touching the durable core.

## Output to the user (every run)
A tight brief, not a document dump:
1. **What I now know** — the 3–5 load-bearing truths, with confidence.
2. **Where I took a stance** — each contested call, position, what would flip it, whether it survived refutation.
3. **Mastery added** — what landed in the playbook / failure-modes / benchmarks this pass.
4. **Frontier** — what's still below target and what the next pass would dig/widen into.
5. Mode run (light/deep) + KB path + new source count.

Lead with the point. Numbers over adjectives. State confidence out loud and flag thin evidence — don't launder convention as proof.

## Guardrails
- The knowledge base is yours. If any of it is sensitive, keep it out of any public repo you publish.
- **Pure domain reference — never applied to your specific situation in the KB itself.** Application is a separate, on-demand step. This keeps the KB reusable and stale-proof.
- This skill produces *knowledge*, never actions. It does not send, post, publish, move money, or take irreversible steps on your behalf.
- Distinguish verified findings from convention (cite-or-flag). Honesty about evidence strength is part of the deliverable.
- Never fabricate experts, credentials, sources, or quotes. Synthesize the real published record only.
- Digests + links, not verbatim transcripts (full-text by exception only).
