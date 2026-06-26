## Description: <br>
Web search API for AI agents that returns search result titles, URLs, snippets, and positions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dommholland](https://clawhub.ai/user/dommholland) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent builders use this skill to add web search through the GetPost API, including signup, authentication, and search request examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and returned results are sent through a third-party web search API. <br>
Mitigation: Avoid confidential searches unless the provider is trusted and approved for the intended data. <br>
Risk: API keys may be exposed through shared logs, transcripts, or command history. <br>
Mitigation: Store the GetPost API key outside shared outputs and redact bearer tokens before sharing logs. <br>
Risk: Each search consumes credits, which can create unexpected usage costs. <br>
Mitigation: Monitor credit usage and constrain automated search volume. <br>


## Reference(s): <br>
- [GetPost API Search Documentation](https://getpost.dev/docs/api-reference#search) <br>
- [ClawHub Skill Page](https://clawhub.ai/dommholland/getpost-search) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search requests require a GetPost API key; each search consumes credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
