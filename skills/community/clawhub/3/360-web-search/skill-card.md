## Description: <br>
Real-time Chinese web search powered by 360's search engine API for recent web, news, market, and China-focused queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rybobo](https://clawhub.ai/user/rybobo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search current Chinese web sources, retrieve recent news or market information, and verify facts that may have changed after an agent model's training cutoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to 360 when the skill is triggered. <br>
Mitigation: Avoid submitting secrets, confidential documents, or sensitive personal data in search prompts. <br>
Risk: The SEARCH_360_API_KEY grants access to a third-party search service. <br>
Mitigation: Protect the API key, do not expose it in prompts or logs, and rotate it if it may have been disclosed. <br>
Risk: API calls may consume paid quota. <br>
Mitigation: Monitor usage and choose search plans appropriate to the query. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rybobo/360-web-search) <br>
- [360 AI Platform](https://ai.360.com/platform) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown search results with cited source URLs, freshness metadata, and setup or error guidance when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SEARCH_360_API_KEY and outbound HTTPS access to api.360.cn; search queries are sent to 360.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
