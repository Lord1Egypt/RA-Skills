---
name: autoskill
preamble-tier: 2
version: 1.1.1
author: Science-Prof-Robot
homepage: https://github.com/Science-Prof-Robot/autoskill
license: MIT
description: |
  Intelligent skill router. Analyzes the current problem statement and context,
  scores all available skills for applicability, and recommends the most relevant
  ones in priority order. **No skill is ever invoked without your explicit approval.**

  Use when you want Claude to automatically identify and recommend the right
  skills without manually choosing them. Great for complex tasks where the right set
  of skills is non-obvious.

  Invocation:
    /autoskill [problem description]
    /autoskill (uses current conversation context if no args given)

  Examples:
    /autoskill fix the login bug that crashes on empty password
    /autoskill add unit tests for the payment module
    /autoskill review my PR before I merge
    /autoskill (running with no args analyzes the current conversation)
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - AskUserQuestion
  - Skill
---

## Preamble (run first)

The commands below inspect local git state and detect the project language from
config files. They do not modify anything, send data externally, or run project
code. They are safe to run in any local workspace.

```bash
_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "no-git")
echo "BRANCH: $_BRANCH"
_LANG_SIGNALS=""
[ -f package.json ] && _LANG_SIGNALS="$_LANG_SIGNALS typescript,javascript"
[ -f requirements.txt ] || [ -f pyproject.toml ] || [ -f setup.py ] && _LANG_SIGNALS="$_LANG_SIGNALS python"
[ -f Cargo.toml ] && _LANG_SIGNALS="$_LANG_SIGNALS rust"
[ -f go.mod ] && _LANG_SIGNALS="$_LANG_SIGNALS go"
[ -f pom.xml ] || [ -f build.gradle ] && _LANG_SIGNALS="$_LANG_SIGNALS java"
[ -f pubspec.yaml ] && _LANG_SIGNALS="$_LANG_SIGNALS dart,flutter"
ls *.csproj 2>/dev/null | head -1 | grep -q . && _LANG_SIGNALS="$_LANG_SIGNALS csharp"
echo "LANG_SIGNALS:${_LANG_SIGNALS:-unknown}"
_GIT_CHANGES=$(git status --short 2>/dev/null | head -20 || echo "")
echo "GIT_CHANGES: $(echo "$_GIT_CHANGES" | wc -l | tr -d ' ') files"
echo "CHANGED_EXTS: $(echo "$_GIT_CHANGES" | grep -oE '\.[a-zA-Z]+$' | sort -u | tr '\n' ',' 2>/dev/null || echo 'none')"
```

## High-Risk Skill Registry

The following skills perform irreversible, externally-visible, or broadly-scoped
actions. They are **always treated as SUGGEST-tier** — they will never be
recommended for automatic inclusion and always require individual user
confirmation before running.

```
HIGH_RISK_SKILLS = [
  # Deployment / release / CI
  ship, land-and-deploy, canary, deploy, setup-deploy, prp-pr, deployment-patterns,

  # Payment / billing / money
  customer-billing-ops, finance-billing-ops, agent-payment-x402,

  # Database mutations
  database-migrations,

  # External communications / public posts
  github-ops, x-api, email-ops, messages-ops, unified-notifications-ops,
  crosspost, content-writer,

  # Account / enterprise / credential operations
  enterprise-agent-ops, investor-outreach, cso, security-bounty-hunter,

  # Broad shell / file system access
  careful, guard, safety-guard,
]
```

**Additional heuristic:** Any skill whose description contains keywords such as
"deploy", "payment", "billing", "money", "purchase", "credential", "account",
"external message", "post to", "send email", "database migration",
"DROP TABLE", "rm -rf", "force-push", or "broad shell" is also treated as
high-risk even if it is not in the fixed list above.

When scoring (Phase 3), check each candidate against this registry and the
heuristic. If it matches, force its tier to SUGGEST and add a `[HIGH-RISK]`
label in the scoring table, regardless of its numeric score.

