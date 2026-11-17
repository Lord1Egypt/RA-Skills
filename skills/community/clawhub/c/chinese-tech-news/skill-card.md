## Description:

Fetches the latest Chinese technology news from TMTPost, Huxiu, 36Kr, and ifanr RSS feeds and presents headlines with original links, without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofaith](https://clawhub.ai/user/ofaith)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect a current snapshot of Chinese technology headlines from four named RSS sources and inspect the original article links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound HTTPS requests to third-party media RSS feeds.

Mitigation: Install and run it only where outbound access to the listed feeds is acceptable.

Risk: The reviewed release has hardening gaps around response size limits, request timeouts, redirect allowlisting, and output sanitization.

Mitigation: Review network behavior before deployment and add those controls for stricter production environments.

Risk: Fetched headlines and links originate from external feeds.

Mitigation: Treat feed content as untrusted and inspect links before using them in downstream workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ofaith/skills/chinese-tech-news)
- [TMTPost RSS Feed](https://www.tmtpost.com/rss)
- [Huxiu RSS Feed](https://www.huxiu.com/rss/0.xml)
- [36Kr RSS Feed](https://36kr.com/feed)
- [ifanr RSS Feed](https://www.ifanr.com/feed)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text command-line output with numbered headlines, source names, and original article links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and outbound HTTPS access to the listed RSS feeds; no API key is required.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
