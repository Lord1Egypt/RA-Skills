## Description:

用已发布的零售品牌门店快照，帮助零售连锁团队分析门店网络、业态分类、区域覆盖、周边画像、品牌对比与坐标选址。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

Retail market, expansion, and channel teams use this skill to query published retail brand snapshots and compare store footprint, category mix, regional coverage, surroundings, competitors, and candidate locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A retail-data API key could be exposed through chats, logs, repositories, or shared command history.

Mitigation: Keep DDT_API_KEY out of chats, logs, and repositories; configure it only in a local or controlled runtime.

Risk: An untrusted API endpoint could receive authenticated requests.

Mitigation: Set or verify DDT_OPEN_BASE as the official trusted endpoint before making calls with an API key.

Risk: Snapshot, coverage-limited, or truncated API results could be mistaken for a complete current market view.

Mitigation: Report coverage, data version, and preview truncation; avoid inferring missing values, monthly changes, or business outcomes that are not present in API responses.

## Reference(s):

- [店店通 retail network homepage](https://gotoshop-ai.com/ddtclaw/)
- [ClawHub skill listing](https://clawhub.ai/horacetu/skills/ddtclaw-retail-network)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with concise conclusions, key metrics, coverage notes, and occasional curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses API response data only; omits API keys, internal identifiers, supplier data, and unsupported fields.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
