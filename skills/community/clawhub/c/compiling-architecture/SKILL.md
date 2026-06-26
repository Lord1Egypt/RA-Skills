---
name: compiling-architecture
description: "Use when: user wants to select architecture patterns, compile a spec, iterate on constraints/NFRs, audit why patterns were selected/rejected, or finalise an architecture for implementation. Not when: no repeatable decisions needed, or constraints/NFRs are not yet known (gather those first)."
tags: [architecture, nfr, cost, patterns, deterministic, governance]
version: 1.0.2
homepage: https://github.com/inetgas/arch-compiler
metadata: {"hermes":{"tags":["deterministic-compiler","architecture-as-code","architecture-design-patterns","software-architecture-patterns","architectural-decision-records","architecture-trade-off-considerations","cost-optimization","nfr-enforcement"],"category":"devops","requires_toolsets":["terminal"]},"openclaw":{"homepage":"https://github.com/inetgas/arch-compiler"}}
---

# Architecture Compiler

## Overview

A deterministic compiler that selects architecture design patterns from a canonical YAML spec. No LLM, no hidden defaults — same input always produces the same output. All architectural logic lives in pattern files; the compiler is intentionally simple.

---

## Repo Structure — Read This First

Treat the compiler repo as having this contract:

```text
arch-compiler/
├── README.md
├── AGENTS.md
├── README-AGENTS.md
├── tools/        <-- read-only for agents
├── schemas/      <-- read-only for agents
├── config/       <-- read-only for agents
├── scripts/      <-- read-only for agents
├── patterns/     <-- read-only for agents
└── skills/
    ├── using-arch-compiler/
    │   └── SKILL.md
    ├── compiling-architecture/
    │   └── SKILL.md
    └── implementing-architecture/
        └── SKILL.md
```

Before acting:

1. Read `AGENTS.md` for repo-wide agent rules and boundaries.
2. Read this `SKILL.md` for the task-specific workflow.
3. Treat `tools/`, `schemas/`, `config/`, and `patterns/` as read-only unless the human explicitly asks for compiler-maintenance work in this repo.
4. Use this skill only to turn human inputs and constraints into approved architecture artifacts. Do not use it to implement application code.

The important split is:
- `AGENTS.md` = global agent rules for this repo
- `skills/using-arch-compiler/SKILL.md` = workflow router
- `skills/compiling-architecture/SKILL.md` = how to compile and finalise architecture
- `skills/implementing-architecture/SKILL.md` = how to implement an already-approved architecture

---

## When to Use

- You have a project spec (constraints, targets for nfr/operating_model/cost) and need to select appropriate architecture patterns
- You want reproducible, reviewable architecture decisions (same spec → same patterns, every time)
- You are iterating progressively on a spec — starting minimal and adding constraints over time
- You need to audit why specific patterns were selected or rejected
- You want cost feasibility analysis
- You have an existing prototype or codebase and need to compile, validate, or re-approve the architecture it should converge to
- Implementation or refactoring uncovered architecture drift, and you need to update the spec and recompile before coding continues

## When NOT to Use

- You need generative or creative architecture suggestions (use an LLM directly)
- You are designing a one-off system with no need for repeatability
- The constraints, targets for nfr/operating_model/cost aren't supported by schemas (check `schemas/` first)
- You want patterns that account for business logic or domain-specific rules not expressible in the spec schema (check `schemas/` first)
- Do not treat an existing prototype or codebase as architectural authority by default. Existing code is evidence about current reality, not approval of future architecture.
- Do not use this skill to retroactively bless accidental prototype choices without making them explicit in the spec and obtaining approval.

## Session-Start Checklist

Run these checks before writing any spec file, compiling anything, or creating any architecture artifact.

1. **Verify the compiler repo is installed in a stable location**

   Use a persistent path, not `/tmp/`. The canonical examples in this skill assume one of:

   - Codex: `~/.codex/arch-compiler`
   - Claude Code: `~/.claude/arch-compiler`

   Verify one of them exists:

   ```bash
   ls ~/.codex/arch-compiler/tools/archcompiler.py
   ls ~/.claude/arch-compiler/tools/archcompiler.py
   ```

   If neither exists, install the repo to a stable path before continuing. Do not clone to `/tmp/` for normal use.

