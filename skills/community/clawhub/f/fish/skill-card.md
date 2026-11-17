## Description:

Fish is a local terminal utility for recording, searching, and exporting activity logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and terminal users can use Fish to inspect local command activity, view simple statistics, search retained entries, and export logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command inputs and activity can be retained locally under ~/.local/share/fish, including secrets or sensitive filenames if a user enters them.

Mitigation: Install only when local command logging is intended, avoid entering secrets or sensitive data, and inspect or delete ~/.local/share/fish when retained data should be cleared.

Risk: The security review labels Fish as suspicious because its utility framing is vague and some command behavior may be misleading.

Mitigation: Review the installed shell behavior before deployment and limit use to environments where local logging and export behavior are acceptable.

## Reference(s):

- [Fish ClawHub listing](https://clawhub.ai/bytesagain1/skills/fish)
- [BytesAgain homepage](https://bytesagain.com)
- [BytesAgain feedback](https://bytesagain.com/feedback/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Terminal text with local log and export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores timestamped logs under ~/.local/share/fish and can export JSON, CSV, or plain text.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
