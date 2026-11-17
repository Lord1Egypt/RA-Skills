## Description:

Manage Comment data right from your terminal. Use when you need comment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and command-line users use Comment to record, search, inspect, and export local comment-related entries from a terminal workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local CLI persistently saves arbitrary text and activity logs under ~/.local/share/comment without clear retention or deletion controls.

Mitigation: Do not enter secrets, tokens, private notes, or sensitive business data unless local retention is intended; review or remove ~/.local/share/comment when needed.

## Reference(s):

- [Comment on ClawHub](https://clawhub.ai/bytesagain3/skills/comment)
- [BytesAgain Homepage](https://bytesagain.com)
- [BytesAgain Feedback](https://bytesagain.com/feedback/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and local CLI text output; exports may be JSON, CSV, or plain text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores entries and activity logs under ~/.local/share/comment.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
