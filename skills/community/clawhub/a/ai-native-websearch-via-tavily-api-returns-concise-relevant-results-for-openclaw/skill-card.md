## Description: <br>
Performs AI-optimized web searches via Tavily through AIsa, returning concise results with options for depth, topic, and result count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run web searches, retrieve concise source summaries, and extract page content through the AIsa Tavily API proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and URLs are sent to AIsa/Tavily when the skill is invoked. <br>
Mitigation: Use only queries and URLs approved for that provider, and avoid secrets, internal-only links, personal data, or confidential investigation targets. <br>
Risk: The skill requires an AISA_API_KEY for authenticated API calls. <br>
Mitigation: Use a dedicated key where possible and rotate or revoke it according to organizational credential policy. <br>


## Reference(s): <br>
- [ClawHub listing: Web Search Tavily](https://clawhub.ai/0xjordansg-yolo/ai-native-websearch-via-tavily-api-returns-concise-relevant-results-for-openclaw) <br>
- [AIsa](https://aisa.one) <br>
- [AIsa marketplace](https://marketplace.aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls] <br>
**Output Format:** [Markdown-style terminal output with answer, source, extraction, and failure sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are capped at 20; URL extraction returns raw page content when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
