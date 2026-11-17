## Description:

免费查询全国招标/中标公告（标讯），无需 API Key、无需注册、无需配置。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and procurement-focused agents use this skill to find recent Chinese tender and award notices, including titles, dates, locations, buyers, disclosed amounts, and Zhiliaobiaoxun detail-page links. It is suited to initial bidding-data discovery when free summary fields are enough.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may check for local ZLBX paid-service credentials and switch to a formal paid skill unless the user explicitly asks for the free version.

Mitigation: Use it only when that credential check and possible formal-skill handoff are acceptable; explicitly request the free version when paid-service use is not desired.

Risk: The free search output provides summary fields only and can omit full notice text, original source links, contact details, and complete winner details.

Mitigation: Treat results as discovery summaries and verify important procurement decisions against authoritative full notices or an appropriately licensed complete data source.

Risk: Upgrade links and fuller-data prompts are commercial guidance from the skill publisher.

Mitigation: Evaluate those links and any paid-service transition under the user's normal procurement and security review process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liu-jiapeng/skills/bidding-data-free)
- [Zhiliaobiaoxun free bid-search API](https://mcp-server.zhiliaobiaoxun.com/api_free/search_bids)
- [Zhiliaobiaoxun AI Open Platform](https://ai.zhiliaobiaoxun.com?utm_source=free)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown summaries with bid-notice links and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns summary fields only; full notice text, original source links, contact details, winner details, and bulk export are outside the free output.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
