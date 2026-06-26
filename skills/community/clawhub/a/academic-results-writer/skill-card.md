## Description: <br>
Academic Results Writer helps agents write, revise, and audit academic Results sections from statistics, figures, tables, captions, drafts, target-paper structure, and Module H writer transfer packets, with Chinese as the default output language and optional English or journal-specific style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin77-chris](https://clawhub.ai/user/bin77-chris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and academic writing agents use this skill to draft, revise, and audit Results sections for psychology and behavioral science papers while preserving statistical accuracy, source boundaries, and Results-versus-Discussion separation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long generated Results drafts may be saved automatically to a local Desktop output folder. <br>
Mitigation: Avoid providing confidential or unpublished research data unless local file creation is acceptable, and check generated filenames for collisions before re-running similar analyses. <br>
Risk: Academic Results prose can become misleading if the agent fabricates statistics, overstates causality, or mixes target-paper content with user data. <br>
Mitigation: Use the skill's audit sections, source ledger, and statistical guardrails to verify that all values come from the current user input and that target papers contribute structure only. <br>


## Reference(s): <br>
- [Academic Results Writer on ClawHub](https://clawhub.ai/bin77-chris/academic-results-writer) <br>
- [README](artifact/README.md) <br>
- [Statistical Templates](artifact/docs/statistical-templates.md) <br>
- [Quality Checklist](artifact/docs/quality-checklist.md) <br>
- [Target Paper Adaptation](artifact/docs/target-paper-adaptation.md) <br>
- [Module H Bridge Workflow](artifact/docs/module-h-bridge.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Files] <br>
**Output Format:** [Chinese or English Markdown with structured Results drafts, audit notes, checklists, and optional local Markdown file output for long responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is Chinese and standard-depth; long outputs may be written to ~/Desktop/OpenClaw_Paper_Analysis/outputs_md/results_writer/.] <br>

## Skill Version(s): <br>
1.2.1 (source: SKILL.md frontmatter, README, CHANGELOG, evidence.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
