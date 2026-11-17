## Description:

Crawls recent X/Twitter posts for configured users and exports Markdown, URL lists, and downloaded media for local review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyingtimes](https://clawhub.ai/user/flyingtimes)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to manage watched X/Twitter accounts, crawl recent posts through OpenClaw Browser Relay, and archive the results as Markdown and text files with local media references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted post content can cause the media downloader to request external URLs and write downloaded files locally.

Mitigation: Use an X-media host allowlist, block private IP ranges, validate redirects and content types, and set download size quotas before crawling untrusted accounts.

Risk: Automated crawls depend on a logged-in X account and can run from the user's network context.

Mitigation: Use a dedicated low-privilege X account and avoid scheduled crawls on sensitive networks.

Risk: Exported Markdown contains untrusted social media content and media references.

Mitigation: Treat generated Markdown as untrusted content and review it before rendering, sharing, or ingesting it into other systems.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flyingtimes/skills/crawl-from-x)
- [OpenClaw Browser Relay Documentation](https://docs.openclaw.ai/guide/browser-relay)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration]

**Output Format:** [Markdown and plain text files, plus command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated result files can include post text, source URLs, interaction counts, and local paths to downloaded images or videos.]

## Skill Version(s):

2.7.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
