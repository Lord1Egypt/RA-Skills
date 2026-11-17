## Description:

Creator Intel V5 generates engineer-focused technology intelligence briefs from international search results and Chinese technology RSS feeds, emphasizing concrete architectures, algorithms, parameters, and implementation details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uuoov](https://clawhub.ai/user/uuoov)

### License/Terms of Use:

MIT

## Use Case:

Developers, hardware-focused product managers, and technical researchers use this skill to generate concise daily briefs about open source projects, technical architecture advances, and innovative hardware without business or fundraising framing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a real-looking Tavily API key in source code.

Mitigation: Revoke the bundled key and require users to supply their own Tavily credential from an environment variable or secret store before running the skill.

Risk: The skill installs Python dependencies and performs outbound HTTP requests to search and RSS providers.

Mitigation: Install dependencies in an isolated environment with pinned versions and review the configured data sources before execution.

Risk: The optional Feishu cron setup can create recurring external publication of generated briefs.

Mitigation: Enable the cron workflow only after explicitly reviewing the target channel, schedule, and publication permissions.

## Reference(s):

- [Creator Intel V5 ClawHub Skill Page](https://clawhub.ai/uuoov/skills/creator-intel-v5)
- [Tavily Search API Endpoint](https://api.tavily.com/search)
- [Jiqizhixin RSS](https://www.jiqizhixin.com/rss)
- [QbitAI RSS](https://www.qbitai.com/feed)
- [OSChina News RSS](https://www.oschina.net/news/rss)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style briefing text with dated heading, categorized entries, source URLs, and short technical summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local history to ~/.openclaw/creator-intel/history.json for URL deduplication.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