2. **Confirm the application repo location with the user**

   All spec files and approved architecture artifacts belong in the application repo, not in the compiler repo.

3. **Run the shared preflight helper**

   Preferred command:

   ```bash
   python3 ~/.codex/arch-compiler/tools/archcompiler_preflight.py --app-repo <app-repo> --mode compile
   ```

   If the helper reports a failure, stop and follow the exact next action it prints before writing any files.

4. **Verify git is initialised in the application repo**

   The helper above already checks this. The command below is the manual fallback if the helper cannot be run:

   ```bash
   git -C <app-repo> rev-parse --git-dir
   ```

   If this exits non-zero, initialise git and create an initial commit before writing any files:

   ```bash
   git -C <app-repo> init
   git -C <app-repo> commit --allow-empty -m "chore: initial commit"
   ```

5. **Do not write any files until all checks pass**

## Provider-Binding Gate

Pattern-level approval is not the same as provider-level approval.

Treat the architecture as still provisional if any of these remain unresolved:
- concrete cloud/runtime target
- OIDC/auth provider or enforcement boundary
- database/storage/queue provider choice
- AI provider or model class
- retention/deletion mechanism for `nfr.data.retention_days`
- message transport and delivery semantics behind `async_messaging`

If those choices are deferred, say so explicitly to the human before finalising. Once they become concrete later, return to this skill, update the spec, recompile, diff the pattern set, and obtain fresh approval before implementation continues.

For brownfield systems, an existing prototype may reveal provider/runtime/boundary choices that are missing from the approved or in-progress spec. Treat those as inputs that must be made explicit in the spec review loop — not as automatically approved architecture. If the prototype exposes architecture drift, return here, update the spec, recompile, diff the result, and obtain approval before implementation continues.

---

## Artifacts Generated

| File | When written | Description |
|------|-------------|-------------|
| `compiled-spec.yaml` | always (with `-o`) | Full merged spec with defaults applied and `assumptions` section; valid re-input |
| `selected-patterns.yaml` | always (with `-o`) | Patterns that passed all filters, with match scores and honored rules |
| `rejected-patterns.yaml` | `-v` flag only | Patterns that were filtered out, with reason and filter phase |
| `compiled-spec-<timestamp>.yaml` | `-t` flag | Same files with UTC timestamp suffix (e.g. `compiled-spec-2026-03-17T19:36:31Z.yaml`) |
| stdout | always | Compiled spec printed to stdout; inline pattern comments in `-v` mode |

Exit code `0` on success, `1` on validation error or unsatisfiable NFR constraints. Advisory warnings (`warn_nfr`, `[high]` cost) do not change the exit code — they are informational only.

When the spec is rejected (exit 1), the compiler prints a `💡 Suggestions` block listing exactly which fields to change and what values are valid — read it before retrying.

---

## Before Writing Any Spec — App Repo Setup

**MUST-DO before writing a single line of spec or running the compiler:**

1. **Ask the user where the application repo lives.** The spec file, compiled artifacts, and all architecture outputs belong in the application repo — not in the pattern compiler repo. If no app repo exists yet, ask the user to create one (or create a new directory) and confirm the path before proceeding.

2. **Ensure git is initialised in the app repo.** All architecture artifacts must be version-controlled. If the app repo has no git history, run `git init` and make an initial commit before writing any files.

3. **Write the spec file into the app repo**, not into the compiler working directory. Use a name like `<project-name>-spec.yaml` at the root of the app repo.

4. **All compiled output goes into the app repo** — not into a `compiled_output/` folder inside the compiler repo.

**Why this matters:** Architecture artifacts are the permanent record for the application. Placing them in the compiler repo creates confusion about which repo is authoritative, and git-ignored `docs/architecture/` folders in the compiler repo are silently untracked.

---

## Authoring an Input Spec

**When writing a spec on behalf of a user, you MUST:**

1. **Read `schemas/canonical-schema.yaml` first** — this is the authoritative contract for every field, allowed value, and constraint. Do not guess field names or structure.
2. **Read `config/defaults.yaml`** — fields omitted from the spec are filled from here; knowing defaults prevents spec over-specification.
3. **Consult `test-specs/`** — comprehensive examples covering edge cases, compliance requirements, and platform combinations. Use these as reference, not templates to copy blindly.

