## Description:

Fetches curated AI news, social signals, blogs, papers, events, and skill listings from public Agentic Brew RSS feeds and returns compact agent-friendly results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunxiayi](https://clawhub.ai/user/sunxiayi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external agent users use this skill to retrieve timely AI-related items from public RSS feeds, optionally filtering by category, limit, keyword, and Markdown or JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad or detailed feed requests can produce noisy output or unnecessary recurring fetches.

Mitigation: Keep item limits reasonable, especially for detailed all-feed results, and enable recurring delivery only when the user explicitly asks for it.

Risk: Public RSS endpoints can return unchanged daily content, non-2xx responses, or malformed XML.

Mitigation: Surface endpoint failures clearly, avoid tight polling loops, and treat feed timestamps and source links as part of the result context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunxiayi/skills/ai-news-fetcher)
- [Agentic Brew News Feed](https://www.agenticbrew.ai/feed/news.xml)
- [Agentic Brew All Feed](https://www.agenticbrew.ai/feed/all.xml)
- [Agentic Brew GitHub Feed](https://www.agenticbrew.ai/feed/github.xml)
- [Agentic Brew Paper Feed](https://www.agenticbrew.ai/feed/paper.xml)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown list by default, or JSON array when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be grouped by feed category and can include title, link, publication date, description, and categories.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
