## Description:

Queries free public bidding and award notice summaries from Zhiliaobiaoxun for basic procurement opportunity research without registration or an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bailianai](https://clawhub.ai/user/bailianai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and procurement researchers use this skill to search recent Chinese bidding, government procurement, purchase-intent, award-result, and award-publicity notices. It helps identify relevant projects, purchasing entities, disclosed amounts, regions, dates, and detail-page links from free summary data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect configured Zhiliaobiaoxun credentials and route a request to a paid official skill unless the user clearly asks for the free version.

Mitigation: Review the routing behavior before installation and explicitly request the free version when paid lookup should not be used.

Risk: Free-tier results provide only summary fields and may append an upgrade link when free-tier limits or unavailable fields are involved.

Mitigation: Treat the output as summary data only, and use the official paid data source when full notice text, contact details, original links, exports, or larger result sets are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bailianai/skills/bidding-data-free-bailian)
- [Zhiliaobiaoxun free search API](https://mcp-server.zhiliaobiaoxun.com/api_free/search_bids)
- [Zhiliaobiaoxun AI Open Platform](https://ai.zhiliaobiaoxun.com?utm_source=free_official)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown summaries with linked notice titles and concise plain-text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries include title, date, region, purchasing entity, disclosed amount, and Zhiliaobiaoxun detail-page link; unavailable amounts are left blank.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