For brownfield systems, inspect the existing codebase to extract actual providers, runtime assumptions, storage/auth boundaries, and feature signals. Use that information to inform the spec, but do not treat the prototype stack as approved architecture until it is explicit in the spec and reviewed by the human.

**If the user hasn't specified `constraints.cloud`, `constraints.language`, or `constraints.platform`, ask before proceeding.** These three fields drive the majority of pattern selection — defaulting them silently produces a spec that doesn't reflect the user's system. Same applies to any NFR target the user cares about (availability, latency, compliance).

**After writing `functional.summary`, cross-check implied feature flags and confirm with the user before compiling.** Users rarely know the flag names — infer from the description:

| If the summary mentions… | Ask about… |
|--------------------------|------------|
| Calling an AI/ML model (GPT, Claude, embeddings, vision, etc.) | `ai_inference: true` |
| Message queues, events, pub/sub, Kafka, SQS | `async_messaging: true` |
| Real-time updates, WebSockets, live feeds | `real_time_streaming: true` |
| Semantic search, similarity search, embeddings | `vector_search: true` |
| Storing documents or blobs with flexible schema | `document_store: true` |
| Session cache, Redis, low-latency key lookups | `key_value_store: true` |
| Multiple tenants, tenant isolation, per-customer data | `multi_tenancy: true` |
| Scheduled jobs, bulk processing, nightly runs | `batch_processing: true` |

Ask about each implied flag explicitly — do not silently leave implied flags at their `false` default.

**Spec authoring checklist:**
- [ ] Every field used exists in `schemas/canonical-schema.yaml`
- [ ] `constraints.cloud`, `constraints.language`, `constraints.platform` confirmed with user (not assumed)
- [ ] NFR targets reflect actual user requirements, not defaults
- [ ] Feature flags cross-checked against `functional.summary` — implied flags confirmed with user, not silently defaulted to `false`
- [ ] Save spec to a user-specified file (e.g. `<project-name>-spec.yaml`) before compiling

**Example spec:**

```yaml
project:
  name: My Service
  domain: ecommerce
functional:
  summary: REST API for product catalogue
constraints:
  cloud: azure          # aws | azure | gcp | agnostic
  language: python
  platform: api         # api | web | mobile | data | cli
nfr:
  availability:
    target: 0.999
  latency:
    p95Milliseconds: 100
    p99Milliseconds: 200
  security:
    auth: jwt
```

All missing fields are filled from `config/defaults.yaml` and recorded in `assumptions`.

---

## After Compilation

Once the compiler succeeds (exit 0), present results to the user by:

1. **Summarising selected patterns** — read `selected-patterns.yaml` and list pattern names grouped by category, with a one-line description of what each provides. Ask explicitly: "Are there any patterns here you don't want, or patterns you expected that are missing?" Do not move forward until the human has reviewed the full pattern list — patterns are not surfaced again in the pre-approval gate, so this is the human's primary chance to challenge the selection.
2. **Diffing against previous compile (on recompile only)** — if this is not the first compilation, compare the new `selected-patterns.yaml` against the previous one and present the diff before anything else: which patterns were added, which were removed, and the compiler's reason for each change. Do this before presenting cost results. Silent pattern churn between compilations is a common source of surprises.

   **If you find yourself presenting cost or pattern summaries before running a diff, stop — you skipped this step.** Run:
   ```bash
   diff <(grep "^- id:" previous-selected-patterns.yaml | sort) \
        <(grep "^- id:" compiled_output/selected-patterns.yaml | sort)
   ```
3. **Highlighting assumptions** — call out any fields in `compiled-spec.yaml` under `assumptions` that the compiler defaulted on the user's behalf; these represent decisions the user should confirm
4. **Surfacing advisories** — if the compiler printed `warn_nfr` warnings, explain what they mean and what the user can do (e.g. add a throughput NFR to resolve an under-utilisation warning)
5. **Resolving cost ceiling breaches before finalising** — if the compiler printed `[high]` cost warnings, do NOT proceed to finalisation without explicit human sign-off. Present the breach clearly and ask the human to choose a resolution path. See below.
6. **Offering next steps** — ask if the user wants to tighten any constraints, enable feature flags, adjust any defaulted assumptions, or re-compile