## Phase 1 — Problem Extraction

**Goal:** Build a structured context profile from the arguments and project state.

**Input:** `$ARGUMENTS` — the user's problem description. If empty, synthesize from the current conversation: look at the most recent user messages, any error output, open files, or recent tool calls visible in context.

**Build the context profile by answering these questions:**

1. **Problem statement** — What is the user trying to accomplish? (1-2 sentences, concrete)
2. **Action intent** — What category of work is this?
   - `create` — building something new (feature, file, component, test)
   - `fix` — repairing broken behavior (bug, error, crash, regression)
   - `review` — evaluating quality (code review, security audit, PR check)
   - `deploy` — shipping or releasing (push, merge, publish, CI)
   - `document` — writing or updating docs
   - `refactor` — improving structure without changing behavior
   - `test` — adding or improving test coverage
   - `analyze` — understanding or investigating something
   - `design` — UI/UX or architecture planning
   - `optimize` — improving performance
3. **Language/stack** — From the preamble `LANG_SIGNALS` and `CHANGED_EXTS`
4. **Domain tags** — Select all that apply from: `frontend`, `backend`, `database`, `security`, `testing`, `deployment`, `performance`, `documentation`, `architecture`, `mobile`, `api`, `infrastructure`, `data`
5. **Keywords** — Extract 5-10 specific nouns and verbs from the problem statement (e.g., "authentication", "token", "crash", "refactor", "test coverage")

Print the context profile in this format before proceeding:
```
CONTEXT PROFILE
───────────────
Problem:  [1-2 sentences]
Intent:   [action intent]
Stack:    [languages/frameworks]
Domains:  [comma-separated domain tags]
Keywords: [comma-separated keywords]
```

## Phase 2 — Skill Inventory Scan

**Goal:** Build a candidate list from the available skills.

