## Description:

Organizes multiple AI roles into a virtual team for role configuration, task assignment, progress tracking, and work reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gdp6539](https://clawhub.ai/user/gdp6539)

### License/Terms of Use:

MIT

## Use Case:

Developers, solo operators, and small teams use this skill to coordinate AI employee roles, persist their working memory, assign tasks, check team status, and generate reports for lightweight automated operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file handling can escape intended folders or copy local files.

Mitigation: Run the skill only in an isolated workspace and treat role, employee, and template inputs as trusted until path validation is fixed.

Risk: The skill writes persistent employee state and memory files.

Mitigation: Review generated files before reuse and avoid running it where the Node process can access sensitive workspace data.

## Reference(s):

- [AI Employee Team on ClawHub](https://clawhub.ai/gdp6539/skills/ai-employee-team)
- [Publisher profile: gdp6539](https://clawhub.ai/user/gdp6539)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, slash-command references, and Node.js CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local configuration, employee state, and memory files when its Node.js manager is run.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
