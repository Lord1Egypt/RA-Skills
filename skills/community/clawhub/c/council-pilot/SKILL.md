---
name: council-pilot
description: >-
  Fully autonomous expert forum builder and project maturity engine.
  User delivers an idea, auto-distills domain experts from web sources,
  builds knowledge base with breadth/depth/thickness/effectiveness,
  scores maturity (0-100), builds project code, debugs, re-scores in
  adversarial loop until 100/100, then submits to GitHub.
  Composes research-loop, GAN-style agents, council deliberation,
  and verification-loop patterns.
  TRIGGER when: user provides an idea/concept/domain and wants expert-driven
  project built end-to-end; or says "distill experts", "expert forum",
  "build with experts", "maturity loop", or "full auto build".
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - gh
    emoji: "\U0001F3DB"
    homepage: https://github.com/wd041216-bit/council-pilot
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
model: opus
argument-hint: "<domain-or-idea> [--target-repo URL] [--max-iterations N] [--quick]"
---

# Council Pilot — Autonomous Pipeline

Build a fully automated expert-driven project from a single idea. The pipeline discovers experts, distills their public knowledge, forms a council, scores maturity, builds code, debugs, and iterates until the council awards 100/100. Then submits to GitHub.

## Core Rule

Distill methods, evidence preferences, reasoning habits, critique patterns, and blind spots from PUBLIC sources only. Do NOT impersonate living persons, invent private beliefs, fabricate quotes, or treat expert profiles as primary evidence. Expert memory is an analysis lens, not truth.

## Quick Start

```
# Full autonomous pipeline
python3 scripts/expert_distiller.py init --root ./forum --domain "AI Reliability" --topic "LLM hallucination detection"
```

Then invoke this skill with the domain idea. The skill handles everything from discovery to GitHub submission.

## Autonomous Pipeline: 10 Phases

Phases 1-4 run once (setup). Phases 5-9 iterate until convergence. Phase 10 runs once at completion.

```
INIT → DISCOVER → DISTILL → COUNCIL → SCORE
                                        │
                             score < 100│
                                        ▼
          GAP_FILL ← RESCORE ← DEBUG ← BUILD
              │
              │ needs new experts
              ▼
           discover single → distill single → update council
              │
              │ score = 100 + all pass
              ▼
           SUBMIT (terminal)
```

### Phase 1: INIT

**Goal**: Parse user idea into domain spec, initialize forum root.

**Steps**:
1. Parse the user's idea/concept into a domain name and topic description
2. Run CLI:
   ```bash
   python3 scripts/expert_distiller.py init --root <forum_root> --domain "<domain>" --topic "<topic>"
   ```
3. Initialize pipeline state:
   ```bash
   python3 scripts/expert_distiller.py build --root <forum_root> --domain "<domain>" --target-repo "<repo>"
   ```
4. Write the domain's `coverage_axes` — list 3-8 sub-domains the forum should cover

**Output**: Initialized forum root with `domains/<domain_id>.json`, directory layout, `pipeline_state.json`

**Transition**: → DISCOVER

### Phase 2: DISCOVER

**Goal**: Web-search for expert candidates (3-8 people).

**Steps**:
1. Generate search queries from the domain topic (see `agents/expert-researcher.md`)
2. For each query, use the current environment's web search tool to search
3. For each result, use the current environment's web fetch/open tool to read candidate pages
4. Identify real public figures with domain expertise
5. Collect source URLs classified by tier (A/B/C per `references/source-gates.md`)
6. For each candidate, run CLI commands:
   ```bash
   python3 scripts/expert_distiller.py candidate --root <root> --domain <domain> --name "<Name>" --reason "<why>"
   python3 scripts/expert_distiller.py source --root <root> --expert-id <id> --tier A --title "<Title>" --url "<URL>" --note "<Note>"
   python3 scripts/expert_distiller.py source --root <root> --expert-id <id> --tier B --title "<Title>" --url "<URL>" --note "<Note>"
   ```

**Gate**: At least 3 candidates with at least 1 Tier A + 1 Tier B source each

**Output**: `candidates/<id>.json` + `source_dossiers/<id>.json` for each candidate

**Transition**: → DISTILL

### Phase 3: DISTILL

**Goal**: Audit candidates, promote, fill profiles with LLM-driven distillation.

**Steps**:
1. For each candidate, run audit:
   ```bash
   python3 scripts/expert_distiller.py audit --root <root> --expert-id <id>
   ```
2. For candidates that pass audit (`promotion_allowed: true`), create profile:
   ```bash
   python3 scripts/expert_distiller.py profile --root <root> --domain <domain> --expert-id <id> --name "<Name>"
   ```
3. For each promoted expert, fill the profile by reading source content:
   - Read source URLs with the current environment's web fetch/open tool
   - Extract career arc, reasoning patterns, critique styles, blind spots
   - Write the filled profile to `experts/<id>/profile.json`
   - Write the distillate markdown to `experts/<id>/distillate.md`
   - Follow the contract in `references/profile-contract.md`
4. Rebuild index:
   ```bash
   python3 scripts/expert_distiller.py index --root <root>
   ```

