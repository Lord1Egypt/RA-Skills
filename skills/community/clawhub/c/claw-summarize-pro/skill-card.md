## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamwang-wh](https://clawhub.ai/user/williamwang-wh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to have an agent run or configure the summarize CLI for concise summaries of web URLs, local files, PDFs, images, audio, and YouTube links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party Homebrew tap and summarize CLI that are not pinned in the release evidence.

Mitigation: Install only from trusted sources and review the upstream CLI or tap before use when supply-chain assurance matters.

Risk: Summarizing local files or protected content can expose sensitive information to configured model or extraction providers.

Mitigation: Use narrowly scoped API keys and avoid processing highly sensitive files unless the provider and data handling path are acceptable.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/williamwang-wh/skills/claw-summarize-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include model, summary length, token limit, extraction, and fallback service settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
