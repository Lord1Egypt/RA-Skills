## Description: <br>
Methodical end-to-end software delivery orchestrator for Codex CLI with dual project modes (greenfield for new builds, brownfield for existing systems) and dual execution modes (autonomous and gated). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShalomObongo](https://clawhub.ai/user/ShalomObongo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to run disciplined software delivery with specs, stage gates, validation evidence, documentation updates, and controlled delegation to coding-agent CLIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scaffold project documentation, update workflow files, run validation commands, and delegate tasks to coding-agent CLIs. <br>
Mitigation: Install it only in trusted workspaces and review generated prompts, commands, and planned file changes before execution. <br>
Risk: Autonomous execution can make unintended code or documentation changes costly in sensitive repositories. <br>
Mitigation: Use gated mode for unfamiliar or sensitive projects and require user approval at each gate. <br>
Risk: User-supplied validation commands may perform actions beyond simple checks. <br>
Mitigation: Inspect validation commands before running them and prefer least-privilege environments for project verification. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ShalomObongo/codex-conductor) <br>
- [Spec-Driven Development](references/spec-driven-development.md) <br>
- [Planning Questionnaire](references/planning-questionnaire.md) <br>
- [Modes](references/modes.md) <br>
- [Gate Checklists](references/gate-checklists.md) <br>
- [Testing Matrix](references/testing-matrix.md) <br>
- [Manual Test Templates](references/manual-test-templates.md) <br>
- [Coding-Agent Runbook](references/codex-runbook.md) <br>
- [Gate Prompt Templates](references/gate-prompts.md) <br>
- [Research Playbook](references/research-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown with inline shell commands, generated project files, and JSON status artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates project documentation, workflow files, and orchestrator state when used in a target workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
