## Description:

Helps agents manage Alibaba Cloud ApsaraVideo Live resources and workflows via OpenAPI/SDK, including live domain configuration, stream ingest and playback setup, recording and transcoding templates, monitoring queries, and live stream operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to plan and perform Alibaba Cloud ApsaraVideo Live management tasks, including domain setup, stream operations, recording/transcoding configuration, monitoring queries, and OpenAPI metadata discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user may authorize changes to the wrong Alibaba Cloud Live region, domain, app, or stream.

Mitigation: Confirm the exact region, domain, app, stream, and desired operation before mutations; use read-only Describe/List APIs first and keep a rollback plan.

Risk: Saved evidence files may contain credentials, Authorization data, signatures, tokens, signed URLs, or sensitive identifiers.

Mitigation: Use least-privilege STS/RAM credentials and redact sensitive values before saving request payloads, responses, or execution notes under output/aliyun-live-manage/.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/aliyun-live-manage)
- [Source List](references/sources.md)
- [Task Templates](references/templates.md)
- [Alibaba Cloud OpenAPI Product Page](https://api.aliyun.com/product/live)
- [ApsaraVideo Live API Metadata](https://api.aliyun.com/meta/v1/products/live/versions/2016-11-01/api-docs.json)
- [ApsaraVideo Live API Definition Template](https://api.aliyun.com/meta/v1/products/live/versions/2016-11-01/apis/{ApiName}/api.json)
- [Alibaba Cloud ApsaraVideo Live Documentation](https://www.alibabacloud.com/help/en/live)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated JSON or Markdown evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated API inventory and execution evidence are expected under output/aliyun-live-manage/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
