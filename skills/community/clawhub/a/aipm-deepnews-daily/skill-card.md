## Description: <br>
AI Product Manager daily intelligence digest that fetches AI news from curated RSS sources, translates titles and summaries to Chinese, deduplicates articles, and produces a Markdown digest without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Janettbella69](https://clawhub.ai/user/Janettbella69) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI product managers, technical teams, and individual practitioners use this skill to collect recent AI product, research, developer, and industry news into a Chinese-language daily digest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound requests are made to public RSS feeds and to Google Translate for article titles and summaries. <br>
Mitigation: Use the skill only with feeds whose content may be shared with the translation service; avoid private or internal feeds unless that sharing is acceptable. <br>
Risk: Third-party Python dependencies and external feed content can affect runtime reliability and output quality. <br>
Mitigation: Install dependencies in an isolated environment and review generated digests before using them for product or executive decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Janettbella69/aipm-deepnews-daily) <br>
- [Hugging Face Blog RSS feed](https://huggingface.co/blog/feed.xml) <br>
- [OpenAI Blog RSS feed](https://openai.com/blog/rss.xml) <br>
- [Google AI Blog RSS feed](https://blog.google/technology/ai/rss/) <br>
- [DeepMind Blog RSS feed](https://deepmind.google/blog/rss.xml) <br>
- [Anthropic Blog RSS feed](https://www.anthropic.com/rss.xml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown digest written to stdout and latest_digest.md, with setup and execution commands in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public RSS feeds, uses googletrans for Chinese translation, caches seen article IDs locally, filters articles by recency, and limits per-feed and total article counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
