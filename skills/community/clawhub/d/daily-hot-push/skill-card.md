## Description:

Daily Hot Push creates a daily Top 10 Chinese trending-news digest for Feishu from Weibo, Zhihu, Baidu, and 36Kr while filtering out celebrity gossip and promotional content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imgolye](https://clawhub.ai/user/imgolye)

### License/Terms of Use:

MIT

## Use Case:

External users and teams who monitor Chinese news trends use this skill to receive a concise daily digest in Feishu or request the digest manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled Feishu delivery can continue sending daily digests until the cron job is removed.

Mitigation: Confirm the cron schedule and recipient before enabling it, and remove the cron job when daily delivery is no longer wanted.

Risk: Public hot-list content is fetched and then sent to the configured Feishu recipient.

Mitigation: Use only an intended Feishu recipient and avoid configuring channels where public news digests would be inappropriate.

Risk: AI filtering of fast-changing hot-list items can omit relevant items or rank less important items highly.

Mitigation: Review the generated digest before acting on time-sensitive or high-impact news.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imgolye/skills/daily-hot-push)
- [Weibo hot list on TopHub](https://tophub.today/n/KqndgxeLl9)
- [Zhihu hot list on TopHub](https://tophub.today/n/mproPpoq6O)
- [Baidu realtime hot list on TopHub](https://tophub.today/n/Jb0vmloB1G)
- [36Kr 24-hour hot list on TopHub](https://tophub.today/n/Q1Vd5Ko85R)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown digest with numbered items and optional cron command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a concise Top 10 digest; Feishu delivery depends on the configured OpenClaw Cron schedule and recipient.]

## Skill Version(s):

1.0.0 (source: frontmatter, artifact/_meta.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
