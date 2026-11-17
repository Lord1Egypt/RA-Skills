## Description:

给一份财报或公告，把其他综合收益的披露读成每条都能回到原句的登记表：概况、税后净额明细（税前／所得税影响／税后净额三数）、重分类调整、归属于母公司与少数股东、现金流量套期与折算差额。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial analysts can use this skill to turn Chinese company reports or announcements into a source-linked register of other comprehensive income disclosures. It preserves the reported figures and quotations for human review rather than recalculating amounts or making investment judgments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports an unvalidated destination for a request carrying an API key.

Mitigation: Confirm the destination is the intended trusted service before supplying CUE_API_KEY; omit the key if the destination cannot be verified.

Risk: Attachments may be parsed by an external service.

Mitigation: Do not submit confidential reports or attachments unless the service is approved for that data.

Risk: The review reports a checker validation bypass and a local usage marker.

Mitigation: Treat checker results as one review aid, inspect the generated register against the source documents, and review unexpected local file changes.

Risk: The security assessment has partial coverage, and static analysis of the fixture shell script was degraded.

Mitigation: Review and scan all release files, including the fixture shell script, before deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-cn-other-comprehensive-income-cn)
- [Cue MCP data channel](https://cuecue.cn/hub/mcp)
- [Cue Omni Reader](https://cuecue.cn/hub/omni-reader)
- [Cue API key setup](https://cuecue.cn/hub/api-key)
- [Live MCP catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Chinese Markdown register with source quotations, anchors, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fixed seven-section structure; missing disclosure items are explicitly listed; no recalculation or investment recommendations.]

## Skill Version(s):

0.1.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
