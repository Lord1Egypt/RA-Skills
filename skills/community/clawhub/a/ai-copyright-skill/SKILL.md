---
name: AI-Copyright-Skill
description: "AI-native IP skill: generate patent applications, software copyright materials, or technical disclosures from AI project code/papers/docs, with direct Word and PPT output. Covers 7 AI domains, 11 claim templates, patentability check, desensitization, prior-art search, and self-check."
version: "2.0.0"
author: jaccen
tags: ["patent", "software-copyright", "ip", "ai", "intellectual-property", "docx", "pptx", "3d-vision", "generative-ai", "embodied-ai", "rag", "ai-watermark"]
---

# AI IP Document Generation

Generate Chinese patent applications, software copyright registration materials, or technical disclosure reports from AI project code, research papers, and design docs. Direct Word (.docx) + PPT (.pptx) output. Built-in 7 AI domain coverage with 11 claim templates.

Three output paths:
- **Patent**: CNIPA-format invention patent (claims + specification + abstract), with technical disclosure as intermediate deliverable
- **Software Copyright**: CPCC registration materials (manual + source code document)
- **Technical Disclosure**: From papers/notes to agent-deliverable disclosure

## 7 AI Domains x 22 Sub-Directions

| Domain | Sub-Directions | Claim Template |
|--------|---------------|----------------|
| Perception AI | 2D CV · 3D Vision & Graphics · Audio/Video · Sensor Fusion | 2.1 Architecture · 2.2 3D Vision |
| Cognitive & Language | LLM · Multimodal LLM · RAG · Knowledge Graph | 2.3 Training · 2.4 MLLM · 2.5 RAG |
| Generative AI | Diffusion & Controlled Gen · AIGC Watermark · Style Transfer | 2.6 Diffusion |
| Decision & Interaction | Agent · Embodied AI · RL | 2.7 Agent · 2.8 VLA |
| AI Engineering | Training/Fine-tuning · Inference Opt · Data Engineering · Edge/IoT | 2.9 Inference · 2.10 Data |
| AI Safety & Governance | Adversarial Defense · Watermark · Federated Learning · Alignment | 2.11 Watermark |
| Industry Apps | Autonomous Driving · Industry QC · Healthcare · Finance · AI4Science · Digital Content | Domain-adapted |

## Triggers

patent / claims / specification / software copyright / disclosure / IP application / paper-to-patent / `/ai-copyright` / `/AI知产`

**Iteration**: When user modifies existing output, enter iterative correction flow directly.

## Overall Flow

```
Phase 0  Patentability Pre-Assessment (patent path only)
Phase A  Requirement Diagnosis → path + domain + risk level
Phase B  Project Analysis → auto-detect (11 types + 6 industries) + extract key points
Phase C  Generation (branch by path)
  C1 Patent: search → layout → disclosure → claims (11 templates) → specification → abstract → self-check
  C2 Software Copyright: manual (4 templates) → source code doc → self-check
  C3 Technical Disclosure: mapping (6 general + 7 domain-specific) → drafting → self-check
Phase D  Confirmation Gate
Phase E  Iterative Correction
Phase F  Word Output (docx-js, auto)
Phase G  Briefing PPT (python-pptx, patent default)
```

## Phase 0: Patentability Pre-Assessment

Per `references/ai-patent-special.md` §1, check three elements:

| Element | Check | Pass Standard |
|---------|-------|---------------|
| Technical Problem | Anchored to specific scenario | Not "low efficiency" / "poor accuracy" |
| Technical Means | Algorithm steps bound to system architecture | Each step linked to HW/SW component |
| Technical Effect | Quantifiable | Concrete numbers or comparison baselines |

### Domain Risk Assessment (§1.3)

