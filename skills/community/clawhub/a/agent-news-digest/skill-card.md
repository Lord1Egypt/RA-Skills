## Description: <br>
키워드 기반 뉴스 수집 및 3줄 요약 에이전트 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinu4you](https://clawhub.ai/user/jinu4you) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and external users use this skill to collect recent news for a topic, summarize articles in Korean, score their importance, and return a concise briefing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Startup behavior can automatically spend API-key quota on a hard-coded Bitcoin news job without an explicit user request. <br>
Mitigation: Remove or disable the automatic mock job and run searches only after an explicit agent job is received. <br>
Risk: Topics and retrieved article snippets are sent to Tavily and the selected LLM provider. <br>
Mitigation: Use limited, revocable API keys and avoid submitting sensitive topics or content unless the provider data handling is acceptable. <br>


## Reference(s): <br>
- [Agent News Digest on ClawHub](https://clawhub.ai/jinu4you/agent-news-digest) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>
- [Groq OpenAI-compatible API endpoint](https://api.groq.com/openai/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [JSON job result containing article metadata, summaries, importance scores, and a Korean markdown briefing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 10 requested items after sorting by importance score.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
