## Description:

Summarize URLs or files with the summarize CLI, including web pages, PDFs, images, audio, and YouTube links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to summarize URLs, local files, and YouTube links through the summarize CLI, with provider-specific API keys and optional extraction fallback services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Summarized local files, fetched URL content, or YouTube content may be sent to the selected model provider or fallback extraction service.

Mitigation: Review data sensitivity before summarizing, choose the intended provider deliberately, and configure only the API keys required for that provider or service.

Risk: The skill depends on installing and running the summarize CLI from a Homebrew tap.

Mitigation: Install only if the Homebrew tap and CLI provider are trusted, and verify the CLI source before use in sensitive environments.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/apply-8233)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; the summarize CLI may return plain text or machine-readable JSON summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports length and token limits, provider-specific API keys, and optional fallback extraction services.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
