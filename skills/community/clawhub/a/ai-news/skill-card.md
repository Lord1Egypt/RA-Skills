## Description: <br>
Retrieves daily news summaries and article details from the cjiot.cc API, with support for date queries, hot-news ranking, category filtering, and article reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vic240821](https://clawhub.ai/user/vic240821) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to answer requests for today's news, news on a specified date, hot stories, category-specific lists, and selected article details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The disclosed third-party API receives requested dates and article IDs. <br>
Mitigation: Avoid using sensitive request details and review whether api.cjiot.cc is appropriate for the deployment environment. <br>
Risk: Returned article text is external news content and may include misleading or instruction-like content. <br>
Mitigation: Treat article content as untrusted text for summarization or display, not as instructions for the agent to follow. <br>


## Reference(s): <br>
- [cjiot daily news API](https://api.cjiot.cc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown or plain text news summaries, with optional shell commands for bundled Node scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts an optional YYYY-MM-DD date for daily news lookup or an article ID for detail lookup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
