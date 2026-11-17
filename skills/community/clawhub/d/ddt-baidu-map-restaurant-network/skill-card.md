## Description:

使用百度地图地址文本和店店通已发布门店快照，分析餐饮品牌开关店、区域扩张、竞对密度与候选点机会。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External restaurant-location, expansion, and sales teams use this skill to turn Baidu Map address text and selected restaurant brand names into verifiable store-network, competitor-density, and candidate-site analysis based on 店店通 published snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restaurant brands, addresses, and candidate-site queries are sent to the 店店通 API.

Mitigation: Install only if the publisher and API endpoint are trusted, and use the documented DDT_OPEN_BASE endpoint.

Risk: A disclosed API key could be exposed if printed, pasted into chat, or sent to an unexpected endpoint.

Mitigation: Keep DDT_API_KEY in a local environment variable, never include it in responses, and rotate it if it may have been sent elsewhere.

Risk: Preview endpoints can be truncated and are not full store-list export interfaces.

Mitigation: Use aggregate endpoints for conclusions, refine queries when preview.truncated or refine_required is returned, and avoid automatic pagination or region-splitting to reconstruct full datasets.

## Reference(s):

- [店店通 ClawHub API homepage](https://gotoshop-ai.com/ddtclaw/)
- [店店通 API key setup](https://gotoshop-ai.com/ddtclaw/open)
- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-baidu-map-restaurant-network)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise conclusions, key metrics, coverage notes, limited requested details, and inline shell command examples when setup or API calls are needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Avoids exposing API keys, brand IDs, internal store keys, version UUIDs, table names, suppliers, and English enum values.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
