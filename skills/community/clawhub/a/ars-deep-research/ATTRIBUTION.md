# Attribution Notice

These skills (deep-research, academic-paper, academic-paper-reviewer, academic-pipeline) are **adaptations** of the [Academic Research Skills (ARS) suite](https://github.com/Imbad0202/academic-research-skills).

## Original Work

- **Creator:** Cheng-I Wu (吳政億)
- **Repository:** https://github.com/Imbad0202/academic-research-skills
- **License:** [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/)
- **Copyright:** Copyright (c) 2026 Cheng-I Wu

## Adaptation Details

- **Adapter:** Hermes Agent Skill Adaptation
- **Scope:** Replaced Claude Code's internal multi-agent system with Hermes Agent's native `delegate_task` orchestration mechanism
- **Preserved:** All 108+ knowledge files (agent definitions, references, templates, shared cross-skill documents) are preserved **verbatim** from the original
- **What changed:** The orchestration layer — how agents are invoked, sequenced, and checked — adapted from Claude Code slash-command / internal-agent model to Hermes `delegate_task` pattern

## License of This Adaptation

This adaptation is distributed under the **same CC BY-NC 4.0 license** as the original work. You are free to:

- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

Under the following terms:

- **Attribution** — You must give appropriate credit to Cheng-I Wu, provide a link to the license, and indicate if changes were made
- **NonCommercial** — You may not use the material for commercial purposes

**This adaptation is not endorsed by or affiliated with the original author.**

## Files

- `LICENSE` — Full CC BY-NC 4.0 license text
- Each `SKILL.md` — Contains attribution metadata and modification notice in frontmatter
