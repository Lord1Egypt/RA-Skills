---
name: conclave
description: "Conclave is a multi-agent reasoning skill that orchestrates multiple AI CLIs into structured debates. Each agent independently analyzes the problem, challenges competing arguments, identifies flaws and contradictions, and refines the reasoning through multiple rounds of discussion — helping you reach more reliable conclusions than relying on a single AI."
version: 1.6.7
author: Hermes Agent
metadata:
  hermes:
    tags: [Debate, Multi-Agent, Decision, Claude, Codex, Gemini, Qwen, DeepSeek, Doubao, Ark, Manus, Install, Update, Export, Archive]
---

# Conclave — Multi-Agent Structured Debate & Adjudication

Given a user topic, convene AI agents to independently posit arguments, engage in anonymous cross-examination, converge, and sign off unanimously, producing a chair-adjudicated final markdown report.

Use for high-stakes decisions (pricing structure, contract risk, architecture selection, investment judgment). Do not use for daily trivia.

## ⚠️ Full Capability Disclosure (read before installing)

This skill does **significantly more** than "debate orchestration". By design it:

- **Installs and updates global CLI tools** (`npm install -g`, brew, apt, etc.) via `scripts/install.sh` and pre-flight self-updates.
- **Inspects local auth state** (checks for API keys, OAuth tokens, keychain status) without reading secret values.
- **Transmits your debate topic** to 6 third-party AI cloud APIs (Claude/OpenAI, Google, Alibaba, ByteDance/Ark, Manus).
- **Persists full debate records** indefinitely under `~/.hermes/debates/` (briefs, raw agent outputs, verdicts, votes).
- **Mandatorily exports** the entire arena to the current working directory after every debate.
- **Calls external REST APIs** (Manus `api.manus.im`) with the debate final draft.

**Do not install if** you are not comfortable with global package changes, third-party AI services seeing your content, or full debate archives being retained and copied into your working directory.

## ⚠️ Security & Privacy Notice

**Before using Conclave, read this.**

1. **Local data persistence**: Every debate creates a persistent folder under `~/.hermes/debates/` containing the full brief, all agent outputs, anonymity mappings, chair verdicts, and final reports. These files remain on disk indefinitely unless you manually delete them. Do not use Conclave for topics containing regulated personal data, trade secrets, or classified information unless you accept this retention risk.

2. **External data sharing**: Panelists (Claude, Codex, Gemini, Qwen, DeepSeek, Doubao) receive debate prompts via their respective cloud APIs. The external advisor (Manus) receives the final draft and round summaries via MCP or direct REST polling. By running a debate, you are transmitting your topic and context to these third-party AI providers. Review each provider's data policy before debating sensitive topics.

3. **Credential handling**: This skill **never** prompts for, stores, or logs passwords. The Claude Code auth section previously referenced an unsafe `security unlock-keychain -p <password>` pattern; this has been removed. Users must manually unlock the macOS keychain in an interactive terminal before background sessions.

4. **Input validation**: The `init_debate.sh` script sanitizes the topic slug to lowercase letters, digits, and hyphens only. Do not pass unsanitized user input directly into shell commands.

5. **Data retention & cleanup**: See `scripts/cleanup.sh` for automated cleanup of debates older than a configurable retention period. Run it periodically or via cron.

6. **Calibration logging**: Verifiable predictions are appended to `~/.hermes/debates/calibration.jsonl` (prediction_id, question, timestamp, agent, role, probability, resolution_date, ground_truth, brier_score, log_loss). This file grows indefinitely. It contains only verifiable predictions, not strategic judgments. Remove it manually if you do not want this persisted.

## Roles

| Role | Who | Notes |
|------|-----|-------|
| Chair & Panelist | Hermes (this agent) | Moderates the session and also argues; must be impartial and must not favor any side (including itself) |
| Panelists | Claude / Codex / Gemini / Qwen / DeepSeek / Doubao | Six CLIs covering reasoning, audit, research, China, coding, and generative domains |
| External Advisor | Manus (MCP API, async) | Does not join regular rounds; reviews the final draft before sign-off; fatal-level objections give the chair the right to call an extra round |
| User | Human | Reviews only the final report; the anonymity mapping is transparent to the user (the user has the right to know who is who) |

## Prerequisites (what the user must install / configure before first use)

`scripts/install.sh` auto-installs Node.js and the four npm-based CLIs and audits their auth, but it does NOT cover the two extra Deep-mode panelists, the external advisor, or the shell utilities the round scripts depend on. Install and configure everything below before the first debate. Nothing here is optional for Deep mode; Standard mode needs only items 1-2 + the first four panelists.

