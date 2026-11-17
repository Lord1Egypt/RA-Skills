## Description:

Agent-Skill-Reviewer reviews AgentSkill quality, structure, documentation clarity, redundancy, and token efficiency, then generates a professional Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ming-shy](https://clawhub.ai/user/ming-shy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit AgentSkill files for clarity, token efficiency, structure, completeness, and logic preservation. It supports structured Markdown review reports and optional helper-script checks for token counts and workflow alignment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the user-selected skill directory and can write Markdown reports into the working directory by default.

Mitigation: Confirm the target path and output path before use, especially in repositories where generated files should be controlled.

Risk: Review suggestions could remove or weaken important skill behavior if accepted without checking logic preservation.

Mitigation: Use the bundled logic validation workflow and manually review proposed changes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ming-shy/skills/agentskill-reviewer)
- [Logic validation guide](references/validation.md)
- [Review report template](references/report_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default report output is Chinese Markdown in a skill-reviews directory unless the user specifies another path.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
