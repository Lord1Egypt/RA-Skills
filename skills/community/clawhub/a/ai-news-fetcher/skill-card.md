## Description: <br>
Fetch curated AI news, social signals, blogs, papers, events, and skills from Agentic Brew public RSS feeds and return a compact, agent-friendly list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunxiayi](https://clawhub.ai/user/sunxiayi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and AI practitioners use this skill to fetch current AI news, social trends, papers, events, repositories, and skill listings from public RSS feeds without writing a scraper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to www.agenticbrew.ai and displays links and content from external feeds. <br>
Mitigation: Use it only where outbound access to that domain is acceptable, and treat returned feed content and links as untrusted external information. <br>
Risk: Daily or weekly usage can create recurring automated requests and recurring delivery of external content. <br>
Mitigation: Review and approve any proposed schedule before enabling recurring execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sunxiayi/ai-news-fetcher) <br>
- [Agentic Brew combined RSS feed](https://www.agenticbrew.ai/feed/all.xml) <br>
- [Agentic Brew news RSS feed](https://www.agenticbrew.ai/feed/news.xml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown list or JSON array of feed items, with optional shell command guidance for fetching and parsing RSS feeds.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Items may include title, link, description, publication date, and categories; output can be filtered by feed, limit, keyword query, and format.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
