## Description:

汽服、轮胎和润滑油品牌的门店网络、区域覆盖与位置画像分析，可将腾讯地图中复制出的地点名称和地址文本作为地点输入，并基于店店通已发布门店快照生成可核验结论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to evaluate automotive aftermarket brand store networks, regional coverage, location profiles, and nearby-store context from published DDT data snapshots. It is scoped to chain automotive service, tire, and lubricant brands and stops when coverage, brand identity, or API responses do not support a conclusion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable API base URL could send the DDT API key to an untrusted endpoint if the environment is controlled by an untrusted party.

Mitigation: Keep DDT_OPEN_BASE unset or pinned to https://gotoshop-ai.com/ddtclaw and avoid running the skill where untrusted users can set environment variables.

Risk: Store-network conclusions may be misleading when brand coverage is incomplete, truncated, or unavailable.

Mitigation: Use only published API response fields, report coverage and data-version limits, and stop the business conclusion when the API response does not support it.

## Reference(s):

- [DDT API homepage](https://gotoshop-ai.com/ddtclaw/)
- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-tencent-map-auto-network)
- [Publisher profile](https://clawhub.ai/user/horacetu)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with concise conclusions, key metrics, coverage notes, and limited requested store details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DDT_API_KEY for live API calls; outputs should avoid API keys, storage IDs, supplier fields, internal fields, and unsupported metrics.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
