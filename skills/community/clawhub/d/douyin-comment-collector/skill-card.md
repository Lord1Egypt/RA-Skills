## Description:

Collects Douyin video comments and account homepage posts, including comment export, optional word-frequency analysis, post title and publish-time capture, local time-window filtering, and daily post distribution summaries for data the user is authorized to access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onebysuzhong-dot](https://clawhub.ai/user/onebysuzhong-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators use this skill to gather Douyin comments or account-post metadata for authorized monitoring, topic research, review, and lightweight text analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reuses live Douyin account cookies.

Mitigation: Use only authorized accounts, treat cookie files as full account credentials, delete them when finished, and never commit or share them.

Risk: Browser and cookie modes include platform-bypass behavior that may be inappropriate for some use cases.

Mitigation: Review whether the collection method is allowed for the intended workflow before running browser or authenticated modes.

Risk: The authenticated HTTP path disables TLS verification.

Mitigation: Run the skill only in an isolated environment and avoid untrusted networks.

## Reference(s):

- [Douyin API and signing notes](references/api.md)
- [Release page](https://clawhub.ai/onebysuzhong-dot/skills/douyin-comment-collector)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated skill runs can produce JSON or CSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include comment records, post metadata, optional word-frequency analysis, and daily post distribution summaries.]

## Skill Version(s):

1.4.0 (source: frontmatter, changelog, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
