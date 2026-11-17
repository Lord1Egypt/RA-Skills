## Description:

Use EverySearch for current web, news, forum, academic, semantic, page-reading, crawling and cross-check retrieval (17 search tools). Use when a task needs up-to-date sources, cited factual verification, or content from a specific public URL or site.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxihexiaoyu](https://clawhub.ai/user/xiaoxihexiaoyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use EverySearch through an agent to retrieve current information from web, news, forums, academic sources, or specified URLs. The agent can use the results and original-source citations to verify factual claims and answer research questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and requested URLs are sent to EveryInfra, which says it retains request parameters; usage may incur charges.

Mitigation: Avoid confidential queries and private or token-bearing URLs, review the privacy policy, and confirm applicable charges before use.

Risk: An exposed API key could allow unauthorized use.

Mitigation: Use a dedicated key restricted to search and store it in secret settings rather than configuration literals.

Risk: Enabled remote tools may expose capabilities beyond the immediate search task.

Mitigation: Review the enabled MCP tools and rely on the live tool list as the source of available capabilities.

## Reference(s):

- [EveryInfra documentation and setup guide](https://everyinfra.com/en/docs?utm_source=clawhub&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=everysearch#quickstart)
- [EveryInfra privacy policy](https://everyinfra.com/en/privacy)
- [EverySearch ClawHub release](https://clawhub.ai/xiaoxihexiaoyu/skills/everysearch)

## Skill Output:

**Output Type(s):** [Search results, Text, Markdown, Source citations]

**Output Format:** [Retrieved source information and citations summarized as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected live search tool; cite original sources and do not treat empty or failed results as proof that information does not exist.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
