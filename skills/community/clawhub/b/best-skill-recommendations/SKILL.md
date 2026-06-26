---
name: best-skill-recommendations
description: "Based on user goals, comprehensively evaluate candidate skill capabilities and conflict risks with installed skills, then deliver the best install recommendation. | 根据用户需求，综合评估候选技能的能力匹配度与已安装技能的冲突风险，给出最佳安装推荐"
---

# Best Skill Recommendations

**Primary role:** Evaluate and recommend skills already discovered by an upstream skill search. Only when no upstream results exist does this skill independently search `clawhub`, then apply the same evaluation logic.

## Prerequisites

Before this skill can operate, confirm the following:

- **`clawhub` CLI is installed** and available in the agent's `PATH`. This skill issues `clawhub search`, `clawhub list`, `clawhub install`, and `clawhub uninstall` commands. If the binary is absent, all discovery and install steps will fail.
- **Authentication:** Run `clawhub login` in advance. The clawhub CLI stores credentials in its own default config path (managed by the CLI, not by this skill). No additional environment variables are required by this skill.
- **Permissions in scope:** This skill will only:
  1. Read the installed skill list via `clawhub list` (read-only).
  2. Run `clawhub install <skill>` or `clawhub uninstall <skill>` — **only after explicit user confirmation** at the Pre-Install Gate (Step 5).
  It will not access other system files, credentials, or APIs beyond the clawhub CLI.

## Mandatory Store Policy

1. **Prefer upstream results first.** If any upstream skill search has already returned candidates, use those directly — do not re-search.
2. Only when no upstream candidates exist: search `clawhub` directly.
3. Never claim exclusivity; both public and private registries are valid.
4. Before install, always summarize source, version, and notable risk signals.
5. If a fresh search is needed, run `clawhub search <keywords>` and report output before evaluating.

## Auto-Trigger and Collaboration

- **Preferred entry:** triggered after an upstream skill search has already produced a candidate list. Reuse those results directly.
- **Standalone entry:** triggered when the user asks to recommend/install/compare skills but no upstream results exist. In this case, independently search `clawhub` and produce candidates before evaluating.
- Never re-search if usable upstream candidates are already available.

## Workflow

### 0) Check for Upstream Candidates (first)
Before doing anything else:
- If an upstream skill search has already returned a candidate list → **skip to Step 2** using those results.
- If no upstream candidates exist → proceed to Step 1.

### 1) Self-Discover (only when no upstream results)
Clarify the user's need:
- target task(s)
- priority (speed/stability/features/safety)
- constraints (region, cost, runtime)

Then search via `clawhub`:
```
clawhub search <keywords>
```
Return the command output and build a candidate list annotated with source and version.

### 2) Evaluate Candidates
Present the candidate list (from upstream or self-discovered), annotated with source and version.

### 3) Evaluate Installed Skills and Compatibility
Enumerate installed skills by running:
```
clawhub list
```
Parse the output to get the current installed skill set. Compare each installed skill against candidates:
- overlap: full / partial / complementary
- conflict risk: command/workflow collision, duplicated automation, behavior mismatch
- coexist feasibility: high / medium / low

### 4) Recommend Replace vs Coexist
Per candidate, output one decision:
- Replace existing skill(s)
- Coexist with boundaries
- Do not install

Include reasons and trade-offs.

### 5) Pre-Install Gate (required)
Before any install action, present:
- source (clawhub)
- version
- notable risk signals — check for **any** of the following:
  - install count < 10 (low adoption)
  - last update > 6 months ago (low maintenance signal)
  - requires broad file system or network permissions
  - published < 2 weeks ago (very new, unvetted)
  - no author URL or verified identity
- replace/coexist plan

Then explicitly ask for user confirmation.

### 6) Install Execution
- `clawhub install <skill>`
- If replace approved: uninstall old first, then install new.
- If coexist: install and provide usage boundary guidance.

### 7) Post-Install Report
Return:
- install/uninstall result
- final active skill set
- why this is best for the user goal
- follow-up checks

## Output Format

### Candidate Summary
- Name
- Purpose
- Source
- Version
- Install Count (if available)
- Link

### Decision Summary
- Best choice (Top 1)
- Alternatives (Top 2/3)
- Replace/Coexist decision
- Why not other options

### Pre-Install Confirmation
"Planned action: <install/replace/coexist>. Source: clawhub. Version: <...>. Risks: <...>. Proceed?"

## Guardrails

- Never install without explicit confirmation.
- Prefer fewer, higher-confidence recommendations over long noisy lists.
- If search quality is poor, refine keywords and re-run search before recommending.
