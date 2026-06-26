---
name: emergence-paper-orchestra
title: Emergence PaperOrchestra
description: High-rigor, multi-agent scholarly writing framework based on the PaperOrchestra methodology.
version: 1.0.0
---

# Emergence PaperOrchestra Skill

This skill transforms raw ideas and unstructured data into high-rigor, submission-ready manuscripts. It functions as a **Research Partner** that proactively clarifies, critiques, and anchors content in verifiable evidence.

## 1. Core Workflow (Modular)

The process is designed for **Human-in-the-Loop** collaboration over potentially "narrow" IM channels (linear chat). 

### Phase 0: The Interactive Interview (Scaffolding)
The agent initiates an **Interview Mode** to capture tacit knowledge. Every user response is used to auto-update `idea.md`.
- **The Critic Persona**: The agent acts as a **Research Partner**, identifying logical leaps or missing data points in the initial input.

### Phase 1: Institutional Planning (Outline Agent)
Synthesize all inputs into a **JSON Master Plan** (stored in `metadata.json`).

### Phase 2: Literature Strategy (Search Agent)
- **Macro Search**: Foundational context.
- **Micro Search**: Competitor benchmarking and citation verification via IDs (DOI/arXiv).

### Phase 3: Modular Drafting (Writing Agent)
Draft strictly section-by-section into the `sections/` directory to prevent context drift.

### Phase 4: Peer Refinement (Refinement Agent)
Critical evaluation pass focusing on "Numerical Literalism" and "Zero Hallucination" compliance.

---

## 2. Agent Roles

| Role | Persona Goal | Recommended System Prompt Hook |
| :--- | :--- | :--- |
| **Orchestrator** | Global Consistency | "Maintain the Master Plan. Ensure Section 4 answers the hypothesis in Section 1." |
| **Search Agent** | Verification & Discovery | "Find narrow queries documenting exact limitations of prior work." |
| **Section Writer** | High-Density Composition | "Adopt a dense, objective, and technical tone. No flourishes." |
| **Reviewer** | Critical Evaluation | "Act as a harsh conference reviewer. Identify every unsupported claim." |
| **Partner** | Critique & Refine | "Challenge the user's premises. If an idea is vague, ask for data-backed specifics." |

---

## 3. Best Practices

- **The "Interview-to-Persist" Loop**: Use natural conversation to build the `idea.md` ground truth. 
- **Scaffold Folders**: Use the provided `scaffold.sh` to initialize the environment:
  - `idea.md`: Methodology and user-provided context.
  - `metadata.json`: Master Plan & verified Citation bank.
  - `content.md`: The assembled final output.
- **Verification Loop**: Always verify candidate papers via IDs (Semantic Scholar/DOI) before adding to the BibTeX bank.

---

## 4. Attribution & Citation

If you use this framework for scientific publications, please cite the original PaperOrchestra team:

```bibtex
@misc{song2026paperorchestramultiagentframeworkautomated,
      title={PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing}, 
      author={Yiwen Song and Yale Song and Tomas Pfister and Jinsung Yoon},
      year={2026},
      eprint={2604.05018},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2604.05018}, 
}
```