| Risk | Domain | Pitfall | Countermeasure |
|------|--------|---------|----------------|
| HIGH | Generative AI (pure content gen) | Classified as "rules of mental activities" | Must bind to tech scenario + conditional control means |
| HIGH | Financial risk control | Classified as "business method" | Must bind to data processing means |
| HIGH | AI alignment / explainability | Classified as "rules of mental activities" | Must bind to safety assurance in specific app scenario |
| MED | Embodied AI | Pure motion control = mental activities | Bind each step to sensor input + actuator output |
| MED | Reinforcement Learning | Pure strategy optimization = math method | Bind to physical system + physics-constrained reward |
| MED | RAG | Pure information retrieval = info expression | Must show complete technical pipeline |
| MED | AIGC watermark | Pure info marking = info expression | Watermark embedding must bind to model internal layers |

**Decision**: All pass + low risk → proceed; All pass + high risk → proceed with mandatory domain countermeasures; Means fail → switch to disclosure path; Effect fail → supplement quantitative comparison.

## Phase A: Requirement Diagnosis

Confirm with user: path selection, tech topic, AI domain (7 domains / 22 directions, auto-detect assisted), applicant info, inventor info, existing materials.

**Gate**: Output 3-5 line diagnosis summary (including domain attribution and risk level).

## Phase B: Project Analysis

### B.1 Auto-Detection (§1.1 Decision Tree)

```
Entry file → Project type
app.py/main.py/serve.py → AI Service
train.py/trainer.py → AI Training
inference.py/predict.py → AI Inference
render.py/gaussian.py/nerf.py → 3D Vision
generate.py/diffusion.py → Generative AI
robot.py/vla.py → Embodied AI
pipeline.py + langchain → Agent
pipeline.py + rag/faiss → RAG System
package.json → Frontend/Fullstack
```

Also detect 6 industry categories (§1.3): autonomous driving / industry / healthcare / finance / AI4Science / digital content.

### B.2 Key Points Extraction

Priority: model definition → training/inference scripts → rendering/generation/control scripts → papers → design docs → README.

Output: **Key Points List** (architecture/algorithm/engineering-level innovations, scheme skeleton, key params, distinctions from prior art, quantifiable effects, domain attribution).

**Gate**: Present key points list for user confirmation.

## Phase C1: Patent Application

### C1.1 Prior Art Search

Online search 2-3 rounds: CNIPA patent DB, Google Patents, arXiv. Suggest CPC classification (§6, 6 groups / 30+ codes).

### C1.2 Layout Advisory (§2)

| Innovation Distribution | Layout Strategy |
|------------------------|-----------------|
| Core innovation in architecture | Single application (arch + training + inference) |
| Architecture + training independent | 2 applications |
| Independent deployment optimization | 3 applications (arch + training + deployment) |
| 3D reconstruction + rendering independent | 2 applications |
| Generation model + control independent | 2 applications |
| Embodied perception + control independent | 2 applications (perception-decision + control-execution) |

### C1.3 Technical Disclosure (Intermediate Deliverable)

7-chapter structure: Invention Name → Tech Field → Background & Prior Art Defects → Invention Content (purpose + scheme + effects) → Figure Description → Specific Embodiments (optimal + alternative) → Key Innovation Summary (3-5 points).

Data source: Phase B key points + C1.1 search results + C1.2 layout advice.

### C1.4 Claims

Per `references/ai-patent-claims-guide.md`. Structure: Method (1 independent + 3-8 dependent) + System (1 independent + 3-8 dependent, step-by-step correspondence) + Storage Medium (1 independent).

**11 Claim Templates by Domain (§2)**:

| # | Type | Domain | Key Structure |
|---|------|--------|---------------|
| 2.1 | Model Architecture | Perception (2D) | Sub-module → processing action → intermediate result chain |
| 2.2 | 3D Vision & Graphics | Perception (3D) | Capture → sparse reconstruction → dense optimization → rendering (4-stage) + rendering computation sub-steps |
| 2.3 | Training Method | AI Engineering | Data construct → init → forward → loss → optimize → converge (6-step) |
| 2.4 | Multimodal LLM | Cognitive & Language | Multi-encoder → projection layer → fusion → decode |
| 2.5 | RAG | Cognitive & Language | Query parse → retrieve → rerank → context reconstruct → generate (5-stage) |
| 2.6 | Diffusion & Controlled Gen | Generative AI | Condition encode → inject → denoise → decode + condition injection sub-steps |
| 2.7 | Agent | Decision & Interaction | Intent → plan → tool execute → observe/reflect → respond |
| 2.8 | Embodied AI (VLA) | Decision & Interaction | Sensor perception → encode+fuse → policy → actuator drive + feedback |
| 2.9 | Inference Optimization | AI Engineering | Original model → optimize → inference strategy → result |
| 2.10 | Data Processing | AI Engineering | Acquire → preprocess → augment → downstream |
| 2.11 | AI Watermark & Traceability | AI Safety | Embed phase (position → generate → inject) + Verify phase (extract → match) |

