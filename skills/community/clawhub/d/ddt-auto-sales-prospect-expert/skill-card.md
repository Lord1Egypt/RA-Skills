## Description:

汽服门店销售攻店专家，结合品牌网络、门店服务类型、位置画像和周边竞对筛选拜访线索。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External automotive aftermarket sales representatives, regional managers, and channel development teams use this skill to identify target service shops, compare brand coverage, review local competition, and prepare store visits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys could be sent to an unintended endpoint if DDT_OPEN_BASE is changed to an untrusted origin.

Mitigation: Use the documented default endpoint or a trusted approved origin only, keep DDT_API_KEY out of chats, logs, and repositories, and rotate the key after any suspected exposure.

Risk: Store and market conclusions can be misleading if API coverage is incomplete, truncated, or unavailable.

Mitigation: Use only returned API fields, report uncovered data as unavailable, respect preview limits, and avoid treating limited previews as full market lists or outcome predictions.

## Reference(s):

- [DDT Claw homepage](https://gotoshop-ai.com/ddtclaw/)
- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-auto-sales-prospect-expert)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise recommendations, key metrics, coverage notes, limited store previews, and occasional curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DDT_API_KEY; uses bounded previews and must not expose API keys, storage IDs, supplier fields, or unsupported metrics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
