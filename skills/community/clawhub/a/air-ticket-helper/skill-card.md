## Description:

酒店聚合助手整合分贝通、携程、美团、同程、华住会、锦江等多个酒店数据源，帮助代理搜索酒店、查询房型和比较价格。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-zry](https://clawhub.ai/user/ryan-zry)

### License/Terms of Use:

MIT-0

## Use Case:

External travel users and agent developers use this skill to search and compare hotel options across multiple Chinese travel and hotel platforms. The current artifact is best read as a hotel aggregation scaffold because the server security evidence says the real API search, room detail, and booking features are not fully implemented.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release display name indicates an air-ticket helper, while the artifact and server summary describe hotel aggregation.

Mitigation: Review the public listing metadata before release so users are not misled about the skill's travel domain.

Risk: The server security summary says the advertised real API search, room details, and booking features are not actually implemented.

Mitigation: Treat this release as a scaffold until provider API calls are completed, tested, and clearly disclosed.

Risk: Future provider integrations may send travel search details to third-party platforms.

Mitigation: Disclose which fields are sent to each provider and avoid sending unnecessary traveler or company data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-zry/skills/air-ticket-helper)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, API calls]

**Output Format:** [Markdown tables and JSON-like API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve provider attribution and avoid fabricating hotel information, prices, or inventory.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
