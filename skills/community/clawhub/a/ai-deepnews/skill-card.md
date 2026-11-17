## Description:

AI DeepNews creates a daily AI product-management intelligence digest by fetching curated public AI RSS feeds, filtering and deduplicating recent items, translating content to Chinese, and outputting a Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[janettbella69](https://clawhub.ai/user/janettbella69)

### License/Terms of Use:

MIT-0

## Use Case:

AI product managers, technical teams, and individual practitioners use this skill to collect recent AI news from curated public feeds and generate Chinese Markdown digest material for daily briefings, weekly reports, or personal tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts public RSS feeds and Google Translate, so article text, summaries, links, and translated output may contain untrusted external content.

Mitigation: Treat generated text and links as untrusted, review links before opening them, and avoid feeding the digest directly into privileged automated workflows.

Risk: Repeated or automated use depends on third-party Python packages and external network services.

Mitigation: Run the skill in an isolated virtual environment, pin dependencies before scheduled use, and monitor failures from feed or translation services.

## Reference(s):

- [AI DeepNews ClawHub skill page](https://clawhub.ai/janettbella69/skills/ai-deepnews)
- [janettbella69 ClawHub publisher profile](https://clawhub.ai/user/janettbella69)
- [OpenAI Blog RSS feed](https://openai.com/blog/rss.xml)
- [Hugging Face Blog RSS feed](https://huggingface.co/blog/feed.xml)
- [arXiv cs.AI RSS feed](https://rss.arxiv.org/rss/cs.AI)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown digest printed to stdout and written to a local latest_digest.md file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The digest groups recent items by source, includes translated Chinese titles and summaries when translation succeeds, and preserves original article links.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
