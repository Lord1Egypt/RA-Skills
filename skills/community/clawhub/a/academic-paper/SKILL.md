---
name: academic-paper
description: "12-agent academic paper writing pipeline on Hermes Agent. 10 modes (full/plan/outline/revision/revision-coach/abstract/lit-review/format-convert/citation-check/disclosure). 6 paper types, 5 citation formats, bilingual abstracts, LaTeX/DOCX/PDF output. Uses delegate_task for each agent. Triggers: write paper, academic paper, guide my paper, parse reviews, AI disclosure, 寫論文, 學術論文, 引導我寫論文, 審查意見."
metadata:
  version: "3.1.1-hermes-1.0"
  last_updated: "2026-05-16"
  status: active
  adapted_from: "imbad0202/academic-research-skills v3.1.1"
  adapted_for: "Hermes Agent (deepseek-v4-pro)"
  task_type: open-ended
  license: "CC BY-NC 4.0"
  original_author: "Cheng-I Wu"
  original_license: "CC BY-NC 4.0"
  original_repo: "https://github.com/Imbad0202/academic-research-skills"
  copyright: "Copyright (c) 2026 Cheng-I Wu"
---
# Academic Paper — 12-Agent Writing Pipeline (Hermes Edition)

📄 **License:** [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · Copyright (c) 2026 Cheng-I Wu  
🔗 **Original:** [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) v3.1.1  
🔄 **Adaptation:** Multi-agent pipeline implemented via `delegate_task` instead of Claude Code's internal agent system. All agent definitions, references, templates, and quality standards preserved unchanged from original. **This adaptation is distributed under the same CC BY-NC 4.0 license.**

## Quick Start

```
Write a paper on the impact of AI on higher education quality assurance
```

## Agent Team

| # | Agent | Phase |
|---|-------|-------|
| 1 | intake_agent | Phase 0: Config interview |
| 2 | literature_strategist_agent | Phase 1: Literature search |
| 3 | structure_architect_agent | Phase 2: Structure/outline |
| 4 | argument_builder_agent | Phase 3: Argument construction |
| 5 | draft_writer_agent | Phase 4: Full draft |
| 6 | citation_compliance_agent | Phase 5a: Citation check |
| 7 | abstract_bilingual_agent | Phase 5b: Bilingual abstract |
| 8 | peer_reviewer_agent | Phase 6: Peer review (max 2 loops) |
| 9 | formatter_agent | Phase 7: Output formatting |
| 10 | socratic_mentor_agent | Plan mode guide |
| 11 | visualization_agent | Figures/charts |
| 12 | revision_coach_agent | Reviewer comment parsing |

## Hermes Execution Pattern

All phases use `delegate_task`. Agent files at `agents/` loaded as context.

### Phase 0: Configuration
```
delegate_task(goal="Conduct paper configuration interview: paper type, discipline, journal, citation format, output format, language, word count.", context="Use agents/intake_agent.md")
```

### Phase 1: Literature
```
delegate_task(goal="Design search strategy, screen sources, produce annotated bibliography.", context="Use agents/literature_strategist_agent.md")
```

### Phase 2: Architecture
```
delegate_task(goal="Select paper structure, create detailed outline with word count allocation and evidence mapping.", context="Use agents/structure_architect_agent.md. Reference: references/paper_structure_patterns.md")
```
⚠️ User must approve outline before Phase 3.

### Phase 3: Argumentation
```
delegate_task(goal="Build argument blueprint: claim-evidence chains, logical flow, counter-argument handling.", context="Use agents/argument_builder_agent.md")
```

### Phase 4: Drafting
```
delegate_task(goal="Write full paper draft section by section, maintaining discipline register and word count.", context="Use agents/draft_writer_agent.md. Reference: references/writing_quality_check.md")
```

### Phase 5: Citations + Abstract (parallel)
```
delegate_task(tasks=[
    {"goal": "Verify all citations: format compliance, reference list completeness, DOI checking.", "context": "Use agents/citation_compliance_agent.md", "toolsets": ["file"]},
    {"goal": "Write bilingual abstract (zh-TW + EN) with 5-7 keywords each. Independent composition, not translation.", "context": "Use agents/abstract_bilingual_agent.md. Reference: references/abstract_writing_guide.md", "toolsets": ["file"]}
])
```

### Phase 6: Peer Review
```
delegate_task(goal="Simulated double-blind review on 5 dimensions: Originality(20%), Method Rigor(25%), Evidence(25%), Argument(15%), Writing(15%). Max 2 loops.", context="Use agents/peer_reviewer_agent.md")
```

### Phase 7: Format
```
delegate_task(goal="Convert to target format (LaTeX/DOCX/PDF/Markdown). Apply journal formatting. Generate cover letter.", context="Use agents/formatter_agent.md. Reference: references/latex_template_reference.md")
```

## 10 Modes

| Mode | Trigger | Agents |
|------|---------|--------|
| `full` | "Write a paper" | All 9 core |
| `outline-only` | "Paper outline" | 1→2→3 |
| `revision` | "Revise paper" | 8→5→6 |
| `abstract-only` | "Write abstract" | 1→7 |
| `lit-review` | "Literature review" | 1→2 |
| `format-convert` | "Convert to LaTeX" | 9 only |
| `citation-check` | "Check citations" | 6 only |
| `plan` | "Guide my paper" | 1→10→3→4 |
| `revision-coach` | "Parse reviews" | 12 only |
| `disclosure` | "AI disclosure statement" | 9 only |

## Critical Rules
1. ⚠️ User must confirm Paper Configuration Record before Phase 1
2. ⚠️ Max 2 revision loops; unresolved → Acknowledged Limitations
3. ⚠️ Every claim must have a citation or be from paper's own data
4. ⚠️ Zero fabricated citations — every reference verified via DOI

## Handoff from deep-research
`intake_agent` auto-detects deep-research materials (RQ Brief, Bibliography, Synthesis) and skips redundant steps.

## Security & Privacy

**Multi-agent design disclosure:** This skill delegates writing tasks across multiple subagents. Paper content is processed through the AI provider's delegated-agent workflow. Use only with content you are comfortable having processed by AI.

**Tool access:** Subagents are granted only `file` tools for reading/writing paper drafts. No terminal, web, or system tools are exposed.

**Agent files:** The `agents/` directory contains academic writing prompt templates. These are task instructions for `delegate_task` — NOT system prompt overrides.
