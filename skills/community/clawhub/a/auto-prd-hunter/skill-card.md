## Description: <br>
Search web for user pain points and output a PRD JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product builders, developers, and operators use this skill to search for real user complaints around a keyword, extract pain points, and generate a structured PRD with OpenClaw task JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords are sent to external services. <br>
Mitigation: Use non-sensitive keywords and a dedicated Brave Search API key when broader web search is needed. <br>
Risk: Baidu support is documented, but server evidence flags a mismatch around that option. <br>
Mitigation: Do not rely on Baidu behavior until the publisher implements it with declared hosts or removes the stale references. <br>
Risk: Without a Brave API key, results may be limited to Hacker News and may return no_results for non-technical topics. <br>
Mitigation: Handle no_results responses in downstream workflows and configure BRAVE_API_KEY for broader search coverage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lijinhongucl-pixel/auto-prd-hunter) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lijinhongucl-pixel) <br>
- [Brave Search API](https://api.search.brave.com/) <br>
- [Hacker News Algolia Search API](https://hn.algolia.com/api/v1/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns valid JSON only, with success, no_results, or error status; success responses include pain points, user stories, MVP features, OpenClaw tasks, source URLs, and generation metadata.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
