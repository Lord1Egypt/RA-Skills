## Description:

店店通·汽车后市场门店网络分析使用已发布的汽车后市场门店快照，帮助市场、渠道、销售和拓展团队分析品牌网络、区域覆盖、周边画像、竞对和候选点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

Market, channel, sales, and expansion teams use this skill to turn published automotive aftermarket store snapshots into brand network, regional coverage, service-type, surroundings, competitor, and candidate-site analysis. It is limited to automotive aftermarket brands and should present API results as coverage-bound analysis rather than a complete market census.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials could be exposed or sent to an untrusted endpoint if DDT_API_KEY or DDT_OPEN_BASE is handled carelessly.

Mitigation: Use the official HTTPS API base by default, keep DDT_API_KEY out of chats, logs, and repositories, and rotate the key if it may have been used with an untrusted base URL.

Risk: Coverage gaps, truncated previews, or unavailable response fields could be mistaken for complete market findings.

Mitigation: Report coverage and data-version information, flag truncated previews, mark missing coverage as unavailable, and avoid inventing metrics that are not returned by the API.

Risk: Results could be over-applied outside the skill's intended automotive aftermarket scope.

Mitigation: Restrict use to automotive aftermarket brands and stop rather than substitute conclusions for restaurant, retail, building-materials, or other unrelated sectors.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/horacetu/skills/ddtclaw-auto-service-network)
- [店店通 DDTClaw Homepage](https://gotoshop-ai.com/ddtclaw/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with concise conclusions, key metrics, coverage notes, limited store details when requested, and inline shell command examples where needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should avoid API keys, storage IDs, supplier details, internal fields, and unsupported metrics.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
