---
name: academic-paper-reviewer
description: "7-agent paper review system on Hermes Agent. 6 modes (full/re-review/quick/methodology-focus/guided/calibration). 5-panel review with editorial decision, revision roadmap, and calibration metrics. Uses delegate_task for each reviewer. Triggers: review paper, peer review, manuscript review, check revisions, calibrate reviewer, 審稿, 同儕審查, 論文審查."
metadata:
  version: "1.0-hermes-1.0"
  last_updated: "2026-05-16"
  status: active
  adapted_from: "imbad0202/academic-research-skills"
  adapted_for: "Hermes Agent (deepseek-v4-pro)"
  task_type: open-ended
  license: "CC BY-NC 4.0"
  original_author: "Cheng-I Wu"
  original_license: "CC BY-NC 4.0"
  original_repo: "https://github.com/Imbad0202/academic-research-skills"
  copyright: "Copyright (c) 2026 Cheng-I Wu"
---
# Academic Paper Reviewer — 7-Agent Review System (Hermes Edition)

📄 **License:** [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · Copyright (c) 2026 Cheng-I Wu  
🔗 **Original:** [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills)  
🔄 **Adaptation:** Multi-agent review system implemented via `delegate_task` instead of Claude Code's internal agent system. All agent definitions, references, and quality standards preserved unchanged from original. **This adaptation is distributed under the same CC BY-NC 4.0 license.**

## Quick Start

```
Review this paper for journal submission
```

## Agent Team

| # | Agent | Role |
|---|-------|------|
| 1 | intake_agent | Receive paper, determine review type |
| 2 | methodology_reviewer | Method rigor assessment |
| 3 | evidence_reviewer | Evidence sufficiency & citation quality |
| 4 | argument_reviewer | Logical coherence & argument structure |
| 5 | domain_reviewer | Domain expertise & literature positioning |
| 6 | editor_in_chief | Aggregate reviews → editorial decision |
| 7 | revision_coach | Convert reviews → actionable roadmap |

## Hermes Execution

### Full Mode: 5-Panel Parallel Review
```
delegate_task(tasks=[
    {"goal": "Review manuscript methodology: design appropriateness, validity threats, replicability. Score 1-5.", "context": "Use agents/methodology_reviewer.md", "toolsets": ["file"]},
    {"goal": "Review evidence: citation quality, source credibility, evidence hierarchy alignment. Score 1-5.", "context": "Use agents/evidence_reviewer.md", "toolsets": ["file"]},
    {"goal": "Review argument: logical flow, claim-evidence alignment, counter-argument handling. Score 1-5.", "context": "Use agents/argument_reviewer.md", "toolsets": ["file"]},
    {"goal": "Review domain positioning: literature coverage, theoretical grounding, contribution significance. Score 1-5.", "context": "Use agents/domain_reviewer.md", "toolsets": ["file"]}
])
```

### Editorial Decision
```
delegate_task(goal="Aggregate all 4 reviewer reports. Apply weighted scoring (Method 30%, Evidence 25%, Argument 25%, Domain 20%). Issue editorial decision: Accept/Minor Revision/Major Revision/Reject with justification.", context="Use agents/editor_in_chief.md", toolsets=["file"])
```

### Revision Roadmap
```
delegate_task(goal="Convert editorial decision + reviewer reports into structured Revision Roadmap: prioritized action items, estimated effort, dependency mapping.", context="Use agents/revision_coach.md", toolsets=["file"])
```

## 6 Modes

| Mode | Trigger | Agents |
|------|---------|--------|
| `full` | "Review paper" | All 7 |
| `re-review` | "Check revisions" | 2→3→4→6 |
| `quick` | "Quick review" | 6 only (EIC assessment) |
| `methodology-focus` | "Check methodology" | 2 only |
| `guided` | "Guide me to improve" | Socratic: 6 with user interaction |
| `calibration` | "Calibrate reviewer" | All + calibration metrics output |

## Calibration Mode
Measures reviewer accuracy: FNR (False Negative Rate), FPR (False Positive Rate), AUC. Requires ground-truth labels on prior reviewed papers.

## Critical Rules
1. ⚠️ Reviewers are paper-blind (don't see author info)
2. ⚠️ Every criticism must include specific actionable suggestion
3. ⚠️ Calibration mode requires 5+ ground-truth papers

## Security & Privacy

**Multi-agent design disclosure:** This skill delegates review tasks across multiple subagents via `delegate_task`. Manuscript content and intermediate review outputs are processed by these agents. Use only with manuscripts you are comfortable having processed through the AI provider's delegated-agent workflow. Remove confidential material not needed for review.

**Tool access:** Subagents are granted only `file` tools for reading/writing review outputs. No terminal, web, or system tools are exposed.

**Agent files:** The `agents/` directory contains academic peer-review prompt templates (role definitions, scoring rubrics, methodology guidelines). These are task instructions loaded as `context` in `delegate_task` calls — NOT system prompt overrides.
