## Description:

Summarize URLs or files with the summarize CLI, including web pages, PDFs, images, audio, and YouTube links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other ClawHub users use this skill to ask an agent to summarize local files, URLs, and YouTube links through the summarize CLI. It is useful when an agent needs concise summaries or machine-readable summary output from supported document and media inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local files, URLs, and media inputs may be sent to selected model providers or enabled fallback services.

Mitigation: Avoid summarizing secrets, confidential documents, private URLs, or regulated data unless that processing has been approved.

Risk: The summarize CLI is installed from an unpinned third-party Homebrew tap.

Mitigation: Review and trust the Homebrew tap and CLI before installation, and pin or audit the dependency in managed environments.

Risk: Optional Firecrawl and Apify fallbacks can introduce additional external processing paths.

Mitigation: Enable fallback service API keys only when their data handling is acceptable for the content being summarized.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/0514-tosr2-skill)
- [Publisher profile](https://clawhub.ai/user/yinwuzhe)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output length can be controlled with CLI flags such as --length and --max-output-tokens.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
