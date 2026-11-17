## Description:

Run Twitter/X research, monitoring, watchlists, and OAuth-gated posting through AIsa for trend tracking, competitor monitoring, and publish-ready workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to research Twitter/X accounts and conversations, monitor trends or watchlists, and prepare approved posting workflows through AIsa.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AIsa API key can appear in local command logs or command output.

Mitigation: Use only an AIsa key acceptable for local exposure, avoid saving command output to shared logs, and rotate the key if it has already appeared in agent or CI output.

Risk: Posting is a public Twitter/X account action mediated by the AIsa relay.

Mitigation: Require explicit user approval before posting and do not claim publication succeeded until the API confirms it.

Risk: Caller-selected local image or video files can be uploaded to the relay.

Mitigation: Upload only files the user explicitly attached or approved, avoid sensitive local files, and confirm paths and media types before submission.

## Reference(s):

- [AIsa Twitter OAuth reference](references/post_twitter.md)
- [AIsa homepage](https://aisa.one)
- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/aisa-twitter-api-command-center)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; Twitter/X read, OAuth, posting, and approved media upload actions are routed through AIsa.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