The full skill list is already loaded in your context (from the system-reminder's "The following skills are available" section). You do NOT need to read files — use the in-context list directly.

**Steps:**

1. From the system-reminder skill list, extract every skill's name and description.

2. Group skills by domain bucket:

| Bucket | Skill name patterns to look for |
|--------|--------------------------------|
| `testing` | tdd, test, pytest, jest, coverage, e2e, playwright, spec |
| `security` | security, auth, vulnerability, owasp, bounty, pentest |
| `code-quality` | review, lint, simplify, refactor, clean, style, standards |
| `deployment` | ship, deploy, land, canary, pm2, docker, ci, cd |
| `frontend` | frontend, ui, design, figma, css, react, vue, html, animation |
| `backend` | backend, api, rest, graphql, server, express, fastapi, spring |
| `database` | database, sql, postgres, clickhouse, migration, schema |
| `documentation` | docs, readme, update-docs, codemaps, openapi |
| `planning` | plan, autoplan, blueprint, office-hours, architect, prp |
| `performance` | performance, optimize, bundle, lighthouse, profil |
| `infrastructure` | kubernetes, terraform, aws, cloud, gstack, mcp |
| `mobile` | flutter, android, ios, kotlin, swift, react-native |
| `meta` | checkpoint, learn, memory, session, instinct, hookify |

3. Build a flat candidate list: every skill that appears in at least one domain bucket relevant to the context profile's `Domain tags`.

Print the candidate count: `Found N candidate skills in relevant buckets.`

## Phase 3 — Relevance Scoring

**Goal:** Score every candidate skill and decide what to recommend, suggest, or skip.

For each candidate skill, score 0–100 using this rubric:

| Criterion | Weight | How to evaluate |
|-----------|--------|-----------------|
| **Intent match** | 35% | Does the skill's purpose directly match the context profile's `action intent`? Exact match = 35, close match = 20, weak match = 10, no match = 0 |
| **Domain match** | 30% | How many of the context profile's `domain tags` appear in this skill's description or bucket? Each match adds ~10 points up to 30 |
| **Keyword overlap** | 20% | How many of the context profile's `keywords` appear (roughly) in the skill name or description? Each match adds ~4 points up to 20 |
| **Stack match** | 15% | Does the skill explicitly target the detected language/framework? Match = 15, stack-agnostic = 10, mismatch = 0 |

**Thresholds:**
- **≥ 70** → RECOMMENDED (high confidence — included in the proposed plan)
- **40–69** → SUGGEST (borderline — presented to user for optional inclusion)
- **< 40** → Skip silently

**High-risk override:** If a skill appears in the HIGH_RISK_SKILLS registry or matches
the heuristic above, force it to SUGGEST tier and mark it `[HIGH-RISK]` in the table,
regardless of its numeric score.

**Constraint: max 5 RECOMMENDED skills per invocation.** If more than 5 score ≥70, take the top 5 by score.

Print the scoring table (show only skills scoring ≥ 30):

```
SKILL SCORING
─────────────────────────────────────────────────────────────────
Skill                  Score  Tier             Reason
─────────────────────── ─────  ──────────────   ─────────────────────
tdd-workflow           88     RECOMMENDED      intent=create, domain=testing, keyword=test
security-review        82     RECOMMENDED      intent=fix, domain=security, keyword=auth
typescript-reviewer    75     RECOMMENDED      stack=typescript, domain=code-quality
code-review            72     RECOMMENDED      intent=review match
database-reviewer      55     SUGGEST          domain=database, weak intent match
ship                   71     SUGGEST [HIGH-RISK]  score≥70 but forced to SUGGEST — deployment skill
seo                    8      SKIP             no frontend/content signals
─────────────────────────────────────────────────────────────────
RECOMMENDED: N skills | SUGGEST: M skills (K high-risk) | SKIP: K skills
```

## Phase 4 — Execution Preview and Mandatory Confirmation

**This phase ALWAYS runs before any skill is invoked.** There are no exceptions.
Even a single RECOMMENDED skill requires explicit user confirmation.

### Step 4a — Show the execution plan

Print the full proposed run as a preview. Do not invoke anything yet:

```
EXECUTION PLAN
──────────────────────────────────────────────────
 #  Skill                Tier        Score  Why
──  ─────────────────── ──────────  ─────  ─────────────────────────
 1  security-review      RECOMMENDED 88     fix intent + security domain
 2  investigate          RECOMMENDED 82     fix intent + keyword=crash
 3  typescript-reviewer  RECOMMENDED 75     stack=typescript
 4  code-review          RECOMMENDED 72     review intent match
 5  ship                 HIGH-RISK   71     deployment — requires confirmation
──────────────────────────────────────────────────
```

### Step 4b — Mandatory confirmation gate

Use **AskUserQuestion** for EVERY run. Do not skip this step.

Format the question as follows:

> **autoskill recommends [N] skills for: "[problem statement]"**
>
> These skills will run **only after you confirm** below:
>
> **Recommended (score ≥70):**
> - `skill-name` — [reason it applies]
> - `skill-name` — [reason it applies]
>
> **Also applicable — want any of these?**
> - `skill-name` [SUGGEST] — [reason it might apply]
> - `skill-name` [HIGH-RISK] — [why it needs confirmation]
>
> **Actions:**
> - Type the names of any suggested/high-risk skills you want to add
> - Type "none" to run only the recommended skills
> - Type "cancel" to stop and do nothing

If the user replies "cancel" or selects no skills and there are no recommended
skills, abort and report BLOCKED.

Add any user-selected skills to the execution queue before continuing.

## Phase 5 — Skill Execution

**Goal:** Apply each queued skill in order.

**Execution order:**
1. RECOMMENDED skills sorted by score descending
2. User-approved SUGGEST / HIGH-RISK skills appended at the end

**For each skill in the queue:**

1. Print: `→ Applying \`[skill-name]\` (score: [N]) — [one-line reason]`
2. Invoke: `Skill(skill="[skill-name]", args="[relevant portion of the original problem statement]")`
3. Wait for the skill to complete before starting the next one
4. Note the outcome (completed / blocked / needs-context)

**If a skill returns BLOCKED or NEEDS_CONTEXT:** note it in the audit table and continue to the next skill. Do not abort the entire queue for one blocked skill.

**If NO skills score ≥40:**

Do not silently do nothing. Instead use AskUserQuestion:

> No skills scored above the applicability threshold for: "[problem statement]"
>
> This usually means the request is best handled directly (not via a specialized skill),
> or the problem description needs more context.
>
> Options:
> A) Let me handle this directly without a skill
> B) Tell me more about what you need (I'll re-score)
> C) Show me all available skills so I can pick manually

