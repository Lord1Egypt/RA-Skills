## Description:

Summarize URLs or files with the summarize CLI for web pages, PDFs, images, audio, and YouTube content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to call the summarize CLI for concise summaries or extracted text from URLs, local documents, media, and YouTube links. It is useful when an agent needs summarized source material, machine-readable summary output, or configuration guidance for supported model providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party CLI installed from a Homebrew tap.

Mitigation: Install only from trusted sources and verify the tap, package, and binary before use.

Risk: Submitted URLs, files, media, or YouTube content may be sent to configured model or extraction providers.

Mitigation: Avoid sensitive or regulated content unless the provider configuration and data handling are approved for that use.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/apply-8138)
- [Publisher profile](https://clawhub.ai/user/yinwuzhe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON output when the summarize CLI is invoked with its machine-readable output option.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
