## Description: <br>
AI News Collector guides an agent to collect recent AI news across product launches, research, business, policy, open source, and community sources, then summarize 15-25 items in Chinese by heat with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to perform broad public web research for recent AI news and return a concise Chinese digest ranked by heat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs multiple public web searches and fetches external articles, which may expose search intent to third-party sites or encounter inaccessible and paywalled sources. <br>
Mitigation: Use it only where public web browsing is allowed, avoid sensitive queries, and mark inaccessible or paywalled sources rather than attempting to bypass access controls. <br>
Risk: News summaries can be incomplete, inaccurate, duplicated, or shaped by source bias and SEO aggregation. <br>
Mitigation: Cross-check high-impact items across multiple sources, merge duplicate coverage, cite original sources, and keep summaries objective. <br>
Risk: Summarizing copyrighted or paywalled reporting may create reuse or compliance concerns. <br>
Mitigation: Prefer brief summaries with source links and follow organizational rules for copyrighted and paywalled material. <br>


## Reference(s): <br>
- [Recommended AI news sources](references/sources.md) <br>
- [ClawHub release page](https://clawhub.ai/alvisdunlop/alv-ai-news-collector) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown news digest in Chinese with ranked sections and source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Typically 15-25 items; includes search count, covered dimensions, and update time when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
