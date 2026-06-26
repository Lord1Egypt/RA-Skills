## Description: <br>
Fetches articles from Farnam Street RSS. Use when asking about decision-making, mental models, learning, or wisdom from Farnam Street blog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjw21century](https://clawhub.ai/user/hjw21century) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to retrieve Farnam Street RSS entries by date or keyword and format article metadata and content for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script makes outbound requests to Farnam Street and depends on feedparser and requests. <br>
Mitigation: Install in an isolated environment and pin dependencies when supply-chain assurance matters. <br>
Risk: RSS entries can be unavailable, outside the available date range, or limited to members-only teaser content. <br>
Mitigation: Treat no-content and members-only responses as partial results and verify important article details against the source URL. <br>


## Reference(s): <br>
- [Output Format Reference](references/output-format.md) <br>
- [Farnam Street RSS Feed](https://fs.blog/feed/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with optional JSON from the fetch script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include article URLs, publication dates, content snippets, available date ranges, and members-only indicators.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
