## Description: <br>
Real-time web search, autosuggest, and AI-powered answers using the official Brave Search API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liujm2012](https://clawhub.ai/user/liujm2012) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the web, retrieve query suggestions, and produce AI-grounded answers with citations when current or external information is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and answer prompts are sent to Brave's API. <br>
Mitigation: Do not include secrets, private internal data, regulated personal information, or other sensitive content in queries. <br>
Risk: The skill requires Brave API keys for search and answers. <br>
Mitigation: Store keys only in environment variables or an uncommitted local .env file, and rotate keys if they are exposed. <br>
Risk: Paid-plan features, usage limits, and costs depend on the user's Brave API plan. <br>
Mitigation: Check the Brave dashboard and current API documentation before production use or high-volume workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liujm2012/brave-api-search-3-0-2) <br>
- [Brave Search API](https://brave.com/search/api/) <br>
- [Brave API Dashboard](https://api-dashboard.search.brave.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text or Markdown search results, autosuggestions, and AI-grounded answers with URLs or citations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Brave API keys from environment variables; rich suggestions, summaries, research mode, limits, and costs depend on the user's Brave plan.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata); artifact metadata also reports 3.0.2 and skill frontmatter reports 3.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
