## Description: <br>
Aggregates and deduplicates AI news from multiple Chinese and English technology sources into a categorized digest with titles, summaries, and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and teams use this skill to gather current AI news from multiple Chinese and English technology sources and receive a deduplicated, categorized markdown digest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound web requests and may use general web search when source pages fail. <br>
Mitigation: Review the default source list for the deployment environment and verify important items against linked source pages before relying on the digest. <br>
Risk: News coverage can be incomplete, stale, duplicated, or unavailable when public sources fail or change. <br>
Mitigation: Treat the digest as a current-news aid, preserve source links in the output, and note failed sources when coverage is incomplete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/big-ai-news) <br>
- [TechNews AI category](https://technews.tw/category/ai/) <br>
- [QbitAI](https://www.qbitai.com/) <br>
- [TechNice AI category](https://www.technice.com.tw/category/issues/ai/) <br>
- [AIBase daily news](https://news.aibase.com/zh/daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown news digest with categorized numbered entries, briefs, links, and top picks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Adapts response language to the user's query; duplicate stories may be merged with multiple source links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