**Domain-Specific Requirements (§1.3)**:

1. Every step must link to system component ("executed via GPU parallel computing unit")
2. **3D Vision**: Must include full 4-stage pipeline; rendering step must expand rendering formula
3. **Generative AI**: Condition injection step must specify injection method (cross-attention/adapter/ControlNet) to avoid "pure content generation" rejection
4. **Embodied AI**: Every step must bind to sensor input + actuator output; include safety constraint dependent claim
5. **RAG**: Must show complete 5-stage technical pipeline to avoid "pure information retrieval" rejection
6. **AI Watermark**: Embed step must specify injection layer/position/encoding; verify step must quantify robustness metrics
7. Training: Must include training data construction, loss function, optimization strategy
8. Multimodal: Must include modality encoding → cross-modal alignment → fusion → decoding

**Dependent Claim Expansion**: General 5-layer (module structure → computation method → param range → preferred embodiment → training features) + 5 domain-specific expansion tables (§3.2).

### C1.5 Specification

5-chapter structure: Tech Field → Background (prior art + defects) → Invention Content (problem + scheme + beneficial effects, must be quantified) → Figure Description (13-type figure requirements in §4) → Specific Embodiments.

**Desensitization Rules (§5)**: 6 general replacements + 14 industry-specific + 4 3DGS/NeRF-specific.

Figures: Use fenced mermaid (`flowchart TB`/`LR`). 13-type AI system figure requirements per §4.

### C1.6 Abstract

≤300 chars. Covers: tech domain + core scheme + main effect. No commercial terms. Replace algorithm names with generic expressions.

### C1.7 Quality Self-Check (100-point)

| Item | Points | Standard |
|------|--------|----------|
| Independent claim completeness | 15 | -5 per missing feature |
| Dependent claim back-reference correctness | 10 | -3 per error |
| Method + System + Medium triple complete | 10 | -5 per missing type |
| Specification sufficient disclosure | 15 | Enabling for skilled person |
| Embodiments cover all claim features | 15 | -3 per uncovered feature |
| Beneficial effects quantified | 10 | -3 per vague assertion |
| Terminology consistency | 5 | -1 per synonym |
| Abstract corresponds to claim 1 | 5 | -5 if not |
| Desensitization completeness | 10 | -3 per leak |
| Figure numbering consistency | 5 | -1 per inconsistency |

≥80: deliver. 60-80: auto-fix and deliver. <60: rewrite.

## Phase C2: Software Copyright

Per `references/ai-software-copyright-guide.md`.

### C2.1 Software Manual (10-15 pages, ≥6 screenshots)

4 templates by project type:

| Project Type | Template | Key Sections |
|-------------|----------|-------------|
| General AI service | §3.1 General | Standard 5 chapters |
| 3D Vision/Reconstruction | §3.2 3D Vision | Capture → reconstruct → render → export |
| Generative AI | §3.3 Gen-AI | Condition input → generation engine → safety management |
| Embodied AI | §3.4 Embodied | Perception → decision → execution → simulation → monitoring |

Key notes: Target non-technical reviewers; use `[Screenshot: feature name]` placeholders; describe deployment/config/monitoring for HCI requirement; declare open-source pre-trained weights outside protection scope.

### C2.2 Source Code Document (front 30 + back 30 pages, ≥50 lines/page)

12-level file priority (§2.1): model.py(train required) → train.py(required) → inference.py(required) → render.py(3D vision required) → dataset.py → loss.py → generate.py(gen-AI required) → control.py(embodied required) → retriever.py(RAG required) → config.yaml(optional).

