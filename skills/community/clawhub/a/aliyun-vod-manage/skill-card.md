## Description:

Use when managing Alibaba Cloud ApsaraVideo VOD resources and media workflows via OpenAPI/SDK, including upload and media asset operations, transcoding templates, playback authorization, AI processing jobs, and VOD troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Alibaba Cloud ApsaraVideo VOD media assets, upload workflows, playback authorization, transcoding templates, AI jobs, and troubleshooting through OpenAPI or SDK-based workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact Alibaba Cloud VOD operations using cloud credentials.

Mitigation: Use least-privilege RAM or STS credentials scoped to the exact VOD task and media resources.

Risk: Destructive operations such as DeleteVideo can remove media assets.

Mitigation: Require explicit confirmation before DeleteVideo or any other destructive change.

Risk: Saved evidence can contain upload authorization, playback authorization, signed URLs, tokens, or sensitive media identifiers.

Mitigation: Redact or delete sensitive evidence before sharing or retaining output files.

## Reference(s):

- [Alibaba Cloud Media VOD skill page](https://clawhub.ai/cinience/skills/aliyun-vod-manage)
- [cinience publisher profile](https://clawhub.ai/user/cinience)
- [OpenAPI product page](https://api.aliyun.com/product/vod)
- [VOD API metadata](https://api.aliyun.com/meta/v1/products/vod/versions/2017-03-21/api-docs.json)
- [ApsaraVideo VOD documentation](https://www.alibabacloud.com/help/en/vod)
- [Source list](references/sources.md)
- [VOD task templates](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API names, configuration steps, and generated JSON or Markdown evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated API inventory and operation evidence are directed to output/aliyun-vod-manage/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