Do not just dump the raw YAML at the user.

### Handling cost ceiling breaches

A `[high]` cost warning means the compiled architecture exceeds a declared ceiling. **Do not finalise until the human explicitly acknowledges and resolves it.** Present the breach using this structure:

---
> **Cost ceiling exceeded — confirmation required before finalising**
>
> | | Ceiling | Actual | Overage |
> |--|---------|--------|---------|
> | Monthly OpEx | $X | $Y | +$Z/mo |
> | One-time CapEx | $X | $Y | +$Z |
>
> **Pattern infrastructure costs** *(for reference only — costs come from each pattern's `cost.provenance` field and were estimated by LLM at authoring time, not sourced from live pricing. Check `cost.provenance.source` in each pattern JSON for the estimate date. Validate against current provider pricing before treating as accurate)*:
> - `pattern-a` — $X/mo
> - `pattern-b` — $Y/mo
>
> **Operating model costs** *(requires your close attention — these often dominate real TCO)*:
>
> The compiler calculated ops team cost using:
> ```
> ops_team_size × single_resource_monthly_ops_usd × on_call_multiplier × deploy_freq_multiplier
> = <value> × $<value> × <value> × <value> = $<total>/mo
> ```
> Please confirm each input is accurate for your team:
> - **`ops_team_size: <value>`** — number of engineers dedicated to operating this system. Default is 0, which produces $0 ops cost and understates real TCO if your team has dedicated ops engineers.
> - **`single_resource_monthly_ops_usd: <value>`** — fully-loaded monthly cost per ops engineer (salary + benefits + overhead). Default is $10,000.
> - **`on_call: <value>`** — whether the team is on-call. `true` applies a 1.5× multiplier reflecting SRE on-call overhead.
> - **`deploy_freq: <value>`** — deployment frequency. Affects operational burden (daily = 1.0×, weekly = 0.8×, on-demand = 1.2×).
>
> If any of these don't match your team's reality, update `operating_model` in the spec and recompile before finalising.
>
> **How would you like to proceed?**
> 1. **Update `operating_model`** — correct the ops team inputs and recompile for an accurate cost picture
> 2. **Raise the ceiling** — update `cost.ceilings` in the spec to reflect the actual cost and recompile
> 3. **Remove specific patterns** — tell me which patterns are not required; I'll remove them and recompile
> 4. **Proceed anyway** — acknowledge the breach and approve as-is; the ceiling remains in the spec as a documented aspiration
---

Wait for the human's explicit choice. Do not guess which option they want and do not proceed to finalisation on your own.

### Promoting assumptions to formal spec fields

When a user wants to adjust a defaulted value, or before finalising (see below):

1. Find the field under `assumptions` — e.g. `assumptions.nfr.latency.p95Milliseconds: 500`
2. Add it at the corresponding top-level path with the confirmed value — e.g. `nfr.latency.p95Milliseconds: 100`
3. Remove the entry from `assumptions`
4. Recompile — the compiler will respect the explicit value and not re-default it

The path mapping is direct: `assumptions.<section>.<field>` → `<section>.<field>`.

**MUST-DO when promoting `assumptions.patterns.<id>.*`:** Before copying any pattern config value into the top-level `patterns:` section, cross-check each value against the spec's explicit choices:

- Does the `defaultConfig` name a specific provider (e.g. `model_provider: openai`, `provider: supabase`)? Cross-check against `constraints.saas-providers` and `constraints.cloud`. If there is a conflict — e.g. `model_provider: openai` but `saas-providers: [anthropic]` — flag it and ask the human for the correct value before promoting.
- Does the `defaultConfig` name a language-specific framework or tool? Cross-check against `constraints.language`.

**Do not silently promote a defaultConfig value that contradicts a spec-level constraint.** The defaultConfig is a registry default, not a user decision — it must be validated against what the user actually specified before it becomes part of the authoritative architecture.

**MUST-DO before final approval when provider-specific variants are selected:** inspect the promoted pattern config as a system, not field-by-field. Look for contradictions such as:
- cloud-specific architecture pattern defaults that imply a different auth or database provider than the human approved
- generic pattern config and provider-specific variant config disagreeing on timeout, persistence, or transport semantics
- a provider default changing the architecture from "agnostic" to provider-bound without that being reflected in `constraints.cloud` or `constraints.saas-providers`

If you find a contradiction, stop and resolve it in the spec before finalising. Do not bury the conflict in the approval header.

---

## Pre-Approval Validation Gate

**Before finalising, you MUST present the compiled spec's core sections to the human for explicit sign-off.** Do not skip this step even if the human said "looks good" to the pattern list — the pattern list is not the architecture contract. The sections below are.

Present the following sections from `compiled-spec.yaml` in readable form and ask the human to confirm each:

```
constraints:
  cloud: <value>          # is this the right target environment?
  language: <value>
  platform: <value>
  saas-providers: [...]   # are these all the external services you intend to use?
  features:               # are these the right feature flags — anything missing or incorrectly enabled?
    ai_inference: <value>
    caching: <value>
    ...

nfr:
  availability:
    target: <value>       # does this reflect your actual uptime requirement?
  latency:
    p95Milliseconds: <value>
    p99Milliseconds: <value>
  data:
    pii: <value>          # does this app store or process personally identifiable information?
    retention_days: <value>
    compliance:           # are these compliance requirements accurate for your jurisdiction?
      gdpr: <value>
      ccpa: <value>
      hipaa: <value>
      sox: <value>

operating_model:
  ops_team_size: <value>        # how many engineers will operate this?
  on_call: <value>              # will someone be paged if this goes down?
  deploy_freq: <value>          # how often will you deploy?

cost:
  ceilings:
    monthly_operational_usd: <value>   # is this a real constraint or a placeholder?
    one_time_setup_usd: <value>
  preferences:
    prefer_saas_first: <value>
```

Then ask: **"Do all of these reflect your actual system requirements? Any corrections before I finalise?"**

Wait for explicit confirmation. Do not proceed to finalisation until the human confirms (or makes corrections and confirms the updated values). If corrections are made, update the spec and recompile before finalising.

**Why this gate exists:** The compiler promotes defaults into these sections — values the human never explicitly typed. A pattern list review does not surface these defaults. This gate ensures the human is signing off on the actual architecture contract, not just the pattern names.

**MUST-DO before asking for approval:** call out any architecture-binding decisions that are still open. If the user is treating them as "implementation details" but they would change providers, runtimes, message semantics, auth boundaries, retention handling, or accepted data-processing risk, tell them these are still architecture decisions and must be resolved before final approval.

---

## Finalising as Authoritative Architecture

When the user approves the compiled spec as the definitive architectural record:

1. **Promote all assumptions to top-level fields and remove the `assumptions` section** — the approved architecture must have no `assumptions` block. Every field must be explicit so implementing agents have a single place to look with no ambiguity about what was decided vs. defaulted.

   For each field under `assumptions.*`: move it to its top-level path, confirm the value with the human if needed, then delete the `assumptions` entry. Pattern configs under `assumptions.patterns.<id>.*` move to `patterns.<id>.*`. Recompile once to verify the spec is still valid with all fields explicit.

   **Verify before proceeding:** After writing `architecture.yaml`, run:
   ```bash
   grep -c "^assumptions:" architecture.yaml
   ```
   If the result is not `0`, the assumptions block is still present — stop and complete the promotion before continuing.

2. **Copy the finalised artifacts to the application repo and commit them there.**

   The pattern compiler repo (`docs/architecture/` here) is a staging workspace — it is git-ignored and not a permanent record. The permanent home for the approved architecture is the application repo that will be built from it.

   Copy these three files into the application repo:
   ```
   <app-repo>/docs/architecture/architecture.yaml              # rename from compiled-spec.yaml
   <app-repo>/docs/architecture/selected-patterns.yaml         # copy as-is
   <app-repo>/docs/architecture/patterns/<id>.json             # copy each selected pattern's full JSON
   ```

   If the user has not told you where their application repo is, ask before proceeding — do not commit into the pattern compiler repo.

   Copy the full pattern JSON for every pattern in `selected-patterns.yaml` — not a summary. The full JSON contains everything an implementing agent needs: `description`, `defaultConfig`, `configSchema` (with trade-off explanations), `provides`, and `requires`. Implementing agents will not have access to the pattern registry and will rely solely on these copied files.

   **Verify before proceeding:** Pattern count in `selected-patterns.yaml` must match pattern files copied:
   ```bash
   grep -c "^- id:" <app-repo>/docs/architecture/selected-patterns.yaml
   ls <app-repo>/docs/architecture/patterns/*.json | wc -l
   ```
   If the counts differ, find and copy the missing pattern JSONs before continuing.

   Commit the approved artifacts explicitly:

   ```bash
   git -C <app-repo> add docs/architecture/ <spec-file>.yaml
   git -C <app-repo> commit -m "feat: add approved architecture"
   git -C <app-repo> log --oneline -1
   ```

   If `git -C <app-repo> log --oneline -1` does not show the approved architecture commit, stop and fix that before proceeding to implementation. Approved architecture artifacts must be versioned.

3. **Add an approval header** to `architecture.yaml` so any agent reading the repo knows this is finalised and not a work-in-progress:
   ```yaml
   # STATUS: APPROVED
   # Approved by: <name>
   # Date: <date>
   # Do not modify without re-running the compiler and obtaining fresh approval.
   project:
     ...
   ```

   **Verify before proceeding:**
   ```bash
   grep -c "STATUS: APPROVED" <app-repo>/docs/architecture/architecture.yaml
   ```
   If the result is not `1`, the header is missing — add it before continuing.

4. **Tell future agents how to consume it** — when asking agents to implement features or make technical decisions, point them explicitly to these three files:
   - `docs/architecture/architecture.yaml` — binding constraints (cloud, language, platform, NFR targets, compliance). Do not deviate without human approval.
   - `docs/architecture/selected-patterns.yaml` — the approved pattern set. Implementation decisions should align with these patterns.
   - `docs/architecture/patterns/<id>.json` — full pattern JSON for each selected pattern. Read the relevant file before implementing a pattern; `defaultConfig` and `configSchema` contain the key implementation decisions and trade-offs.

5. **Re-compilation invalidates approval** — if the spec is recompiled (e.g. to add a new constraint), the output replaces the approved files and requires fresh human sign-off before agents treat it as authoritative again. The old approval header must not survive into the new `architecture.yaml`.

   **Verify after any recompile:**
   ```bash
   grep "STATUS: APPROVED" <app-repo>/docs/architecture/architecture.yaml
   ```
   If this returns a match before the human has re-approved the new output, remove the header immediately — a stale approval header is worse than no header because it misleads implementing agents into treating unreviewed output as authoritative.

6. **Hand off to implementing agents** — the approved `docs/architecture/` folder is the input contract for any implementation workflow. Use `skills/implementing-architecture/SKILL.md` if available, or provide the three artifact paths directly: `architecture.yaml` (binding constraints), `selected-patterns.yaml` (approved pattern set), `patterns/<id>.json` (full pattern detail per pattern).

---

## Running the Compiler

```bash
# Choose the canonical stable install path for your environment:
#   Codex:  ~/.codex/arch-compiler
#   Claude: ~/.claude/arch-compiler
#
# Examples below use the Codex path; substitute ~/.claude/arch-compiler if needed.

# See all options
python3 ~/.codex/arch-compiler/tools/archcompiler.py --help

# Run shared workflow preflight before compiling
python3 ~/.codex/arch-compiler/tools/archcompiler_preflight.py --app-repo <app-repo> --mode compile

# Install dependencies
python3 -m pip install -r ~/.codex/arch-compiler/tools/requirements.txt

# Compile to stdout
python3 ~/.codex/arch-compiler/tools/archcompiler.py my-spec.yaml

# Compile + write artifact files (output directory must exist before running)
mkdir -p compiled_output/
python3 ~/.codex/arch-compiler/tools/archcompiler.py my-spec.yaml -o compiled_output/

# Verbose mode — annotates each spec field with triggered patterns; primarily useful for human review.
# For agents, selected-patterns.yaml and rejected-patterns.yaml are more actionable.
python3 ~/.codex/arch-compiler/tools/archcompiler.py my-spec.yaml -v                       # stdout only
python3 ~/.codex/arch-compiler/tools/archcompiler.py my-spec.yaml -o compiled_output/ -v  # also writes rejected-patterns.yaml

# Add UTC timestamp to output filenames
python3 ~/.codex/arch-compiler/tools/archcompiler.py my-spec.yaml -o compiled_output/ -v -t

# Include coding-level patterns (GoF, DI, test strategies — excluded by default)
python3 ~/.codex/arch-compiler/tools/archcompiler.py my-spec.yaml --include-coding-patterns
```

Run commands against a canonical stable install path. Relative examples like `python3 tools/archcompiler.py ...` assume you are already in the compiler repo; agents often are not. Prefer a persistent install path so the compiler is discoverable across sessions without re-cloning.

---

## How Pattern Selection Works

| Phase | What happens |
|-------|-------------|
| 1. Parse & Validate | Load spec, validate schema, check semantic consistency |
| 2. Merge Defaults | Fill missing fields from `config/defaults.yaml`; record in `assumptions` |
| 2.5 Disallowed filter | Remove any pattern listed in `disallowed-patterns`; warn on unknown IDs |
| 3.1 Constraint filter | Keep patterns whose `supports_constraints` rules all match the spec |
| 3.2 NFR filter | Keep patterns whose `supports_nfr` rules all match the spec |
| 3.3 Conflict resolution | Remove conflicting patterns; winner = highest match score, then lowest cost |
| 3.4 Config merge | Merge pattern `defaultConfig` into `assumptions.patterns` |
| 3.5 Coding filter | Drop `type: coding` patterns unless `--include-coding-patterns` |
| 4. Cost feasibility | Check total cost against `cost.ceilings`; emit advisory warnings |
| 5. Output | Emit compiled spec to stdout; write artifact files if `-o` set |

---

## Key Flags and Fields

**Feature flags** (opt-in capabilities, not performance targets):
```yaml
constraints:
  features:
    caching: true
    vector_search: true
    graph_database: true
```

**Cost and operating model** (required for accurate TCO):
```yaml
cost:
  intent:
    priority: optimize-tco   # minimize-opex | minimize-capex | optimize-tco
  ceilings:
    monthly_operational_usd: 500
    one_time_setup_usd: 1000
operating_model:
  ops_team_size: 2
  single_resource_monthly_ops_usd: 10000
  on_call: true
  deploy_freq: daily          # daily | weekly | on-demand
  amortization_months: 24
```

Without `operating_model`, ops team cost defaults to zero — understating real TCO.

**Disallowed patterns** (explicitly exclude patterns that would otherwise be selected):
```yaml
disallowed-patterns:
  - ops-low-cost-observability   # too complex for project scope
  - ops-slo-error-budgets
```
Excluded patterns appear in `rejected-patterns.yaml` with `phase: phase_2_5_disallowed_patterns`.
A warning is emitted for any ID not found in the registry (typo protection).

---

## Audit Tools

```bash
# Audit pattern metadata quality (descriptions, costs, NFR rules)
python3 tools/audit_patterns.py

# Audit NFR/constraint rule paths (catch stale JSON pointer references)
python3 tools/audit_nfr_logic.py

# Audit conflict symmetry (if A conflicts B, B must conflict A)
python3 tools/audit_asymmetric_conflicts.py
```

See `docs/tools.md` for full tool reference.

---

## Adding or Editing Patterns

### What agents MAY and MAY NOT do

| Action | Agent allowed? |
|--------|---------------|
| Read existing patterns in `patterns/` | ✅ Yes |
| Read `schemas/pattern-schema.yaml` and `schemas/canonical-schema.yaml` | ✅ Yes |
| Author a **new** pattern file | ✅ Yes — but see approval workflow below |
| Edit an **existing** pattern file | ❌ No — human-only |
| Edit `schemas/pattern-schema.yaml` | ❌ No — human-only |
| Edit `schemas/canonical-schema.yaml` | ❌ No — human-only |
| Edit `config/defaults.yaml` | ❌ No — human-only |
| Place a new pattern file directly into `patterns/` | ❌ No — requires human review first |

### Before authoring a new pattern — search existing patterns first

**MUST-DO before proposing to create any new pattern:**

1. **Search `patterns/` for existing candidates** — use the capability name or concept as a search term. A pattern covering the need may already exist under a different name.
2. **Check `rejected-patterns.yaml`** — if a candidate appears there, read its rejection reason. A rejected pattern is often one spec field change away from selection (e.g. enabling `audit_logging: true` to unlock `secrets-vault`, or adding a `saas-provider` to unlock a provider-specific variant).
3. **Present the spec-change option to the human first** — "Pattern X already exists but was rejected because field Y is `false` in your spec. Setting it to `true` would select it. Would you like to do that instead of authoring a new pattern?"

Only proceed to author a new pattern if no existing pattern covers the need and no spec change would unlock one.

### Authoring a new pattern (agent workflow)

**Hard gate:** A user asking you to "author a new pattern" does **not** by itself authorize placing it in `patterns/`. Default to staging-only unless the human explicitly says to make the pattern live in `patterns/`.

When a user asks you to create a new pattern:

1. **Read `schemas/pattern-schema.yaml`** — every field, type, and required property
2. **Read `schemas/capability-vocabulary.yaml`** — check whether every `provides` / `requires` capability you plan to use already exists as a canonical name or alias
3. **Read 2–3 similar existing patterns** in `patterns/` as structural reference
4. **If you introduce a new capability name or alias, update `schemas/capability-vocabulary.yaml` as part of the same change** so the registry vocabulary stays aligned with the new pattern
5. **Write the new pattern file to a human-designated staging location outside `patterns/`** — e.g. `staging/patterns/<id>.json` — **never directly into `patterns/`**

   **Verify before continuing:**
   ```bash
   ls staging/patterns/<id>.json   # must exist
   ls patterns/<id>.json           # must NOT exist
   ```
   If the file is in `patterns/`, move it back to the staging location before proceeding — an unapproved pattern in `patterns/` is immediately live.

6. **Self-review against the schema and vocabulary** — `audit_patterns.py` only scans `patterns/` and will not validate staged files. Instead, manually verify the staged file against `schemas/pattern-schema.yaml` and `schemas/capability-vocabulary.yaml`: check all required fields are present, ID matches filename, capability names are canonical (or intentionally added to the vocabulary), rules use valid JSON pointer paths, and conflict declarations are bidirectional.

   **Verify bidirectional conflicts:** For every pattern ID listed in your new pattern's conflict declarations, check that the other pattern also declares yours:
   ```bash
   grep -l "<your-new-pattern-id>" patterns/*.json
   ```
   Any file returned must contain your new pattern ID in its own conflict list — if not, flag it for the human to fix before approving.
7. **Present the file to the human for review** — explicitly state it is not yet active and awaits approval
8. **Human moves the file into `patterns/`** after review, then runs `python3 tools/audit_patterns.py` and `python3 -m pytest tests/ -q` to confirm it passes — this is the only step an agent must not perform unilaterally

**Do not skip the staging step.** A pattern placed directly into `patterns/` is immediately picked up by the compiler and all tests. Unapproved patterns can silently change compiled output for all specs.

### Key pattern authoring rules

- Pattern IDs must match filename (`cache-aside.json` → `id: "cache-aside"`)
- `provides` / `requires` capability names must align with `schemas/capability-vocabulary.yaml`; if you add a new canonical capability or alias, update the vocabulary in the same change
- `supports_constraints` and `supports_nfr` rules use AND logic — all must match for pattern to be selected
- Conflict declarations must be **bidirectional** — if A conflicts B, B must also declare A
- Sibling variant patterns (e.g. cloud-specific variants) must each conflict with all their siblings
- Never encode logic as pattern ID string matching — all logic goes in pattern metadata fields

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing spec fields not in `schemas/canonical-schema.yaml` | Only use fields that already exist in the schema — agents cannot modify `schemas/canonical-schema.yaml` to add new ones |
| Compiling without `-o` and expecting artifact files | Without `-o`, output goes to stdout only — no files are written |
| Output directory doesn't exist when using `-o` | The compiler silently writes nothing; pre-create the directory before running |
| Treating compiler warnings (`warn_nfr`, `[high]` cost) as errors | They are advisories; exit code is still `0` unless the spec is invalid or unsatisfiable |
