## Description: <br>
AI-synthesized web search via Felo API that aggregates multiple sources into structured summaries for research, trend scanning, and cross-source analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iml885203](https://clawhub.ai/user/iml885203) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to query Felo for AI-synthesized web research, community trend summaries, and market or topic analysis across multiple sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Felo as an external search provider. <br>
Mitigation: Do not include secrets, private documents, regulated data, or confidential internal details in search queries. <br>
Risk: The Felo API key could be exposed if stored or handled carelessly. <br>
Mitigation: Use a dedicated API key and store file-based credentials with restricted permissions such as chmod 600. <br>
Risk: Felo results may not provide exact timestamps or guaranteed time filtering. <br>
Mitigation: Use a timestamp-oriented search tool for time-critical lookups or claims that require exact recency. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/iml885203/felo) <br>
- [Felo](https://felo.ai) <br>
- [Felo OpenAPI Chat Endpoint](https://openapi.felo.ai/v2/chat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses FELO_API_KEY and may read an optional key file at ~/.config/felo/api_key.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
