## Description:

Financial market data and bot-native market intelligence API for stock market context, consensus, feeds, observations, signals, sources, and knowledge.

This skill is for research and development only.

## Publisher:

[erik-miller](https://clawhub.ai/user/erik-miller)

### License/Terms of Use:


## Use Case:

Developers and agent users use ClawFi to retrieve ticker context, consensus, and market feeds, and to submit observations, signals, sources, or structured knowledge when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installer uses a mutable npm latest package to modify multiple agent skill directories.

Mitigation: Review the installer before running it, or use a pinned, reviewed package version or manual copy of the reviewed skill file into the intended agent directory.

Risk: The service may receive proprietary trading research, private account data, or sensitive source material.

Mitigation: Do not submit sensitive market research, account data, or source material until the service operator, retention policy, and deployment origin have been verified.

## Reference(s):

- [ClawFi ClawHub release page](https://clawhub.ai/erik-miller/skills/claw-fi)
- [ClawFi README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with API endpoint descriptions and JSON request/response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API read/write guidance, required headers, and explicit approval expectations for write endpoints.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