**Gate**: At least 2 experts with fully filled profiles

**Output**: `experts/<id>/profile.json` + `experts/<id>/distillate.md` for each promoted expert

**Transition**: → COUNCIL

### Phase 4: COUNCIL

**Goal**: Form expert council with auto-assigned roles.

**Steps**:
1. Create council:
   ```bash
   python3 scripts/expert_distiller.py council create --root <root> --domain <domain> --name "<Domain> Main Council"
   # Optional: --experts id1,id2,id3 to specify which experts (default: all)
   ```
2. Review the auto-assigned roles (chair, reviewer, advocate, skeptic)
3. If needed, manually adjust with `council add-member --role <role>`

**Output**: `councils/<council_id>.json` with members, roles, weights, routing rules

**Transition**: → SCORE (first pass)

### Phase 5: SCORE (First Pass)

**Goal**: Initial scoring — all axes start at 0 (no artifact exists).

**Steps**:
1. Run score command:
   ```bash
   python3 scripts/expert_distiller.py score --root <root> --domain <domain>
   ```
2. This first pass records baseline 0/100 — everything needs building

**Output**: `scoring_reports/<domain>_<timestamp>.json` with total=0

**Transition**: → BUILD (always needs work on first pass)

### Phase 6: BUILD

**Goal**: Generate project code guided by expert lenses, targeting weakest axes.

**Steps**:
1. Read the scoring report to identify weakest axes
2. For each expert in the council, extract build guidance:
   - `reasoning_kernel.core_questions` — what they'd ask
   - `reasoning_kernel.preferred_abstractions` — what concepts they use
   - `advantage_knowledge_base.anti_patterns` — what to avoid
   - `domain_relevance.best_used_for` — where they add value
3. Generate code that:
   - Addresses the specific gaps from the scoring report
   - Uses patterns experts would approve
   - Avoids anti-patterns experts would flag
   - Follows expert testing and quality preferences
4. Write code to the target repo path
5. Record build context:
   ```bash
   python3 scripts/expert_distiller.py build --root <root> --domain <domain> --target-repo <repo_path>
   ```

**Agent**: Use `project-builder` agent for code generation

**Output**: Project source code at target repo path

**Transition**: → DEBUG

### Phase 7: DEBUG

**Goal**: Verification loop — build, types, lint, tests, security, diff.

**Steps**:
1. **Build**: Run the project's build command. Fix failures.
2. **Type Check**: Run type checker. Fix errors.
3. **Lint**: Run linter. Fix warnings.
4. **Tests**: Run test suite. Fix failures.
5. **Security**: Scan for secrets, injection, OWASP top 10.
6. **Diff Review**: Check for regressions and scope creep.

For each stage failure:
- Max 3 retries per failure type
- Tag failure with impacted scoring axis (see `references/build-integration.md`)
- If 3 retries exhausted, feed failure to GAP_FILL

**Agent**: Use `project-builder` agent for build failure fixes

**Transition**:
- All PASS → RESCORE
- Any FAIL (after retries) → GAP_FILL with failure details

### Phase 8: RESCORE

**Goal**: Full 4-axis scoring with council debate protocol.

**Steps**:
1. Run score command against the artifact:
   ```bash
   python3 scripts/expert_distiller.py score --root <root> --domain <domain> --artifact <repo_path>
   ```
2. For each axis, apply expert council debate (see `references/council-protocol.md`):
   - Each expert scores independently using their reasoning kernel
   - Skeptic challenges high scores (>20)
   - Advocate affirms low scores (<15)
   - Compute weighted median per axis
3. Sum axes for total (0-100)
4. Update pipeline state with new scores
5. Generate report:
   ```bash
   python3 scripts/expert_distiller.py report --root <root> --domain <domain> --format markdown
   ```

**Agent**: Use `maturity-scorer` agent for adversarial scoring

**Output**: Updated `scoring_reports/<domain>_<timestamp>.json`

**Transition**:
- total = 100 + verification all PASS → SUBMIT
- total < 100 → GAP_FILL
- Score regression (>10 point drop) → PAUSE and flag

### Phase 9: GAP_FILL

**Goal**: Analyze gaps, add experts if needed, determine build focus.

**Steps**:
1. Run coverage analysis:
   ```bash
   python3 scripts/expert_distiller.py coverage --root <root> --domain <domain>
   ```
2. Analyze scoring report for specific gaps per axis
3. Determine action:
   - **Missing expertise** → DISCOVER single candidate (fast-track), DISTILL, add to council:
     ```bash
     python3 scripts/expert_distiller.py council add-member --root <root> --council-id <id> --expert-id <new_id> --fast-track
     ```
   - **Knowledge gaps** (no new expert needed) → BUILD with focus on specific gaps
   - **Score regression** → Revert to previous approach, BUILD differently
4. Update pipeline state history

**Agent**: Use `gap-analyst` agent for coverage analysis

**Output**: `gap_analyses/<domain>_<timestamp>.json` with recommendations

**Transition**: → BUILD (next iteration)

### Phase 10: SUBMIT

**Goal**: Submit converged artifact to GitHub.

