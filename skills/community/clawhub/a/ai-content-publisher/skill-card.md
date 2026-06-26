## Description: <br>
AI Content Publisher helps agents prepare and publish Markdown articles to Medium, Dev.to, and Hashnode with SEO checks, scheduling guidance, and canonical URLs for cross-posting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qoohsuan](https://clawhub.ai/user/qoohsuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and content teams use this skill to turn Markdown articles into platform-ready posts and coordinate publishing across Medium, Dev.to, and Hashnode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may publish unreviewed content, incorrect tags, a wrong canonical URL, or use the wrong destination account. <br>
Mitigation: Review the final article, tags, canonical URL, destination platforms, and selected account before any publish or batch step; prefer draft mode or an explicit confirmation gate. <br>
Risk: API publishing requires credentials such as DEVTO_API_KEY and HASHNODE_TOKEN. <br>
Mitigation: Store credentials in environment variables or a secret manager, avoid pasting tokens into shared content, and do not log request headers containing secrets. <br>
Risk: Batch publishing can exceed platform expectations or create spam-like posting behavior. <br>
Mitigation: Respect documented platform limits and use spacing between posts, especially for Medium where the artifact recommends no more than two articles per 24 hours. <br>


## Reference(s): <br>
- [AI Content Publisher on ClawHub](https://clawhub.ai/qoohsuan/ai-content-publisher) <br>
- [Dev.to Articles API](https://dev.to/api/articles) <br>
- [Hashnode GraphQL API](https://gql.hashnode.com) <br>
- [Medium New Story](https://medium.com/new-story) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires platform credentials for API publishing and should be reviewed before live public posting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
