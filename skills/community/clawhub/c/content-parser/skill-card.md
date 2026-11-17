## Description:

Extracts and parses content from URLs into normalized text, metadata, and references for review or downstream skill workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xfango](https://clawhub.ai/user/0xfango)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and external users use this skill to extract readable content from supported public HTTP(S) URLs before summarization, content generation, or standalone analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided URLs to the Marswave/ListenHub API, including any information embedded in private or signed links.

Mitigation: Use only public URLs intended for external API processing, and avoid private, sensitive, signed, or access-token-bearing links.

Risk: Extracted content and raw API responses may be saved locally when autoDownload is enabled.

Mitigation: Confirm the output directory before extraction, disable autoDownload when persistence is not needed, and remove generated .md and .json files that should not remain on disk.

Risk: Shell command examples that substitute crafted URL values can execute unintended local commands if handled unsafely.

Mitigation: Validate that URLs are HTTP(S), quote or encode user-supplied values, and review generated shell commands before execution.

## Reference(s):

- [Supported Platforms](artifact/references/supported-platforms.md)
- [ClawHub Skill Page](https://clawhub.ai/0xfango/skills/content-parser)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown previews, JSON API responses, shell commands, and optional local .md/.json files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LISTENHUB_API_KEY; optional autoDownload saves extracted Markdown and raw JSON responses to the current directory.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
