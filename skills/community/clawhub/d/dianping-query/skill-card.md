## Description: <br>
Guides an agent through querying Dianping for restaurant ratings, average cost, addresses, recommendations, nearby food results, and city-specific search handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guogang1024](https://clawhub.ai/user/guogang1024) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search Dianping for specific restaurants, cuisine or area-based recommendations, and nearby food information, then extract practical restaurant details from results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may direct an agent to use a pre-existing logged-in Dianping session without a clear user consent gate. <br>
Mitigation: Prefer public or logged-out Dianping pages; when a logged-in session is needed, ask the user before using it and explain whose account is active and what account-scoped data may be visible. <br>


## Reference(s): <br>
- [Dianping Hangzhou](https://www.dianping.com/hangzhou) <br>
- [Dianping AI Search URL Pattern](https://www.dianping.com/ai-search?keyword=...) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown instructions and extracted restaurant details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include restaurant names, ratings, average cost, addresses, descriptions, recommended dishes, and review summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
