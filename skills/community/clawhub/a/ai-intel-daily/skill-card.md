## Description: <br>
AI Intel Daily fetches AI news from 16+ curated public RSS sources, deduplicates recent items, translates summaries into Chinese, and produces a daily intelligence digest without requiring API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Janettbella69](https://clawhub.ai/user/Janettbella69) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI product managers, engineers, and teams use this skill to collect recent AI news from curated public RSS feeds, translate summaries into Chinese, deduplicate items, and produce a Markdown digest for daily or weekly intelligence workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched article titles and snippets are sent to Google Translate for Chinese summaries. <br>
Mitigation: Use the skill with public feeds only, or disable or replace the external translation step before adding private or internal feeds. <br>
Risk: Generated digests can contain stale, incomplete, or mistranslated third-party news summaries. <br>
Mitigation: Review the linked original articles before relying on the digest for product, engineering, or business decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Janettbella69/ai-intel-daily) <br>
- [Hugging Face Blog Feed](https://huggingface.co/blog/feed.xml) <br>
- [OpenAI Blog RSS](https://openai.com/blog/rss.xml) <br>
- [arXiv cs.AI RSS](https://rss.arxiv.org/rss/cs.AI) <br>
- [arXiv cs.CL RSS](https://rss.arxiv.org/rss/cs.CL) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown digest printed to stdout and written to latest_digest.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local seen_articles.json cache for deduplication and limits articles by feed, total count, and recency.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
