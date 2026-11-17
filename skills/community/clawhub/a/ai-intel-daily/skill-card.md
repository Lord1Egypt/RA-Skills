## Description:

AI Product Manager daily intelligence digest. Fetches news from 16+ curated RSS sources across tech media, AI labs, research papers, developer communities, and podcasts. Auto-translates to Chinese with deduplication and date filtering. Zero API keys required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[janettbella69](https://clawhub.ai/user/janettbella69)

### License/Terms of Use:

MIT-0

## Use Case:

AI product managers, technical teams, and individual practitioners use this skill to collect recent AI news, research, community posts, and podcast updates into a Chinese Markdown digest for daily intelligence, weekly reports, or scheduled distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs outbound network requests to public RSS sources and Google Translate.

Mitigation: Install and run it only in environments where those outbound connections are permitted and monitored.

Risk: Generated article text and links originate from external feeds and may be inaccurate, malicious, or otherwise untrusted.

Mitigation: Review generated digest content before automated redistribution, and add Markdown escaping or URL validation before using it in downstream automated workflows.

Risk: The runtime depends on third-party Python packages, including googletrans.

Mitigation: Pin dependencies and review package provenance before deployment.

## Reference(s):

- [AI Intel Daily skill page](https://clawhub.ai/janettbella69/skills/ai-intel-daily)
- [Publisher profile](https://clawhub.ai/user/janettbella69)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration]

**Output Format:** [Markdown digest printed to stdout and written to latest_digest.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public RSS feeds, filters recent unseen articles, translates titles and summaries to Chinese, and stores a local seen-article cache.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