### 0. System dependencies
- **Node.js >= 18 + npm** — runtime for four of the panelist CLIs. `install.sh` installs it via brew/apt/dnf/pacman/winget where possible.
- **python3** — used by the round scripts to parse JSON API responses (Doubao/Manus). Ships with macOS/most Linux; on minimal systems install it.
- **jq** — used to JSON-escape long prompts before sending to HTTP APIs. Install via brew/apt if missing.
- **git** — only if you publish/sync the skill; not needed to run debates.

### 1. Four npm CLIs (auto-installed by install.sh)
| Panelist | Package | Auth the user must complete |
|----------|---------|------------------------------|
| Claude Code | `@anthropic-ai/claude-code` | Run `claude` once interactively, finish OAuth login. On macOS, unlock the login keychain in an interactive terminal before background debates. |
| Codex | `@openai/codex` | Put the API key in Codex's `auth.json` and set base_url/wire_api in its `config.toml` (see references/panelists.md). |
| Gemini CLI | `@google/gemini-cli` | Export `GEMINI_API_KEY` (and base URL if using a relay) in your shell rc. Key prefix decides the provider — do not mix official and relay keys. |
| Qwen | `@qwen-code/qwen-code` | Run `qwen` once interactively to log in, or export the API key/base URL in your shell rc. |

Run `bash ~/.hermes/skills/conclave/scripts/install.sh` (or `--check-only`) to install these and print an auth checklist. Any `[ACTION]` line = the user must fix that provider before debating.

### 2. Two extra panelists for Deep mode (NOT covered by install.sh — install manually)

> **⚠️ Known-issues warning (verified 2026-08-16): the two Deep-mode-only panelists are the least reliable links in the chain.**
> - **Doubao (seed models) responds very slowly** — the `doubao-seed-*` models can take 300-600s per long prompt and frequently time out on the first try (needs a retry), stalling the round. The turbo model is the only workable one for automated calls, and even it is slow.
> - **DeepSeek (deepcode) needs manual configuration** — the wrapper + settings file must be set up by hand before it works at all (see below); a fresh machine will not have it.
> - **If the experience is poor, just drop them: run Standard mode (4 CLIs: Claude/Codex/Gemini/Qwen + chair) instead of Deep.** The debate is fully valid without Doubao/DeepSeek — declare the reduced roster in the brief. Do not let two flaky panelists block or slow the whole session; a clean 4-panelist debate beats a stalled 6-panelist one.

- **DeepSeek** — the upstream `deepcode` CLI is TTY-locked, so debates use a non-interactive **`deepcode-panelist` wrapper** on the user's PATH. Setup: `npm i -g deepcode`, run it once interactively to generate its settings file (model + API key + base URL + reasoning effort), then place the wrapper script on PATH and make it executable. Config lives in the deepcode settings file. See references/panelists.md §6 for the wrapper and known-good defaults (effort=medium, max_output_tokens, proxy bypass).
- **Doubao (Volcengine Ark)** — `npm i -g @volcengine/ark-cli`, then `arkcli auth login volc-sso` (SSO device flow; the picker needs an interactive PTY). This writes an API key to the arkcli config file. Debates call the Ark Chat Completions REST endpoint directly with the **turbo** model (never the reasoning/seed model in automated calls — it times out). See the `volcengine-ark` skill for auth pitfalls and the safe-call recipe.

### 3. External advisor (Manus) — no install, one key
- Manus runs over the Hermes MCP channel + direct REST; there is no local CLI to install.
- The user must have `MANUS_MCP_API_KEY` set in the Hermes config so the chair can create/poll advisor tasks. Without it, the debate still completes but the final report notes "external advisor not reviewed".

### 4. Proxy note
- All panelist calls must bypass any local proxy (Clash/V2Ray etc.). The round scripts already prepend the proxy-bypass env/flags; if you run a call by hand, add the same bypass or long HTTPS calls will be killed.

## Pre-Game (mandatory before the first debate of each skill activation)

0. **Environment check** (first activation, new machine, or after any CLI failure): run `bash ~/.hermes/skills/conclave/scripts/install.sh`
   - Detects OS (macOS / Linux / WSL / Windows Git Bash) and Node.js/npm + all panelist CLIs; auto-installs anything missing (brew on macOS, apt/dnf/pacman on Linux, manual instructions on Windows).
   - Then audits each provider's auth material (existence only — no secrets read) and prints an ACTION checklist.
   - If any `[ACTION]` line appears: **STOP — ask the user to configure that provider's key/OAuth first** (exact steps in `references/panelists.md`). No debate until every provider is configured.
   - `--check-only` audits without installing.
