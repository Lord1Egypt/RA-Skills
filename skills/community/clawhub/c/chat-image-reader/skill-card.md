## Description:

Reads and analyzes images from messages across 10+ chat platforms using platform-specific APIs and unified image processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zqy15306762317](https://clawhub.ai/user/zqy15306762317)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve image attachments from configured chat platforms, save them locally, and pass them to an image analysis tool for OCR, screenshot, chart, or general image interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader has broad network access across configured chat and media endpoints.

Mitigation: Install only when the configured chat platforms are trusted, and restrict bot or app credentials to the least privileges needed for image retrieval.

Risk: Downloaded images are written to local paths and may contain sensitive chat content.

Mitigation: Use a private temporary directory, limit file permissions, and clean downloaded images after analysis.

Risk: Direct URL downloads can retrieve untrusted or unexpected content.

Mitigation: Avoid passing arbitrary URLs from untrusted users and review URL sources before download.

Risk: Passing API tokens on command lines can expose credentials through shell history or process listings.

Mitigation: Prefer environment variables or secret-managed configuration for tokens and rotate credentials if exposed.

## Reference(s):

- [Chat Platform Image API Reference](references/platform-api.md)
- [ClawHub skill page](https://clawhub.ai/zqy15306762317/skills/chat-image-reader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, API call patterns, and local file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download images to local temporary files and then emit the file path for downstream analysis.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
