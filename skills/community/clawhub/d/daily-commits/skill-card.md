## Description:

Summarize a person's git commits for a specific date, grouped by feature points, in English. Use when reviewing daily work output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrew020](https://clawhub.ai/user/andrew020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering leads use this skill to review a person's daily git activity for a specific date, grouped by feature or functional area with concise English descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided dates and author names are placed into git command templates, which can create command-injection risk if an agent embeds them directly into shell command text.

Mitigation: Validate the date format, reject control characters in author names, and pass user inputs to git without composing unsafe shell command strings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andrew020/skills/daily-commits)
- [Publisher profile](https://clawhub.ai/user/andrew020)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary with git command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [English-only summary grouped by feature area with total commit count.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
