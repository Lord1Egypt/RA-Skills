## Description:

Campaign is a command-line tool for campaign and content tasks, including drafting, editing, optimization, scheduling, search, status checks, and local export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to manage campaign and content notes from the terminal, review recent activity, search saved entries, and export local logs for automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Campaign/content text may be stored in plaintext under ~/.local/share/campaign and exported locally.

Mitigation: Do not use the skill for confidential customer, account, strategy, credential, or regulated data unless plaintext local storage and export behavior are acceptable.

Risk: The description and command documentation understate persistent storage, search, and export behavior.

Mitigation: Review the script behavior before installation and make users aware of local storage, search, and export paths.

## Reference(s):

- [Campaign ClawHub listing](https://clawhub.ai/xueyetianya/skills/campaign)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save, search, summarize, and export plaintext campaign/content log entries under ~/.local/share/campaign.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
