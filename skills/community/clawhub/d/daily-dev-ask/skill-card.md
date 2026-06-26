## Description: <br>
Answer technical questions by searching daily.dev's developer community article knowledge base and synthesizing answers with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nimrodkra](https://clawhub.ai/user/nimrodkra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to ask technical questions and receive answers grounded in daily.dev community articles, with source links and clear notes when coverage is partial. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a daily.dev API token from the user's environment or secret store. <br>
Mitigation: Use a dedicated, revocable token and keep it in the operating system secret store or an environment variable rather than committing it to files. <br>
Risk: Technical questions and context sent to daily.dev may expose sensitive information to that service. <br>
Mitigation: Avoid sending private code, credentials, or sensitive internal questions unless sharing them with daily.dev is intended. <br>
Risk: A misdirected request could expose the token outside daily.dev. <br>
Mitigation: Verify API calls are made only to api.daily.dev before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nimrodkra/daily-dev-ask) <br>
- [daily.dev Plus](https://app.daily.dev/plus) <br>
- [daily.dev API token settings](https://app.daily.dev/settings/api) <br>
- [daily.dev keyword recommendation endpoint](https://api.daily.dev/public/v1/recommend/keyword?q={keywords}&limit=20) <br>
- [daily.dev semantic recommendation endpoint](https://api.daily.dev/public/v1/recommend/semantic?q={query}&limit=20) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown answer with source links and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Grounds claims in daily.dev article results and includes relevant source links, engagement signals, and coverage gaps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
