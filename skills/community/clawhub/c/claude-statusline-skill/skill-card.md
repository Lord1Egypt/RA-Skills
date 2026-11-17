## Description:

Adds a Claude Code status line that displays the current Git branch, model, and changed-line count, with placeholders for context usage, output tokens, cost, and duration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mark-heartflow](https://clawhub.ai/user/mark-heartflow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code can configure this skill's local status-line command to show basic session and repository status while they work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation requires editing Claude Code settings to run a persistent local status-line shell script.

Mitigation: Review the settings change and script contents before enabling the command, and keep the script in a trusted local path.

Risk: Context usage, output token, cost, and duration fields are placeholders in the provided script.

Mitigation: Treat those fields as unavailable unless the script is extended and tested for the user's Claude Code environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and Bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local setup instructions and an example status-line shell script; several displayed metrics remain placeholders unless extended.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