1. **Initialize the arena**: run `bash ~/.hermes/skills/conclave/scripts/init_debate.sh <topic-slug>`
   - Auto-creates `~/.hermes/debates/conclave-YYYYMMDD-<slug>/`
   - Generates the full directory structure + starter template files (brief.md / mapping.md / constraints.md / index.md)
2. **Fill the brief**: write brief.md, mapping.md, and constraints.md under `01_brief/`.
3. **Version & parameter check**: see `references/panelists.md` (commands, parameters, auth pitfalls for each agent).
4. **Pre-flight (update + ignition)**: run `bash ~/.hermes/skills/conclave/scripts/preflight.sh <arena-path>`
   - Phase A: best-effort self-update of all panelist CLIs (failures are non-fatal and logged; `--skip-update` bypasses).
   - Phase B: ignition ping of all panelist agents (plus Manus, verified manually); results are auto-written to `00_preflight/preflight.log`.
   - Any ping failure: fix first (key / proxy / version), then debate.
5. **Launch the debate**: use `terminal(background=true)` to spawn the panelist CLIs in parallel, writing outputs to `02_r1/`.

## Arena Directory (one isolated folder per debate, auto-named)

**Root**: `~/.hermes/debates/` (persistent archive, not /tmp)
**Per-debate naming**: `conclave-<yyyymmdd>-<topic-slug>/`
  - Topic slug: 2-6 lowercase English letters/digits (e.g., `medlibya`, `pricingv2`)
  - Multiple debates on the same day append `-N` (e.g., `conclave-20260813-medlibya-2`)

**Auto-init**: run `scripts/init_debate.sh <topic-slug>` to generate the directory structure and print the path.

### Directory Structure

| Path | Purpose |
|------|---------|
| `00_preflight/` | Pre-flight ping results |
| `01_brief/` | Brief + anonymity mapping + user constraints |
| `02_r1/` | R1 positioning (all mode-dependent panelists in parallel) |
| `03_r2/` | R2 rebuttals |
| `04_r3/` | Convergence round 3 |
| `05_r4/` | Convergence round 4 |
| `06_r5/` | Convergence round 5 |
| `07_verdicts/` | Chair synthesis per round |
| `08_signoff/` | Final draft + individual votes |
| `09_deliver/` | Final report + meeting minutes |
| `index.md` | Full index: timeline, file map, key decisions |

### File Discipline
- **Long texts go to disk**; prompts only give paths — do not stuff long text into command-line arguments.
- **Every round's speeches must be written to the corresponding round directory**; do not just glance at terminal stdout.
- **Chair synthesis is mandatory after every round**, written to `07_verdicts/`; otherwise panelists in the next round do not get the divergence list.
- **Final report and minutes must land in `09_deliver/`**; also copy `final.md` to the debate root for easy discovery.

## Clarification Phase (mandatory before drafting the brief)

After receiving the topic and before writing the brief, the chair self-audits: is the topic ambiguous? Is any key constraint missing from the background?
- Any unclear point / multiple reasonable interpretations → **ask the user first; no debate until answered**.
- Questions must be multiple-choice (clarify tool, 2-4 options + Other); never make the user do essay questions; ask at most 4 critical ones at a time.
- After the user answers, write brief.md; the user's answers go into the brief's "Constraints" section as shared premises for all agents.
- If a trajectory-altering question arises mid-debate (e.g., a divergence hinges on a fact only the user knows) → the chair may pause, ask the user via clarify, append the answer to the brief, and resume.
- Do not force questions when there are none — if the topic is already clear, debate immediately; do not ritualize clarification.

## Brief Sign-off Gate (mandatory, user-mandated 2026-08-16)

**After writing brief.md and BEFORE launching R1, the chair MUST show the brief to the user and get explicit approval to proceed.** The brief is the shared premise every panelist argues from — a wrong or incomplete brief poisons the entire debate (all panelists faithfully propagate a bad premise; you only discover it after 30-50 CLI calls). Writing the brief is NOT permission to start.

- Paste the brief's key sections (topic, data pack, constraints, mode) into the reply, or give the path and ask the user to read it.
- Ask a direct go/no-go via clarify (approve-and-launch-R1 / needs-edits). No R1 launch until the user says go.
- If the user corrects anything, update brief.md, re-show, re-confirm.
- Applies to EVERY debate including follow-up/supplementary/sub-debates. Separate from the Clarification Phase: clarification fills gaps in the topic; this gate confirms the assembled brief is correct before spending the CLI budget.
- No exception — even an "obvious" topic gets a 10-second brief confirmation; it is far cheaper than a poisoned debate.

