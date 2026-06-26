---
name: deep-research
description: "Universal deep research with 13-agent pipeline on Hermes Agent. 7 modes: full research, quick brief, paper review, lit-review, fact-check, Socratic guided research dialogue, systematic review with meta-analysis. Uses delegate_task for each agent. Triggers on: research, deep research, literature review, systematic review, meta-analysis, PRISMA, evidence synthesis, fact-check, guide my research, help me think through, 研究, 深度研究, 文獻回顧, 系統性回顧, 後設分析, 事實查核, 引導我的研究, 幫我釐清."
metadata:
  version: "2.9.3-hermes-1.0"
  last_updated: "2026-05-16"
  status: active
  adapted_from: "imbad0202/academic-research-skills v2.9.3"
  adapted_for: "Hermes Agent (deepseek-v4-pro)"
  task_type: open-ended
  license: "CC BY-NC 4.0"
  original_author: "Cheng-I Wu"
  original_license: "CC BY-NC 4.0"
  original_repo: "https://github.com/Imbad0202/academic-research-skills"
  copyright: "Copyright (c) 2026 Cheng-I Wu"
---
# Deep Research — Universal Academic Research (Hermes Edition)

📄 **License:** [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · Copyright (c) 2026 Cheng-I Wu  
🔗 **Original:** [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) v2.9.3  
🔄 **Adaptation:** Multi-agent pipeline implemented via `delegate_task` instead of Claude Code's internal agent system. All agent definitions, references, templates, and quality standards preserved unchanged from original. **This adaptation is distributed under the same CC BY-NC 4.0 license.**

**Model**: Uses `deepseek-v4-pro` (1M context / 384K max_tokens) for all agent tasks.

## Quick Start

```
Research the impact of AI on higher education quality assurance
```

**Execution** (Hermes orchestrator + delegate_task):
1. Scoping — delegate_task(research_question_agent + research_architect_agent)
2. Investigation — delegate_task(bibliography_agent + source_verification_agent)
3. Analysis — delegate_task(synthesis_agent + devils_advocate_agent)
4. Composition — delegate_task(report_compiler_agent)
5. Review — delegate_task(editor_in_chief + ethics_review + devils_advocate)
6. Revision — delegate_task(report_compiler_agent)

---

## Hermes-Specific Execution Model

**Core pattern**: The main Hermes agent is the ORCHESTRATOR. Each research phase spawns subagents via `delegate_task`. The orchestrator manages:
- Phase sequencing and checkpoint gating
- Context handoff between phases
- Quality enforcement (failure = halt and get user input)
- Mode selection (full/quick/socratic/etc.)

**Agent files** at `agents/` contain specialized prompts loaded as `context` in `delegate_task`.

**Reference files** at `references/` provide domain knowledge injected as-needed.

---

## Phase 1: SCOPING

### Step 1.1: Research Question
```python
delegate_task(
    goal="Transform the research topic '[USER_TOPIC]' into a precise, FINER-scored research question with scope boundaries. Output: RQ Brief with 2-3 sub-questions.",
    context="Use the agent definition at agents/research_question_agent.md for the full methodology. Apply FINER criteria (Feasible, Interesting, Novel, Ethical, Relevant).",
    toolsets=["file", "web"]
)
```

### Step 1.2: Methodology Blueprint
```python
delegate_task(
    goal="Design a methodology blueprint for the research question: [RQ_FROM_STEP_1]. Include: research paradigm, method selection, data strategy, analytical framework, validity criteria.",
    context="Use agent definition at agents/research_architect_agent.md. Reference: references/methodology_patterns.md.",
    toolsets=["file", "web"]
)
```

### Checkpoint 1 — Devil's Advocate
```python
delegate_task(
    goal="Review the Research Question Brief and Methodology Blueprint. Test for: RQ clarity, method appropriateness, scope validity. Output verdict: PASS or REVISE with specific feedback.",
    context="You are the Devil's Advocate. Use agent definition at agents/devils_advocate_agent.md. Reference: references/logical_fallacies.md, references/cross_agent_quality_definitions.md.",
    toolsets=["file"]
)
```
⚠️ **CRITICAL issues → HALT. Require user correction.** User must confirm before Phase 2.

---

## Phase 2: INVESTIGATION

### Step 2.1: Literature Search
```python
delegate_task(
    goal="Conduct a systematic literature search for [RQ]. Output: search strategy, inclusion/exclusion criteria, PRISMA-style flow, annotated bibliography in APA 7.0.",
    context="Use agent definition at agents/bibliography_agent.md. Reference: references/apa7_style_guide.md, references/source_quality_hierarchy.md.",
    toolsets=["file", "web"]
)
```

### Step 2.2: Source Verification
```python
delegate_task(
    goal="Verify and grade all sources from the bibliography. Apply evidence hierarchy grading (Level I-VII), predatory journal screening, conflict-of-interest flagging. Output: Verified & Graded Sources + Source Quality Matrix.",
    context="Use agent definition at agents/source_verification_agent.md. Reference: references/source_quality_hierarchy.md, references/cross_agent_quality_definitions.md.",
    toolsets=["file", "web"]
)
```

---

## Phase 3: ANALYSIS

### Step 3.1: Cross-Source Synthesis
```python
delegate_task(
    goal="Synthesize findings across all verified sources. Identify themes, contradictions, knowledge gaps. Output: Synthesis Narrative + Gap Analysis with evidence convergence/divergence mapping.",
    context="Use agent definition at agents/synthesis_agent.md. Reference: references/argumentation_reasoning_framework.md, references/interdisciplinary_bridges.md.",
    toolsets=["file"]
)
```

### Checkpoint 2 — Devil's Advocate
```python
delegate_task(
    goal="Review the synthesis. Check for cherry-picking, confirmation bias, logic chain validity, alternative explanations. Output verdict: PASS or REVISE.",
    context="Use agent definition at agents/devils_advocate_agent.md. Reference: references/logical_fallacies.md.",
    toolsets=["file"]
)
```

---

## Phase 4: COMPOSITION

```python
delegate_task(
    goal="Compile a full APA 7.0 research report from all prior materials. Structure: Title → Abstract → Intro → Lit Review → Methodology → Findings → Discussion → Conclusion → References. Word count: 3,000-8,000.",
    context="Use agent definition at agents/report_compiler_agent.md. Reference: references/apa7_style_guide.md. Include all prior phase outputs as context.",
    toolsets=["file"]
)
```

---

## Phase 5: REVIEW (3 agents in parallel)

```python
# Run all three simultaneously
delegate_task(tasks=[
    {
        "goal": "Editorial review: assess originality, rigor, evidence sufficiency, argument coherence, writing quality. Verdict: ACCEPT/MINOR/MAJOR/REJECT with line feedback.",
        "context": "Use agent definition at agents/editor_in_chief_agent.md. Reference: references/apa7_style_guide.md.",
        "toolsets": ["file"]
    },
    {
        "goal": "Ethics review: AI disclosure compliance, attribution integrity, dual-use screening, fair representation. Verdict: CLEARED/CONDITIONAL/BLOCKED.",
        "context": "Use agent definition at agents/ethics_review_agent.md. Reference: references/ethics_checklist.md, references/irb_decision_tree.md.",
        "toolsets": ["file"]
    },
    {
        "goal": "Final vulnerability scan: strongest counter-argument test, significance check, alternative explanations. Verdict: PASS/REVISE.",
        "context": "Use agent definition at agents/devils_advocate_agent.md. Reference: references/logical_fallacies.md.",
        "toolsets": ["file"]
    }
])
```

---

## Phase 6: REVISION

```python
delegate_task(
    goal="Revise the full report addressing all Phase 5 feedback. Incorporate editorial, ethics, and devil's advocate insights. Max 2 revision loops. Remaining issues → Acknowledged Limitations section.",
    context="Use agent definition at agents/report_compiler_agent.md. Include all Phase 5 review outputs and the current draft.",
    toolsets=["file"]
)
```

---

## Mode Selection

Before starting, determine the mode based on user intent:

| Mode | Phases Active | Output | Word Count |
|------|---------------|--------|------------|
| `full` (default) | All 6 phases | Full APA 7.0 report | 3,000-8,000 |
| `quick` | Phase 1(RQ) + 2(Biblio+Verification) + 4(Report) | Research brief | 500-1,500 |
| `review` | Phase 5 only | Reviewer report on provided text | N/A |
| `lit-review` | Phase 2 + 3 | Annotated bibliography + synthesis | 1,500-4,000 |
| `fact-check` | Phase 2.2 only | Verification report | 300-800 |
| `socratic` | Socratic Mentor (see below) | Research Plan Summary | N/A |
| `systematic-review` | All phases + RoB + Meta-Analysis | PRISMA 2020 report | 5,000-15,000 |

**Mode Selection Logic**:
- User has clear RQ and needs full report → `full`
- User has vague idea, needs guidance → `socratic`
- User has paper to evaluate → `review`
- User needs quick summary → `quick`
- User only needs literature → `lit-review`
- User needs to verify claims → `fact-check`
- PRISMA-compliant review needed → `systematic-review`

When ambiguous between `socratic` and `full`, prefer `socratic`.

---

## Socratic Mode

5-layer dialogue guiding users from vague ideas to concrete research questions.

Core principle: ⚠️ **Never give direct answers.** Guide through questions.

### Agent (single delegate_task per layer):
```python
delegate_task(
    goal="Layer [N] Socratic dialogue for research topic: [USER_TOPIC]. Previous layers: [LAYER_OUTPUTS]. Ask questions that probe [LAYER_FOCUS]. Never give answers.",
    context="Use agent definition at agents/socratic_mentor_agent.md. Reference: references/socratic_mode_protocol.md, references/socratic_questioning_framework.md.",
    toolsets=["file"]
)
```

**Layers**: Clarification → Assumption Probing → Evidence/Reasoning → Viewpoint/Perspective → Implication/Consequence

Auto-end after 10 rounds without convergence → suggest switching to `full` mode.

---

## Systematic Review Mode

PRISMA 2020-compliant. Adds two extra agents:

```python
# After Phase 2 bibliography:
delegate_task(goal="Assess risk of bias using RoB 2 (RCTs) and ROBINS-I (non-randomized). Traffic-light visualization.",
    context="Use agent definition at agents/risk_of_bias_agent.md. Reference: references/systematic_review_toolkit.md.",
    toolsets=["file"])

# After Phase 3 synthesis:
delegate_task(goal="Design and execute meta-analysis or narrative synthesis. Effect sizes, heterogeneity (I²), GRADE assessment.",
    context="Use agent definition at agents/meta_analysis_agent.md. Reference: references/systematic_review_toolkit.md.",
    toolsets=["file"])
```

---

## Critical Rules (IRON RULES)

1. ⚠️ **Every claim must have a citation** — no unsupported assertions
2. ⚠️ **Gray zone = FAIL** — if you cannot confirm a reference exists, it does not go in the report
3. ⚠️ **Devil's Advocate CRITICAL → HALT** — explain the issue, require user correction
4. ⚠️ **Ethics BLOCKED → HALT** — list issues and remediation path
5. ⚠️ **Max 2 revision loops** — remaining issues become Acknowledged Limitations
6. ⚠️ **User confirmation after Phase 1** — do not auto-continue
7. **Vibe citing = forbidden** — every reference must be independently verifiable
8. **No phase skipping** — complete each phase fully before moving to next

---

## Orchestrator Checklist

Before starting each phase, the orchestrator (main Hermes agent) MUST:
1. Verify the previous phase checkpoint passed
2. Load the relevant agent file via `read_file`
3. Pass all prior outputs as context to `delegate_task`
4. Review subagent output before proceeding
5. Respect HALT conditions (ask user, don't auto-fix)

---

## Failure Paths

| Scenario | Recovery |
|----------|----------|
| RQ cannot converge | Provide 3 candidate RQs, suggest lit-review |
| Insufficient literature (<5 sources) | Expand search strategy, suggest alternative keywords |
| Devil's Advocate CRITICAL | HALT, explain, require correction |
| Ethics BLOCKED | HALT, list issues |
| Socratic non-convergence (>10 rounds) | Suggest switching to full mode |

---

## Agent File References

| Agent | File |
|-------|------|
| research_question_agent | agents/research_question_agent.md |
| research_architect_agent | agents/research_architect_agent.md |
| bibliography_agent | agents/bibliography_agent.md |
| source_verification_agent | agents/source_verification_agent.md |
| synthesis_agent | agents/synthesis_agent.md |
| report_compiler_agent | agents/report_compiler_agent.md |
| editor_in_chief_agent | agents/editor_in_chief_agent.md |
| devils_advocate_agent | agents/devils_advocate_agent.md |
| ethics_review_agent | agents/ethics_review_agent.md |
| socratic_mentor_agent | agents/socratic_mentor_agent.md |
| risk_of_bias_agent | agents/risk_of_bias_agent.md |
| meta_analysis_agent | agents/meta_analysis_agent.md |
| monitoring_agent | agents/monitoring_agent.md |

All agent files are the original v2.9.3 definitions with unchanged methodology.
They are loaded as `context` in `delegate_task` calls.

---

## Output Language

Follow user's language. Academic terminology kept in English.

---

## Anti-Patterns

| # | Anti-Pattern | Correct Behavior |
|---|-------------|-----------------|
| 1 | Confirmation bias in source selection | Devil's Advocate checkpoint must include counter-evidence search |
| 2 | Cherry-picking evidence | Report full evidence landscape including conflicting findings |
| 3 | Vibe citing (mixing elements from 2-3 real papers into fake reference) | Every reference must be verified independently |
| 4 | ⚠️ Treating "difficult to verify" as acceptable | Gray zone = FAIL |
| 5 | Skipping phases | Complete each phase fully |
| 6 | Shallow Socratic mode | Ask genuine questions, never lead to predetermined conclusions |
| 7 | Source tier inflation | Apply evidence hierarchy strictly |

---

## Handoff to academic-paper

After research complete, these materials can be handed off:
1. Research Question Brief
2. Methodology Blueprint
3. Annotated Bibliography
4. Synthesis Report
5. [If socratic] INSIGHT Collection and Research Plan Summary

User says "now help me write a paper" → switch to `academic-paper` skill.

## Security & Privacy

**Multi-agent design disclosure:** This skill delegates research tasks across multiple subagents via `delegate_task`. Research content and intermediate outputs are processed by these agents. Use only with research topics you are comfortable processing through the AI provider's delegated-agent workflow.

**Tool access:** Subagents are granted `file` tools (for writing output) and `web` tools (for literature search only). No terminal or system tools are exposed during review/composition phases.

**Agent files:** The `agents/` directory contains academic research prompt templates (role definitions, methodology guidelines, quality rubrics). These are task instructions loaded as `context` in `delegate_task` calls — NOT system prompt overrides. Frontmatter in agent files (e.g., `name:`, `description:`) is metadata only.