Desensitization (§2.2): Remove API keys, absolute paths, internal addresses, personal info, hardware models, cloud URLs, DB passwords. Retain algorithm comments.

### C2.3 Quality Self-Check

Pages 15 + Screenshots 10 + Feature coverage 15 + Non-tech description 10 + GPU/CUDA info 10 + Code pages 15 + Lines per page 10 + Name consistency 5 + No secret leaks 10.

## Phase C3: Technical Disclosure

### C3.1 Paper-to-Disclosure Mapping (§3)

**General 6-type mapping**: Research Problem → Technical Problem | Contribution → Technical Solution | Method Modules → Implementation Units | Algorithm Flow → Implementation Flow | Experimental Outcome → Expected Effects | Ablation Study → Alternative Embodiments.

**Domain-specific mapping (§3.2)**: 3D Vision (rendering formula → claim step) | Generative AI (noise schedule → claim step, condition injection → dependent claim) | Embodied AI (Sim2Real → adaptation step) | RL (reward function → computation step) | RAG (retrieval strategies → dependent claims) | AI Watermark (robustness experiments → verification step) | AI4Science (physics constraints → necessary feature).

### C3.2 Drafting

7-chapter structure (same as C1.3).

### C3.3 Quality Self-Check

Problem anchoring 15 + Implementability 20 + Quantified comparison 15 + Clear distinction 15 + Figure coverage 15 + Agent comprehensibility 10 + Completeness 10.

## Phase D: Confirmation Gate

After each phase: present summary, options: Confirm / Modify / Switch path / Save progress (.temp/ai-ip-progress.md).

## Phase E: Iterative Correction

Identify → Locate → Targeted fix → Diff annotation (`<!-- Revision -->`) → Save as v{N} → Re-run affected self-check items only. Do NOT re-run full pipeline.

## Phase F: Word Output

Auto-executed after Phase C (unless user requests md only). Uses docx-js workflow: `.temp/{case}-docx.js`.

| Path | Output |
|------|--------|
| Patent | disclosure.docx + patent.docx (cover + claims + spec + abstract) + briefing.pptx |
| Software Copyright | manual.docx + source_code.docx |
| Technical Disclosure | single disclosure.docx |

Format: Song Ti 24pt body / Hei Ti 32-28pt headings / 1.5x line spacing / 480DXA indent / 1-inch margins. Source code: Courier New 18pt, ≥50 lines/page.

Alternatives: `md` / `docx` (default) / `both`.

## Phase G: Briefing PPT

Auto for patent path; `--ppt` for others. python-pptx workflow: `.temp/{case}-ppt.py`.

5-8 slides: Cover → Background & Pain Points → Core Innovation → System Architecture → Effects Comparison → Patent Layout → Implementation Plan. 16:9, blue theme (#1B3A5C + #3B82F6), Microsoft YaHei font.

## Output Specification

```
outputs/{case-id}/
├── patent/          disclosure.docx + {case}.docx + briefing.pptx
├── software-copyright/  manual.docx + source_code.docx
└── disclosure/      disclosure.docx
```

Each path also retains Markdown intermediates. Self-check report: `{case}_selfcheck.md`.

**Prohibitions**: No skill name/repo path/disclaimers in deliverables. No self-check section in body. No fabricated patent numbers/links. No "approximately" in claims. No commercial terms in abstract.

## Knowledge Index

| Reference File | Contents |
|---------------|----------|
| `references/ai-patent-special.md` | §1 Patentability + 8 domain risks §2 Layout (incl 3D/embodied) §3 6-type + 10 domain mapping §4 13-type figures §5 6+14+4 desensitization §6 6-group CPC §7 Quick reference |
| `references/ai-patent-claims-guide.md` | §1 Triple claim principle §2 11 claim templates §3 5-layer + 5 domain-dependent expansion |
| `references/ai-software-copyright-guide.md` | §1 11-type + 6 industry detection §2 12-level priority + desensitization §3 4 manual templates §4 10 pitfalls |
