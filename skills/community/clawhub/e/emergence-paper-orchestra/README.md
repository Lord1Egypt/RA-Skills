# Emergence PaperOrchestra Skill

A high-rigor, multi-agent scholarly writing framework for the Agent Economy. Developed by **Emergence Science**, this skill implements the **PaperOrchestra** (arXiv:2604.05018v1) methodology for autonomous manuscript generation and professional authoring.

## Overview

Unlike standard LLM drafting, **Emergence PaperOrchestra** acts as a **Research Partner**. It decomposes the writing process into specialized roles—Orchestrator, Search Agent, Section Writer, and Reviewer—to ensure:
- **Zero Hallucination**: Strict "Numerical Literalism" and "Data-Chaining."
- **Institutional Rigor**: Semantic Scholar/DOI verified citation banks.
- **Agent-DX**: Optimized for modular parsing and long-term project persistence.

## Key Features

- **Multi-Round Interview**: Captures human tacit knowledge via conversational scaffolding.
- **Modular Drafting**: Section-by-section construction to maintain high semantic density.
- **Portable Scaffolding**: Shell scripts provided for environment initialization on any Ubuntu/macOS VM.

## Usage

Initialize a new project using the provided scaffold:
```bash
./scripts/scaffold.sh "My Research Project"
```

Then, invoke your agent with the **PaperOrchestra Protocol** to begin the Phase 0 Interview.

## Attribution

This framework is an implementation of the PaperOrchestra methodology. If you use it for academic purposes, please cite:

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

---
© 2026 Emergence Science. Built for the future of autonomous scholarly discovery.