## Phase 6 — Decision Audit Report

After all skills have run (or been skipped), print the final report:

```markdown
## autoskill Run Complete

**Problem:** [problem statement]
**Intent:** [action intent] | **Stack:** [stack] | **Domains:** [domains]

| Skill | Score | Tier | Applied | Outcome | Reason |
|-------|-------|------|---------|---------|--------|
| tdd-workflow | 88 | RECOMMENDED | ✅ | completed | create intent + testing domain |
| security-review | 82 | RECOMMENDED | ✅ | completed | fix intent + security domain |
| ship | 71 | HIGH-RISK | ⏸ User | skipped | user declined |
| database-reviewer | 55 | SUGGEST | ⏸ User | completed | user approved |
| seo | 8 | SKIP | ❌ | — | no frontend signals |

**Summary:** [N] skills applied, [M] skipped, [K] blocked.
```

## Completion Status Protocol

Report final status as one of:
- **DONE** — All queued skills completed successfully
- **DONE_WITH_CONCERNS** — Completed, but one or more skills returned BLOCKED or NEEDS_CONTEXT
- **BLOCKED** — Could not determine applicable skills, all skills failed, or user cancelled
- **NEEDS_CONTEXT** — Problem statement too vague to score skills reliably

## Design Constraints

- **Never bulk-read skill files.** The system-reminder list is sufficient for scoring. Only read a specific SKILL.md file if you need to understand invocation details for an edge case.
- **Never hardcode skill assumptions.** Always derive the candidate list from the live system-reminder. New skills added to the system are automatically included.
- **Mandatory confirmation for every run.** No skill is ever invoked without the user first seeing the execution plan and explicitly confirming or selecting which skills to run. There are no single-skip exceptions.
- **High-risk skills always require individual confirmation.** Skills that deploy, send messages, modify data, charge accounts, or access broad shell/file scope are never automatically included — they are always presented as optional and marked `[HIGH-RISK]`.
- **Heuristic + registry for high-risk detection.** The fixed HIGH_RISK_SKILLS list is supplemented by a keyword heuristic so newly added skills with dangerous descriptions are caught even if the registry has not been updated.
- **Show the plan before executing.** The execution preview in Phase 4 ensures the user always sees what will run before any skill is invoked.
- **Graceful degradation.** If the Skill tool is unavailable, print the scored table and explain which skills the user should invoke manually.
- **Max 5 recommended skills.** Prevents runaway chaining on broad problem statements.
- **Sequential execution.** Skills run one at a time, in score order. Never parallel — each skill may change project state that the next skill depends on.

## Safety Notice

`autoskill` is a meta-skill that recommends and routes to other skills. It does not
perform any file modifications, deployments, or external communications itself.
However, the skills it recommends may do so. Because of this:

1. **Always review the execution plan** before confirming.
2. **Remove any skill you do not want** by selecting only the ones you trust.
3. **Be especially cautious with [HIGH-RISK] skills** — they are marked for a reason.
4. **If you are unsure, choose "cancel"** — autoskill will stop and you can proceed manually.
