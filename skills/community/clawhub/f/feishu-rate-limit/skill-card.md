## Description:

Provides Feishu/Lark API rate limit handling guidance with smart interval control and 429 retry handling for batch operations, document writes, and bitable operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingsunrise](https://clawhub.ai/user/dingsunrise)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to pace Feishu/Lark API workflows, retry 429 responses, and plan batch, document, and bitable operations without exceeding service limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conservative pacing can slow Feishu/Lark workflows even when rate limits are not currently being hit.

Mitigation: Review interval, batch size, and retry settings against the workload before applying them broadly.

Risk: Local caching or rate-limit error logs may contain sensitive Feishu data.

Mitigation: Review cache and error-log contents, retention, and access controls before using the skill with sensitive Feishu data.

Risk: Broad activation wording may apply the guidance to Feishu API calls where extra pacing is unnecessary.

Mitigation: Use the skill when Feishu/Lark rate-limit handling is desired and review proposed workflow changes before execution.

## Reference(s):

- [Feishu API Limits Documentation](https://open.feishu.cn/document/platform-notices/platform-updates-/custom-app-api-call-limit)
- [OpenClaw Feishu Solution](https://xx0a.com/blog/openclaw-feishu)
- [Feishu Developer Community](https://open.feishu.cn/community)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with code blocks, tables, and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces pacing, batching, retry, caching, and troubleshooting guidance for Feishu/Lark API workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