## Workflow (dynamic rounds, auto-partitioned into directories)

**Step 0 Init**: `bash ~/.hermes/skills/conclave/scripts/init_debate.sh <topic-slug>` → creates `~/.hermes/debates/conclave-YYYYMMDD-<slug>/`. All subsequent files land in this directory.

```
R1 Positioning   → agents in parallel, unseen by each other (prevent anchoring). Write to 02_r1/. Chair also writes a position.
R2 Rebuttal      → Each agent receives the other agents' R1 (anonymized). Task: identify ≥1 fatal flaw per opponent + self-defense. Write to 03_r2/.
R3+ Convergence  → Chair synthesizes consensus/divergence into 07_verdicts/verdict_rN.md; only divergence points are sent back.
                   Each agent must "concede" or "rebut with evidence"; equivocation is prohibited. Write to 04_r3~08_signoff/.
                   Termination may occur as early as R3 if strategic divergence is resolved and every objection carries an executable alternative.
                   Hard ceiling: 8 rounds (including R1 and R2).
```

Round reference files:
- `02_r1/` for each agent's positioning
- `03_r2/` for rebuttal speeches
- `07_verdicts/verdict_rN.md` for chair synthesis
- `08_signoff/final_draft.md` for sign-off draft
- `09_deliver/final.md` + `minutes.md` for final deliverables

Constructive Opposition Iron Rule (user-mandated, applies to all rounds):
- **Any objection / rebuttal must carry its own solution** — "what do you think is the correct approach?", executable, verifiable.
- Objection + reason without solution = invalid speech; the chair names and sends it back for rewrite; it does not count toward the round's output.
- When rebutting others in R2, you must give "how would you fix it"; in R3-R5, alternatives and new evidence are both mandatory.

## Convergence Rules (user-mandated)

### Round bounds
- Floor: 2 rounds (R1 + R2). High-risk topics (architecture, security,
  irreversible migration) floor: 3 rounds.
- Ceiling: 8 rounds, hard. Sub-debate rounds count toward this ceiling.
- Risk level is declared by the chair at the end of R1. If any panelist
  disputes the level, the topic is treated as high-risk. Default when
  unclear: high-risk.
- Termination evaluation begins only after the applicable floor round.
- Dynamic termination: the chair may terminate early when all remaining
  divergence points are parametric/executional and every objection carries
  an executable alternative. Hard floor still applies.

### Divergence ledger
Chair maintains after each round: item ID, description, level
(strategic / structural / parametric / executional), status
(open / resolved / suspended / accepted-risk), alternative, verifiable
resolution criterion, proposer, first-seen round.

### Termination (all four required)
1. No open strategic- or structural-level items.
2. The most recent round produced no new substantive disagreement
   (chair-classified; restatements of existing disagreements do not count).
   Any panelist may object once per round to the chair's "restatement, not
   new" classification. The objection forces the item into the ledger as
   open; the chair must then close it on substance, not on classification.
3. No admissible unresolved structural hold.
4. No user veto.

### Structural hold admissibility
- A structural hold must name (a) the affected interface, data-model
  field, or failure mode, and (b) a verifiable criterion under which it
  would be resolved. A hold missing either is recorded as parametric and
  does not block termination.
- Each panelist may have at most 2 active structural holds at a time.
- Release: proposer confirms downgrade, OR another panelist seconds the
  downgrade, OR — after the same hold has been re-asserted in two
  consecutive rounds with no new evidence — the chair overrules it with a
  written reason recorded in the ledger and carried into the sign-off.

### Forced close
Trigger, whichever comes first: (a) the ceiling round is reached, or
(b) two consecutive rounds add zero new strategic- or structural-level
items. On trigger the chair closes the debate and records every remaining
open item in the sign-off as a known unresolved risk with trigger
conditions and a rollback plan. Forced close is a valid termination.

### Stalemate
An item that stays strategic-level for two consecutive rounds with no
party conceding: chair must either (a) record it as accepted-risk with
trigger conditions and rollback plan, or (b) spin off a focused
sub-debate (max 2 rounds, relevant panelists only).

### Rollout (non-blocking)
Adopt immediately behind flag `convergence: dynamic` (defaults: floor
2/3, ceiling 8). Per debate, log: rounds used; the round at which the old
5-round rule would have stopped; every strategic/structural item first
seen after round 2. Review after 10 logged debates.
Escape defect := a strategic- or structural-level item first seen in a
round that the compared rule would have cut, AND which later required a
post-sign-off change.

