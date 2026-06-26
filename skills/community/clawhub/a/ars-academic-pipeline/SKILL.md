---
name: academic-pipeline
description: "10-stage end-to-end research-to-publication pipeline orchestrator on Hermes Agent. Stages: planning → deep-research → academic-paper → academic-paper-reviewer → revision → polish → ethics → disclosure → format → deliver. Resume support. Uses delegate_task for each stage. Triggers: full pipeline, end-to-end research, research to paper, publish paper, 完整學術流程, 從研究到發表."
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
# Academic Pipeline — 10-Stage End-to-End (Hermes Edition)

📄 **License:** [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · Copyright (c) 2026 Cheng-I Wu  
🔗 **Original:** [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills)  
🔄 **Adaptation:** Orchestration pipeline implemented via `delegate_task` instead of Claude Code's internal agent system. All agent definitions, references, and quality standards preserved unchanged from original. **This adaptation is distributed under the same CC BY-NC 4.0 license.**

Orchestrates the full academic workflow from research idea to publication-ready output.

## 10 Stages

| Stage | Skill Used | Key Output |
|-------|-----------|------------|
| 1. Planning | intake + mode selection | Project Plan with stage gating |
| 2. Research | deep-research (full/quick) | RQ Brief + Methodology + Bibliography + Synthesis |
| 3. Paper Draft | academic-paper (full) | Complete paper draft |
| 4. Peer Review | academic-paper-reviewer (full) | 5-panel review + Editorial Decision |
| 5. Revision | academic-paper (revision) | Revised draft + tracked changes |
| 6. Polish | academic-paper (revision) | Final polished manuscript |
| 7. Ethics Check | academic-paper-reviewer (quick) | Ethics clearance |
| 8. AI Disclosure | academic-paper (disclosure) | Venue-specific AI statement |
| 9. Format | academic-paper (format-convert) | LaTeX/DOCX/PDF + cover letter |
| 10. Deliver | file output | Publication package |

## Hermes Execution

The orchestrator (main Hermes agent):
1. **Stage 1**: Clarify user intent → select modes → create Project Plan
2. **Stage 2-6**: Sequential delegate_task calls, each loading the relevant skill
3. **Stage 7-9**: Lightweight parallel or sequential based on dependencies
4. **Stage 10**: Write final package to disk

### Key Checkpoints
- Stage 1→2: User approves Project Plan
- Stage 2→3: Research report accepted by user
- Stage 4→5: Review decision received
- Stage 6→7: Polished draft ready

### Resume Support
Pipeline state stored in `~/.hermes/sessions/`. User can resume with:
```
Continue the academic pipeline from Stage 4
```

## Usage Patterns

**Full pipeline**:
```
Take "AI impact on HE quality assurance" through the full pipeline to publication-ready manuscript
```

**Partial pipeline**:
```
Start from Stage 3 with my existing deep-research output
```

**Resume**:
```
Resume pipeline from Stage 5 with reviewer comments: [comments]
```

## Integration with Hindsight Memory
Pipeline state and key outputs are retained to Hindsight for long-term tracking:
```
hindsight memory retain --content "[stage_output]" --tags "pipeline,stage-N"
```

## Critical Rules
1. ⚠️ Each stage MUST complete before the next begins
2. ⚠️ User confirmation at all IRON RULE checkpoints
3. ⚠️ Ground truth isolation: review stage must NOT see author identity

## Security & Privacy

**Orchestration disclosure:** This pipeline orchestrates multiple skills (research → writing → review) via `delegate_task`. All content passes through the AI provider's workflow. Use only with topics you are comfortable processing through AI.

**Tool access:** This pipeline delegates to sub-skills which independently control their own tool access. No stage is granted terminal, web, or system tools beyond what each sub-skill permits.

**Agent files:** All `agents/` directories across sub-skills contain academic prompt templates, NOT system prompt overrides.
