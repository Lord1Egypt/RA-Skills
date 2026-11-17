## Description:

Assist-skills helps teams deploy a LINLAN AI development assistant reference package into projects, adding project-level agent guidance, tool rules, standardized development templates, and workflow prompts for Trae, CodeBuddy, Claude Code, and opencode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linlannet](https://clawhub.ai/user/linlannet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to set up AI-assisted development workflows in an existing project, including deployment of reference files, project rules, requirements/design/test/review templates, and quick command workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment can add persistent project instruction files and tool rules that affect future agent behavior.

Mitigation: Review the files to be added, run a dry run first, and inspect AGENTS.md, CLAUDE.md, .trae, and .codebuddy changes before using the installed rules.

Risk: A Windows vendoring option can write outside the selected project when unsafe custom VendorDir values are used.

Mitigation: Use an explicit target directory and the default relative VendorDir; avoid parent-directory segments or absolute paths.

Risk: Broad deployment prompts can trigger project setup actions before the target directory and overwrite intent are clear.

Mitigation: Confirm the target directory before execution and use Force only when overwriting existing files is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linlannet/skills/assist-skills)
- [README.en.md](README.en.md)
- [VERSION.md](VERSION.md)
- [AI pilot reference package guide](ai-pilot/README.md)
- [Quick commands reference](ai-pilot/reference/quick-commands.md)
- [Evaluation metrics definitions](ai-pilot/reference/metrics-definition.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and project file/configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May add persistent project instruction files and tool rules when deployment scripts are run; supports dry-run and skip-rules options.]

## Skill Version(s):

1.0.2 (source: server release metadata and target metadata; VERSION.md reports v1.0.2-linlan)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