Sign-off (not counted as a round):
- Final draft sent to all agents; each may only reply `Agree` or `Oppose + specific clause + specific reason + own alternative`.
- **Destruction without construction = invalid vote (user-mandated)**: opposition must give an executable alternative; votes lacking one are void, treated as abstentions, and the chair proceeds with the remaining valid votes.
- Unanimous pass → external advisor review.
- Opposition & rounds remain → extra round targeting the objection reason and alternative; rounds exhausted → chair adjudicates, alternative appended to minority opinion.

External Advisor (Manus):
- Send final draft + round summaries; ask: any fatal-level objections?
- If yes → chair judges: valid → extra round (if rounds exhausted, disclose the objection and adjudication reason in the final); invalid → written rejection with reason in the final.
- If no → deliver.

## Anonymity Rules

- In R2 rebuttals and convergence rounds, all speeches are signed "Panelist A~E"; no identity clues allowed.
- mapping.md is generated by the chair and kept secret for the session; the user may inspect it at any time.
- Chair synthesis quotes only "Panelist X"; the final report may disclose real-name stances (user requests transparency).

## Disconnection Rules (user-mandated: explicit retry count)

- **Per-agent per-round maximum: 2 calls** (1 original + 1 retry). No infinite retry loops.
- First failure (timeout / 401 / crash / empty output / max-turns reached) → **immediate retry**.
  - If the failure is parameter-related (e.g., Claude "Reached max turns"), **adjust the parameter first** (raise `--max-turns`, add `--allowedTools ''`, etc.) before retrying. This corrected call counts as the retry.
  - Otherwise, use an identical retry.
- Second consecutive failure → mark that agent **absent for that round**. Debate continues; final report notes absent party and reason; fix after the session, restore for the next debate.
- Chair (Hermes) never disconnects; Manus advisor timeout 30 min → skip advisor, final report notes "external advisor not reviewed".
- **WAIT FOR ALL PANELISTS BEFORE THE FINAL STEP (user-mandated 2026-08-16).** Do NOT run the convergence verdict / final draft / sign-off / deliverables until every panelist's output for the round has actually arrived (or been formally marked absent after 2 failures per the rule above). Slow panelists — especially Doubao seed models (300-600s, frequent first-try timeout) and DeepSeek — must be waited out with `process(action='wait')`, not skipped early. Closing the round while a panelist is still legitimately in flight is a process violation: their content can change the verdict, and you will have to redo the final step. "Slow" ≠ "absent": absent requires 2 real failures, not just being late.

## Language Rule (user-mandated)

- The debate language must match the user's current session language. The chair sets this in the brief's `Language` field.
- All agents (including the chair) must output in that language; English defaults are overridden.
- If the user switches language mid-session, the brief is updated and all subsequent rounds follow the new language.

## Parameter Rules

- Codex default `-c model_reasoning_effort="medium"` (cost/speed balance); user calls "important session" for xhigh.
- Codex exec is a read-only sandbox; file writes are rejected → prompts must require "full text to stdout", and the chair extracts from process logs to disk.
- Claude uses `-p --max-turns 1`; Gemini uses `-p`; Qwen uses `-p`. All non-interactive; no TUI.
- Prompts for the agents are identical word-for-word except the role sentence, ensuring fairness.

## Deliverables (two items, both mandatory)

### 1. final.md (decision document, `09_deliver/final.md`)
1. **First paragraph: dry conclusion**. 3-5 sentences in plain language: what is the final opinion, what to do, one key risk. No fluff, no jargon stacking.
2. Consensus list (items all agents agree on).
3. Divergence & adjudication: each point → each agent's stance (real name disclosed) → chair ruling + reason.
4. Minority opinions (if any) verbatim appendix.
5. External advisor opinion and handling result.
6. Absence / exception notes (if any).

### 2. minutes.md (process document, `09_deliver/minutes.md`)
Recap how the debate reached the final report:
1. Opening: topic + clarification answers / rulings + how each shaped the outcome.
2. Roster & anonymity mapping (real names disclosed).
3. Round-by-round evolution: R1 multi-way stance comparison → R2 what got killed (who struck) → R3-R5 how divergence closed → sign-off round what each objection turned into.
4. Kill list: rejected solutions / categories + cause of death + who struck.
5. Agent contributions & evaluation (real names).
6. Minority opinion archive.
7. File index (source paths per round).

Give the user the absolute paths of `09_deliver/final.md` and `09_deliver/minutes.md`, and paste the first paragraph of final in the reply.

### 3. index.md (debate root directory)
After each debate, auto-generate `index.md` in the debate root:
- Topic, date, participants
- Timeline: R1 → R2 → convergence → sign-off → advisor, timestamps per step
- File map: pointers to round sources
- Key decision quick-reference
- Info usable for `@session` restarts

