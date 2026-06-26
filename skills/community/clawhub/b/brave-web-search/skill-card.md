## Description: <br>
Searches the web and returns ranked results or AI-generated summarized answers using the Brave Search API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kghamilton89](https://clawhub.ai/user/kghamilton89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to perform real-time web lookups, retrieve ranked results with citations, and request concise AI-generated summaries for factual questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search and answer queries are sent to Brave APIs and may disclose sensitive text if users include it in a query. <br>
Mitigation: Avoid using secrets, credentials, personal data, or confidential business topics unless sending that text to Brave is intentional. <br>
Risk: Unsafe command construction could expose user-provided queries to shell parsing. <br>
Mitigation: Invoke the script with discrete argv elements, such as execFile-style calls, rather than interpolating queries into shell command strings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kghamilton89/brave-web-search) <br>
- [Brave Search API endpoint](https://api.search.brave.com/res/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON results or concise text summaries for agent presentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRAVE_SEARCH_API_KEY for web results and BRAVE_ANSWERS_API_KEY for summarized answers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
