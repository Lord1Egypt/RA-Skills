## Description:

Extracts Douyin video context, original descriptions, and spoken transcripts from a video link, share text, or aweme ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users can provide a Douyin video link, share text, or aweme ID to retrieve video context, the original description, and a spoken transcript. The skill presents transcript content in structured, copyable, and concise forms, and can continue checking an existing transcript job.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious because its CLI commands use a mutable latest package, and the partial scan could not resolve several references.

Mitigation: Wait for a reviewed fixed CLI release and understand its credential access before installation; review the unresolved references.

## Reference(s):

- [抖音文案提取 on ClawHub](https://clawhub.ai/devinchen2014/skills/douyin-video-copy-extract)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Structured transcript results and Markdown guidance; direct CLI results are formatted as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript jobs may be asynchronous and should be continued with the same job ID. SRT export is available through the CLI when valid time segments are returned.]

## Skill Version(s):

0.1.14 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