This index lets the user find key decisions in 10 seconds even after 3 months.

### 4. Post-debate export to the user's working directory (mandatory, user-mandated 2026-08-14)

After every debate, copy the ENTIRE arena directory (not just `09_deliver/`) into the session's current working directory, preserving the arena folder name:

```bash
cp -R ~/.hermes/debates/conclave-YYYYMMDD-<slug> "$PWD/"
diff -r ~/.hermes/debates/conclave-YYYYMMDD-<slug> "$PWD/conclave-YYYYMMDD-<slug>" && echo "COPY VERIFIED"
```

- The diff verification is mandatory; report file count, total size, and the destination absolute path.
- `~/.hermes/debates/` remains the canonical archive; the working-directory copy is the user's working artifact.
- If the user only asks for "the results", still export the full arena — briefs, round sources, verdicts, and votes are all part of the deliverable.
- **Security warning**: the exported arena contains the full raw debate content (briefs, agent outputs, mapping). Do not run Conclave inside directories that are auto-synced to public repositories, cloud backups, or shared drives unless you want that content synchronized. Export to an isolated directory or delete the copy after review.

### 5. One debate = one self-contained folder; follow-up debates get a NEW folder (user-mandated 2026-08-14)

- **Consolidation**: at debate close, ALL files of the session (brief, constraints, mapping, preflight log, every round's raw+cleaned speeches, verdicts, sign-off votes, final.md, minutes.md, index.md) must live inside the single arena folder. No strays in /tmp, no loose copies elsewhere — the exported folder in the user's cwd is the complete, self-contained record.
- **Follow-up / supplementary debates**: if the user later asks to continue, extend, or re-debate the same topic, do NOT reopen or append into the old arena. Run `init_debate.sh` again to create a fresh arena (same-day same-slug auto-appends `-N`, e.g. `conclave-20260814-burrypltr-2`), and put the previous arena's absolute path into the new `01_brief/brief.md` under a "Prior debate" heading so panelists can read the old final.md as input context. The old folder stays frozen as the historical record; the new debate's export goes to a separate folder in the cwd.

## Chair Neutrality Red Line

- Synthesis must not weight a point just because the chair proposed it; chair views struck down must still be recorded under "rejected positions".
- Rulings must cite round-source evidence (file + line number); no impressions allowed.
- If the user disagrees with a ruling → the user's word is the supreme arbiter; the chair writes the user's opinion into the final report marked "user adjudication".

## Consensus Protocol v1.1 (2026-08-14, supersedes ad-hoc aggregation)

The chair MUST follow `references/consensus-protocol-v1.md` (v1.1). Operational deltas from the classic workflow:

1. **Modes**: Quick = 2 CLIs + Hermes (Claude + Gemini); Standard = 4 CLIs + Hermes (Claude/Codex/Gemini/Qwen); Deep = 6 CLIs + Hermes (all panelists). Declare the mode in the brief; user may override.
2. **Structured R1**: prompts require a claims/evidence/assumptions/uncertainties block before free text.
3. **Claim table**: verdicts must carry a claim-level table with source-overlap dedup (two agents citing one source = one independent evidence).
4. **Divergence triage**: next-round prompts target only the top 1-2 decision-relevant claims (flip test first, then divergence, then evidence obtainability) — never re-ask whole questions.
5. **Stopping**: Decision-Flip Value proxy (continue only if an open claim can flip the decision AND its expected loss reduction exceeds round cost); hard floor/ceiling rules remain as guardrails.
6. **Manus triggers**: verifiable-fact dependence, R1 unanimity (herding check), critical dissent, time-sensitive topics. REST polling path (references/panelists.md).
7. **Dissent**: expected-loss triage Dᵢ = P(Fᵢ) × Impact(Fᵢ), self-reported P discounted ×0.5 (heuristic); Dᵢ > 10% of value at stake forces a targeted round or Manus check.
8. **Aggregation**: normalized weights + log-odds pool + N_eff report (default ρ 0.6 same-family / 0.3 cross-family, HEURISTIC); label all pooled probabilities "uncalibrated" until calibration.jsonl has ≥30 resolved predictions.
9. **Calibration log**: append verifiable predictions only (with check dates) to `~/.hermes/debates/calibration.jsonl`; resolve due entries at the start of each new debate. Never score non-verifiable judgments.
10. **final.md additions**: mode, N_eff (labeled), claim table, baselines (majority + equal-weight), dissent triage, Decision State block (Belief/Consensus/Confidence/Decision/Robustness), why-stopped block, rigor tags on every soft number.
11. **Terminal states include NO CONSENSUS — INSUFFICIENT EVIDENCE and DEBATE_FAILED**; emitting them to prevent a bad decision is success.
12. **Manus dual mode**: Blind Reality Check (sees only the question, never council output) vs Draft Review (post-sign-off). Never merge.
13. **Phase gates**: N<30 resolved predictions → equal weights only; 30-100 → offline research, no live weight changes; ≥100 → learned aggregation only if it beats equal-weight baseline out-of-sample.

## Field Lessons (2026-08-12 Libya sourcing session)

1. **External advisor opinions must carry a version number**: Manus reviewed an old draft; half its opinions were already resolved — attach a version number when sending the advisor task, and require the first line of the opinion to state the reviewed version; otherwise you waste a round.
2. **Audit-type panelist (e.g., Claude) objection depth increases per round**: structure → parameters → footnotes, always able to dig deeper. The chair must adjudicate closure when "objections have degraded to parameter-level and alternatives are directly absorbable"; otherwise there is no convergence. Closure standard: no strategic-level divergence + all objections have absorbable alternatives.
3. **`claude -p --max-turns 1` occasionally reports "Reached max turns"**: when retrying per disconnection rules, raise `--max-turns` to 3-10 (add `--allowedTools ''` to prevent spinning); do not stick to the original parameter.
4. **CLI stdout handling**: CLI stdout mixes ANSI codes and shell startup noise (local shell rc plugin errors); normalize with regex before anonymizing, otherwise read_file may judge the file binary.
5. **R1 same direction = high-confidence signal**: when agents independently position unseen, if they independently pick the same direction / same approach, that judgment's credibility maxes out; synthesis can directly promote it to "consensus" without further debate. Conversely, points where R1 diverges are real divergence, worth spending round budget on.
6. **Session cost & pace expectation**: one full Conclave session (clarification → R1 → R2 → convergence → sign-off × N) is roughly 30-50 CLI calls, 1.5-3 wall-clock hours. Codex medium/low effort is fast enough; Claude long answers may take 10+ minutes per session. Run everything in background parallel + notify_on_complete; the chair writes its own draft while waiting.
7. **Highest-value use of audit-type panelist**: let the most rigorous panelist's (this session was Claude) objections directly rewrite final numbers, not just serve as QC — this session's six fatal arithmetic errors + one payment reallocation (breakeven 93% → 86%) all came from its opposition votes.

## Field Lessons (2026-08-13 Self-optimization session)

8. **Self-debate is valid and efficient**: Using Conclave to optimize its own SKILL.md produced actionable output in 3 rounds. The chair must be willing to concede ground when the audit-type panelist's objections are structurally sound.
9. **Shell parameter escaping is a real failure mode**: Multi-line prompts containing backticks (e.g., markdown code blocks) passed through `zsh -i -c "..."` are interpreted as command substitution by the outer shell. Use Python `subprocess` with `shlex.quote`, or strip backticks from prompts.
10. **Codex exec sandbox + shell expansion trap**: Wrapping a prompt in single quotes prevents `$(cat file)` expansion; Codex receives the literal string. Always use double quotes for shell expansion when passing file content inline.
11. **Merge minority alternatives rather than overrule**: Claude and Qwen both opposed the chair's R3 draft but provided full rewritten text. Merging their specific amendments (ceiling 8, forced close, hold admissibility, classification appeal) produced a better final rule than either the original proposal or a pure adjudication.
12. **Dynamic termination proved itself in practice**: This debate reached strategic convergence after R2; R3 functioned as a sign-off round. Total 3 rounds vs. the old fixed 5, validating the mechanism we were designing.

## Field Lessons (2026-08-14 Burry AI-bubble debate)

13. **Assign each panelist their letter explicitly in R2+ prompts**: Asking panelists to "recognize your own R1 stance" in the anonymized bundle failed — three of the panelist CLIs misidentified themselves as Panelist A (the strongest position) in both R2 and R3. The persuasion was genuine, but the minutes had to log an anomaly. Fix: in R2+ prompts, state "You are Panelist X" directly; anonymity is preserved because the mapping file still hides which real CLI is X.
14. **Chair-fetched live data beats panelist estimates**: The chair pulled real option quotes mid-debate (PLTR 150/120 spread $7.20 vs panelist-estimated $7.00; ORCL 140/110 $10.90 vs estimated $8.00 — a 36% miss). The real numbers directly changed the final contract counts. For any debate touching market/pricing data, the chair should inject a verified data pack into the brief AND re-verify before the final draft.
15. **A GTC limit order can merge two opposing positions**: "Execute now" vs "wait for a dip" deadlocked until the chair ruled "place the order now at a limit price that only fills on a dip" — both sides' logic satisfied, zero round cost. When two panelists differ only on timing, look for an order-type / trigger mechanism that encodes both.

## Field Lessons (2026-08-14 Naked-leg supplementary debate)

16. **Manus advisor works via direct REST polling — no webhook needed**: The MCP channel only exposes create_task, but the same API key (MANUS_MCP_API_KEY in config.yaml) works against `https://api.manus.im/v1/tasks` directly: POST to create (`{"prompt": ..., "taskMode": "chat"}`), then GET `/v1/tasks/{task_id}` every 60s until `status == "completed"`; the advisor's answer is in `output[].content[].text` where `role == "assistant"`. Review came back in ~3 minutes with 5 findings (3 absorbed, 1 softened, 1 rejected). This fully replaces the webhook/user-paste fallback on CLI-only machines.
17. **Explicit role assignment in prompts works**: R2/R3 prompts stating "You are Panelist X" (lesson 13) eliminated the identity-misrecognition anomaly entirely — all panelist CLIs defended their own positions.
18. **A rich data pack changes debate quality**: Providing 3 expiries × multiple strikes of real option quotes + earnings calendar in the brief let panelists do arithmetic kills (e.g., "Nov-20 contract = -70% residual at forced 11-02 exit") instead of opinion wars. For market debates, the data pack IS the debate.
19. **Users amend mid-debate — route through constraints, not prompts**: The user's mid-turn message ("rolling allowed, must use Manus API") was appended to constraints.md as shared premises rather than editing live round prompts, keeping all agents on identical instructions.

## Field Lessons (2026-08-16 Surgical sub-debate — two process violations)

20. **A follow-up/sub-debate is a NEW arena, never a subfolder of the old one (violation + fix).** When the user asked to re-evaluate one SKU (surgical instruments) after the main debate closed, the chair wrongly created `conclave-20260815-medv9/10_subdebate_surgical/` inside the frozen main arena. This breaks §5 "follow-up debates get a NEW folder": the old arena must stay frozen as history, and the new debate must be self-contained. Fix: run `init_debate.sh <slug>` for a fresh `conclave-YYYYMMDD-<newslug>/`, move ALL sub-debate files into its standard dirs (task→02_r1/r1_task.md, each panelist→02_r1/, verdict→07_verdicts/verdict_r1.md, decision→09_deliver/final.md+minutes.md, +index.md), put the prior arena's absolute path in the new brief under "Prior debate", delete the wrongly-placed subfolder from BOTH the canonical archive and the working-directory export, then export the new arena fresh. Rule of thumb: if you're about to `mkdir` anything other than the 10 standard dirs inside an arena, STOP — you want a new arena instead.
21. **Brief sign-off gate (see the dedicated section).** Even a single-SKU sub-debate must show its brief to the user for go/no-go before launching R1. Skipping it risks running the whole sub-debate on a premise the user would have corrected in one sentence.
22. **A sub-debate can legitimately compress the workflow but still owes full deliverables.** A single parametric sub-question can be R1-only (independent positioning) + chair convergence, skipping anonymous R2/sign-off/Manus — but it still must land final.md + minutes.md + index.md in its OWN new arena. Do NOT back-fill the result into the parent's final.md in place (see lesson 23); if a merged view is wanted, write it to a NEW file. The sub-debate arena + a pointer is the record; the parent stays frozen.

## Field Lessons (2026-08-16 Surgical RE-debate — repeat violations, user escalated)

23. **NEVER edit a prior debate's files — this was violated TWICE and the user escalated.** When a follow-up debate produces a result that affects the parent plan, the temptation is to edit the parent's final.md in place. DO NOT. The parent arena is frozen history. Correct pattern: (a) the follow-up lives entirely in its own new arena; (b) if the user wants a merged/updated plan, create a NEW file (e.g. `final_vN+1.md` or a fresh merged arena) and paste the combined result there, leaving the old final.md untouched. Only edit the parent's file if the user explicitly says to. Rule of thumb: after any follow-up debate, ask "does the user want the parent updated in place, or a new merged file?" — default to a new file. (First violation: sub-debate placed as a subfolder. Second violation: back-filled edits into the parent final.md without being asked. Both drew explicit user correction.)
24. **"Wait for all panelists" applies doubly to the final step (see Disconnection Rules).** In this same session the chair issued the convergence verdict before Doubao's (slow) output had arrived, treating late as absent. Late ≠ absent. Wait with `process(action='wait')` until every panelist's file is non-empty or has 2 logged failures, THEN converge.
