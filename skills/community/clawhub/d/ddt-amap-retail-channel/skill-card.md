## Description:

使用高德地图地址文本和店店通已发布门店快照，帮助市场与渠道分析人员评估零售品牌的业态结构、城市覆盖、竞品差异与市场机会。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

Market and channel analysts use this skill to turn AMap-copied place names and address text into retail brand, regional coverage, channel mix, competitor comparison, and candidate-site analysis grounded in published DDT store snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes credentialed network calls to the DDT retail API.

Mitigation: Keep DDT_API_KEY out of chats, logs, and repositories, and stop on authentication failures instead of exposing or retrying with the key.

Risk: A custom API base URL could send authenticated requests to an untrusted endpoint.

Mitigation: Set DDT_OPEN_BASE explicitly to the trusted DDT endpoint before making authenticated requests.

Risk: Retail conclusions can be misleading if the brand is unpublished, coverage is incomplete, or previews are truncated.

Mitigation: Use only API-returned metrics, disclose uncovered fields, narrow truncated previews, and stop rather than substituting approximate brands or missing data.

Risk: Users may confuse address input support with an official AMap relationship.

Mitigation: Preserve the disclosure that this is not an official AMap product and that store conclusions come from DDT's published snapshots.

## Reference(s):

- [DDT Claw homepage](https://gotoshop-ai.com/ddtclaw/)
- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-amap-retail-channel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise analytical summaries and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses disclosed authenticated DDT retail API calls; outputs should avoid API keys, internal identifiers, supplier fields, and unsupported metrics.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
