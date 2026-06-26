## Description: <br>
AI news reading assistant that aggregates 100+ RSS sources, scores user interest, deduplicates across days, and gathers AI/technology news, arXiv papers, GitHub trending projects, and AI company updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingcodingking](https://clawhub.ai/user/kingcodingking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and external users use this skill to collect current AI and technology news, scan recent papers, find trending AI repositories, and produce daily or weekly summaries filtered by category or keyword. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs broad outbound web requests to RSS feeds, arXiv, GitHub Trending, and article URLs. <br>
Mitigation: Review configured sources before use and run only in environments where those outbound requests are acceptable. <br>
Risk: Fetched RSS content may be cached locally. <br>
Mitigation: Avoid running the skill on sensitive feeds or in shared workspaces unless local cache retention is acceptable. <br>
Risk: The URL summarizer can send user-provided URLs to Jina Reader without strong URL limits. <br>
Mitigation: Do not summarize private, internal, authenticated, signed, or sensitive URLs unless the Jina Reader fallback is removed or made explicitly opt-in. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingcodingking/ai-news-hub) <br>
- [Publisher profile](https://clawhub.ai/user/kingcodingking) <br>
- [Project homepage](https://github.com/lanyasheng/ai-news-aggregator) <br>
- [GitHub issues](https://github.com/lanyasheng/ai-news-aggregator/issues) <br>
- [arXiv API](http://export.arxiv.org/api/query?) <br>
- [Hugging Face blog feed](https://huggingface.co/blog/feed.xml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON summaries with links, source names, dates, categories, and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cached RSS content, article excerpts, relevance scores, deduplicated news lists, arXiv paper metadata, and GitHub trending repository details.] <br>

## Skill Version(s): <br>
2.3.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
