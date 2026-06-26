## Description: <br>
Research and discover trending content sources for any topic using web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcbaivn](https://clawhub.ai/user/mcbaivn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and social media teams use this skill to gather recent articles, news, videos, and social sources before drafting posts or curated content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries are sent to Brave and Tavily, which can expose sensitive topics if users include confidential information. <br>
Mitigation: Avoid confidential topics or secrets in search prompts and review query text before running searches. <br>
Risk: The skill uses a Tavily API key from the OpenClaw environment. <br>
Mitigation: Use a revocable Tavily key and keep shell/API execution limited to the documented Tavily search request. <br>


## Reference(s): <br>
- [Source Filters Reference](references/source-filters.md) <br>
- [Tavily](https://tavily.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/mcbaivn/content-research-mcbai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown research brief with numbered source lists and article metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source URL, date, summary, auto-detected tag, and search engine label for each result.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
