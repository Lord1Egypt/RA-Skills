## Description:

AideNote Skill helps an agent query, search, summarize, and inspect SlonAide/AiDeNote recording notes, with optional setup for an OpenClaw remote bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajingmiao](https://clawhub.ai/user/ajingmiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw users use this skill to retrieve recording-note lists, inspect note details, view AI summaries, search note content, and check API connectivity. Users may also use it to install or inspect a local AiDeNote bridge that lets the mobile app connect to OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote bridge setup can download and run installer code, pass the AideNote API key into that process, and create login persistence.

Mitigation: Review the installer source and URLs before running setup, avoid environments with unrelated secrets, and prefer releases that verify installer hashes or signatures and document uninstall steps.

Risk: The AideNote API key may be exposed through installer behavior, process environments, or logs.

Mitigation: Use a scoped key where possible, keep logs private, and rotate the key if it may have been exposed.

Risk: Recording notes and transcripts can contain private or sensitive user information.

Mitigation: Use the skill only in trusted agent sessions, avoid sharing full transcripts unnecessarily, and review outputs before sending them into shared channels.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ajingmiao/skills/aidenote)
- [AiDeNote web app](https://h5.aidenote.cn/)
- [SlonAide web app](https://h5.slonaide.cn/)
- [AideNote API base URL](https://api.aidenote.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text responses with command snippets, status messages, and structured note summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Long transcripts may be truncated in responses, and API keys are masked in diagnostic output.]

## Skill Version(s):

1.0.10 (source: ClawHub release evidence; artifact frontmatter and package metadata report 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
