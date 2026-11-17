## Description:

Queries Dianping restaurant information, including ratings, average spend, addresses, cuisine or area search results, and nearby food recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memoryf](https://clawhub.ai/user/memoryf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Dianping for restaurant names, cuisines, regions, and recommendations, then summarize key restaurant details from search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references a named Dianping login and possible phone/SMS verification flow without clear account ownership boundaries.

Mitigation: Use only an account the operator owns or is explicitly authorized to use, and avoid giving SMS verification codes to an agent unless a secure platform flow is available.

Risk: Restaurant search results and city targeting may be affected by account location, cookies, or Dianping page behavior.

Mitigation: Prefer public browsing where possible, verify the city-specific URL or city parameter, and treat extracted restaurant details as results that may need user confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/memoryf/skills/dianping-query-moss)
- [Dianping Hangzhou page](https://www.dianping.com/hangzhou)
- [Dianping AI search URL pattern](https://www.dianping.com/ai-search?keyword=...)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or concise text summaries of restaurant search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries typically include restaurant name, rating, average spend, address or area, specialties, recommended dishes, and review highlights.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
