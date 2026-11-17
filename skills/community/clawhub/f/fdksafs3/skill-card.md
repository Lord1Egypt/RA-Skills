## Description:

Guides agents to use the GitHub CLI (`gh`) for issues, pull requests, CI workflow runs, API queries, and JSON-filtered output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yequanzheng](https://clawhub.ai/user/yequanzheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect GitHub pull requests, issues, workflow runs, logs, and API responses with the GitHub CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub CLI guidance may cause an agent to act with the user's authenticated GitHub permissions.

Mitigation: Review proposed `gh` commands before execution and use least-privilege GitHub authentication for the repositories involved.

Risk: Malformed or low-quality metadata can make the skill's purpose unclear before installation.

Mitigation: Review the skill name, description, and release metadata before publishing or installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yequanzheng/skills/fdksafs3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub CLI commands that use the user's authenticated gh session.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