**Steps**:
1. Run final verification (all 6 stages must PASS)
2. Generate final report:
   ```bash
   python3 scripts/expert_distiller.py report --root <root> --domain <domain> --format markdown --output MATURITY_REPORT.md
   ```
3. Create git branch: `council-pilot/<domain_id>`
4. Commit all changes with format:
   ```
   feat(council-pilot): <domain> maturity 100/100

   Breadth: 25/25 | Depth: 25/25 | Thickness: 25/25 | Effectiveness: 25/25
   Expert council: <council_name> (<expert_count> experts)
   Iterations: <iteration_count>
   ```
5. Push branch and create PR:
   ```bash
   git push -u origin council-pilot/<domain_id>
   gh pr create --title "Expert-Distilled: <domain>" --body-file MATURITY_REPORT.md
   ```
6. Update pipeline state: `status: submitted`

**Output**: GitHub PR URL

**Transition**: Terminal (pipeline complete)

## Convergence Criteria

The pipeline terminates ONLY when ALL conditions are met:

1. Maturity score = 100 (breadth=25, depth=25, thickness=25, effectiveness=25)
2. Verification loop: all 6 stages PASS
3. No coverage gaps flagged by gap analyst
4. Council consensus that artifact is submission-ready

A score of 100 means the expert council cannot find meaningful improvements. This is intentionally hard to achieve.

## Loop Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--max-iterations` | 10 | Maximum BUILD→DEBUG→RESCORE cycles |
| `--target-repo` | current dir | Where to build the project |
| `--quick` | false | Reduce to 2 experts, max 3 iterations |

## State Persistence

Pipeline state is stored in `<root>/pipeline_state.json`:
- Current phase, iteration count, score history
- Target repo, GitHub branch, active council
- Experts added mid-loop (flagged for later review)
- Build failures and score regressions

Each iteration reads state at start, writes at end. Context can be safely compacted between iterations.

## Dynamic Expert Addition

The pipeline can add new experts mid-loop:
1. Gap analyst identifies uncovered sub-domain
2. Expert researcher discovers 1-2 targeted candidates (fast-track)
3. Minimum viable sources collected (1 Tier A + 1 Tier B)
4. Abbreviated audit → skeleton profile → add to council
5. Fast-tracked experts start with weight cap 0.2 (vs 0.3)
6. After 2 scoring cycles, fast-track flag is removed

Maximum 2 new experts per iteration. Total council size must not exceed 10.

## Failure Recovery

| Failure | Recovery |
|---------|----------|
| Max iterations reached | Pause, generate report, print current state |
| Build failure after 3 retries | Log failure, continue to GAP_FILL |
| Score regression (>10 points) | Pause, revert to previous artifact |
| Context window pressure | Write state to disk, compact, resume |

## Search Tools

Use whichever web research surface is available in the active agent runtime:
- In Codex, use the built-in web search/open workflow when current public sources are needed.
- In Claude Code, use configured web-search MCP tools if they are installed.
- If no web tool is available, run `discover --from-file` with a curated JSON source list and mark the run as source-file assisted.

## Safety and Trust

- Require at least one Tier A and one Tier B source before promotion
- Never use Tier C sources to define core beliefs, bio_arc, signature_ideas, critique_style, or quote_bank
- Mark stale or weakly sourced fields as tentative
- Preserve source refs and freshness metadata with every profile
- Downgrade conclusions that rely only on expert memory
- Never fabricate quotes — all quotes must be verbatim or clearly marked as paraphrases with source attribution
- Expert memory is an analysis lens, not primary evidence

## Fast Commands (Manual Mode)

All CLI commands work standalone without the autonomous pipeline:

```bash
# Initialize
python3 scripts/expert_distiller.py init --root ./forum --domain "My Domain" --topic "Description"

# Add candidate and sources
python3 scripts/expert_distiller.py candidate --root ./forum --domain "my-domain" --name "Expert Name" --reason "Why"
python3 scripts/expert_distiller.py source --root ./forum --expert-id expert-name --tier A --title "Source" --url "https://..." --note "Note"

# Audit, profile, validate
python3 scripts/expert_distiller.py audit --root ./forum --expert-id expert-name
python3 scripts/expert_distiller.py profile --root ./forum --domain "my-domain" --expert-id expert-name --name "Expert Name"
python3 scripts/expert_distiller.py validate --root ./forum --strict

# Council management
python3 scripts/expert_distiller.py council create --root ./forum --domain "my-domain"
python3 scripts/expert_distiller.py council list --root ./forum
python3 scripts/expert_distiller.py council show --root ./forum --council-id my-domain-main

# Scoring and analysis
python3 scripts/expert_distiller.py score --root ./forum --domain "my-domain" --artifact ./project
python3 scripts/expert_distiller.py coverage --root ./forum --domain "my-domain"
python3 scripts/expert_distiller.py report --root ./forum --domain "my-domain" --format markdown

# Discovery and maintenance
python3 scripts/expert_distiller.py discover --root ./forum --domain "my-domain" --from-file candidates.json
python3 scripts/expert_distiller.py refresh --root ./forum --stale-only
```
