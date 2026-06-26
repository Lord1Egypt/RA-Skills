# Clawdit Audit Framework

This document is the analytical reference for the Clawdit belief audit process. It defines what beliefs are, how to extract them, how to evaluate them, and how to structure findings.

---

## 1. What is a Belief?

In the context of an OpenClaw agent, a **belief** is any directive, instruction, preference, constraint, identity statement, or behavioral rule embedded in the agent's loaded context files. Beliefs shape every downstream decision the agent makes.

Beliefs are found in:

- **SOUL.md** — Identity, personality, values, behavioral guidelines, communication style
- **AGENTS.md** — Capabilities, tool usage patterns, operational rules, decision-making heuristics
- **USER.md** — Information about the owner, preferences, context
- **Skill SKILL.md files** — Per-skill behavioral instructions, output formats, tool-use patterns
- **Standing orders / cron configurations** — Implicit beliefs about what should happen automatically
- **Custom .md files** — Any additional markdown files loaded into the agent's context

### Belief Types

| Type | Description | Example |
|------|-------------|---------|
| **Identity** | Who the agent is, its name, its role | "You are a research assistant named Atlas" |
| **Personality** | Tone, communication style, demeanor | "Be concise and direct" |
| **Behavioral Rule** | What to do or not do in specific situations | "Always confirm before deleting files" |
| **Capability Claim** | What the agent can or should do | "You can browse the web and summarize articles" |
| **Constraint** | Limitations or prohibitions | "Never share API keys in messages" |
| **Preference** | Default choices or biases | "Prefer Python over JavaScript for scripts" |
| **Context/Memory** | Facts about the owner or environment | "The user works in healthcare consulting" |
| **Process** | Multi-step procedures or workflows | "When asked to research, first search, then summarize, then cite" |
| **Priority** | What matters most when goals conflict | "Speed over thoroughness for quick questions" |
| **Meta-Instruction** | Instructions about how to handle instructions | "If unsure, ask for clarification" |

---

## 2. Belief Extraction Process

For each file in the target agent's workspace:

### Step 1: Read the complete file
Read the full contents without summarizing or interpreting.

### Step 2: Segment into discrete beliefs
Break the file into individual directives. Each belief should be:
- A single, testable statement
- Attributable to a specific location (file + section/line reference)
- Classifiable by type (see table above)

### Step 3: Note the belief's scope
Some beliefs are global (apply always). Some are conditional (apply only in certain contexts). Some are skill-specific (apply only when that skill is active). Record the scope.

### Step 4: Record the belief's apparent intent
What was the author likely trying to achieve with this directive? This is your best interpretation — it may not match the user's current intent, and that gap is itself a finding.

---

## 3. Evaluation Criteria

Every belief is evaluated against the user's stated goals. The evaluation produces one of these classifications:

### 🟢 Aligned
The belief directly supports one or more stated goals. It is clear, specific, and actionable.

### 🟡 Neutral
The belief neither helps nor hinders stated goals. It may be a reasonable default or a matter of taste. Low priority for review, but worth noting if it consumes significant token budget.

### 🔴 Misaligned
The belief actively works against one or more stated goals. This is the highest-priority finding.

### ⚪ Stale
The belief references tools, models, APIs, workflows, or contexts that no longer exist or have changed significantly. It may have been aligned when written but is now outdated.

### 🟠 Conflicting
The belief contradicts another belief found elsewhere in the loaded context. Both cannot be true or both cannot be followed simultaneously.

### 🔵 Vague
The belief is too ambiguous to evaluate. It could be interpreted multiple ways, which means the agent's behavior will be inconsistent depending on how the model interprets it in any given session.

### ⚫ Redundant
The belief restates something already expressed elsewhere in the loaded context. See **Section 6: Duplication Analysis** for the detailed sub-classification, as not all redundancy is equally harmful.

---

## 4. Cross-File Conflict Detection

Conflicts are the most damaging belief pathology because the agent has no mechanism to resolve them — it simply picks one interpretation per session, often inconsistently.

### Common Conflict Patterns

1. **Tone Conflicts**: SOUL.md says "be concise" but a skill says "provide detailed explanations"
2. **Tool Preference Conflicts**: One file says "prefer tool A" while another says "use tool B for the same task"
3. **Identity Fragmentation**: Different files describe the agent's role differently, creating an incoherent persona
4. **Priority Inversions**: SOUL.md prioritizes speed, but a process directive in AGENTS.md requires thoroughness
5. **Capability Contradictions**: One file claims the agent can do X, another restricts it from doing X
6. **Stale vs. Updated**: An old file references deprecated behavior that a newer file has updated, but the old file was never cleaned up

### Conflict Severity

- **Critical**: Conflicts that fire frequently and produce visibly inconsistent behavior
- **Moderate**: Conflicts that fire occasionally or in edge cases
- **Low**: Conflicts between rarely-activated beliefs or beliefs with minimal behavioral impact

---

## 5. Token Efficiency Analysis

Every belief consumes context window tokens. The audit should assess:

- **Token cost vs. value**: Is this belief earning its token budget? A 200-token process description that fires on 1% of interactions may not be worth the cost.
- **Redundancy tax**: Beliefs stated multiple times across files multiply token cost without necessarily multiplying effectiveness. See Section 6 for nuance.
- **Specificity dividend**: Vague beliefs that require the model to interpret them may produce worse results than specific beliefs that cost the same tokens. Replacing vague with specific can improve performance at zero token cost.

> **Note:** Token counts produced during an audit are estimates, not precise measurements. LLMs cannot exactly count their own loaded context tokens. Estimates are useful for relative comparisons (which beliefs cost more than others) and for identifying obvious waste, but should not be treated as exact figures.

---

## 6. Duplication Analysis

Not all duplication is equally harmful. The audit classifies every instance of duplication into one of three categories:

### ⚫-1: Pure Waste
The same instruction stated the same way (or near-identically) in multiple files with no contextual reason for the repetition. This burns tokens for zero benefit.

**Recommendation:** Consolidate to a single location. Remove duplicates.

**Example:** SOUL.md says "Always respond in English" and AGENTS.md also says "Default language is English. Always respond in English."

### ⚫-2: Contextual Reinforcement
A directive restated in a skill-specific or context-specific way that may actually improve performance by firing in the exact moment the behavior matters most. The general version in SOUL.md sets the baseline; the specific version in a skill's SKILL.md reinforces it precisely when it counts.

**Recommendation:** Keep, but flag as a maintenance item. If the general version is updated, the specific version must also be updated or it becomes a conflict.

**Example:** SOUL.md says "Always confirm before destructive actions." A file management skill also says "Before deleting any file, ask the user to confirm." The skill-specific version is technically redundant but serves a reinforcement function.

### ⚫-3: Drift-Prone Duplication
Beliefs stated in multiple places that are identical today, but where updating one and forgetting to update the other will silently create a cross-file conflict. This is how many conflicts are born — they start as innocent redundancy.

**Recommendation:** Consolidate to a single source of truth. If the belief must exist in multiple places, add a comment noting the dependency (e.g., "Keep in sync with SOUL.md line 15").

**Example:** SOUL.md defines the agent's name as "Atlas" and USER.md also states "Your agent's name is Atlas." If the user later renames the agent in SOUL.md but forgets USER.md, the agent may inconsistently refer to itself.

### Duplication Summary in Report
For each instance of duplication, the audit records:
- The duplicated belief (both/all versions, with source files)
- Duplication sub-classification (⚫-1, ⚫-2, or ⚫-3)
- Token cost of the duplication (approximate)
- Recommendation (remove / keep with note / consolidate)

---

## 7. Report Structure

The audit report is organized as follows:

### Executive Summary
- Total beliefs extracted (count by file)
- Distribution by classification (aligned, misaligned, stale, conflicting, vague, redundant, neutral)
- Top 3-5 highest-impact findings
- Estimated token budget spent on non-aligned beliefs

### Goal Alignment Matrix
For each stated goal:
- Beliefs that support it
- Beliefs that hinder it
- Gaps (goals with no supporting beliefs)

### Findings (by priority)
Each finding includes:
- The belief text (quoted from the file)
- Source file and location
- Classification
- Reasoning
- Recommendation (keep / revise / remove / merge)
- Proposed revision (if applicable) — marked as draft for user approval

### Cross-File Conflict Register
Each conflict includes:
- The two (or more) conflicting beliefs
- Their source files
- Severity rating
- Recommended resolution

### Duplication Register
Each duplication instance includes:
- The duplicated beliefs (all versions)
- Their source files
- Sub-classification (⚫-1 Pure Waste / ⚫-2 Contextual Reinforcement / ⚫-3 Drift-Prone)
- Token cost
- Recommendation

### Token Efficiency Notes
- Beliefs consuming disproportionate tokens relative to their activation frequency
- Total token cost of redundancy (all ⚫ categories combined)
- Suggestions for more token-efficient formulations

---

## 8. Collaborative Review Protocol

After presenting findings, Clawdit enters collaborative review mode:

1. **Present findings one at a time**, starting with highest priority
2. **Wait for user response** before proceeding to the next finding
3. **Accept the user's decision** — if they want to keep a misaligned belief, that is their prerogative
4. **Offer to draft revisions** for beliefs the user wants to change
5. **Track decisions** so the user has a record of what was reviewed and what was decided
6. **Offer to generate updated files** incorporating all approved changes — but only write files with explicit user permission

---

## 9. Important Limitations

- Clawdit evaluates beliefs as written. It cannot observe the agent's actual runtime behavior to confirm whether beliefs are being followed as intended.
- Clawdit's analysis is only as good as the goal elicitation. Incomplete or vague goals produce incomplete or vague evaluations.
- Some beliefs may interact in complex ways that are not visible from static analysis alone. Clawdit should note when it suspects interaction effects but cannot confirm them.
- Clawdit does not evaluate the quality of the underlying LLM or the OpenClaw platform itself — only the belief files loaded into context.
