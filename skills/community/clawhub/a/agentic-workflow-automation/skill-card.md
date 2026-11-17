## Description:

Generate reusable multi-step agent workflow blueprints for trigger/action orchestration, deterministic workflow definitions, and automation handoff artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x-professor](https://clawhub.ai/user/0x-professor)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to define reusable workflow blueprints with triggers, ordered steps, dependencies, and fallback behavior for handoff to tools such as n8n or internal orchestrators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dry-run option should not be relied on to prevent filesystem changes.

Mitigation: Use temporary, non-sensitive output paths when testing and verify generated files before moving them into a project.

Risk: User-supplied output paths could write to unintended or sensitive locations.

Mitigation: Choose explicit output paths in safe working directories and avoid overwriting existing sensitive files.

Risk: CSV output from untrusted input can be unsafe to open directly in spreadsheet software.

Mitigation: Review or sanitize generated CSV fields before opening or sharing CSV files derived from external input.

## Reference(s):

- [Workflow Blueprint Guide](artifact/references/workflow-blueprint-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/0x-professor/skills/agentic-workflow-automation)
- [Publisher Profile](https://clawhub.ai/user/0x-professor)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [JSON, Markdown, or CSV workflow blueprint artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normalizes workflow name, trigger, ordered steps, step type, and fallback behavior; JSON input is capped at 1 MiB.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
