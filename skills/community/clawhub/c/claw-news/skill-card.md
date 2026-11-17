## Description:

Claw News generates daily news digests from active topic searches, RSS/Atom feeds, configured interests, AI summaries, and targeted Kickstarter tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[russellfei](https://clawhub.ai/user/russellfei)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to manage news interests, fetch articles from search APIs and RSS feeds, summarize results, and produce scheduled news digests for review or delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships plaintext API keys and may log key prefixes.

Mitigation: Remove the keys from the release, rotate any exposed credentials, stop logging key prefixes, and test only with isolated low-scope keys.

Risk: The skill exposes the user environment to an unverified helper.

Mitigation: Verify or bundle the helper before installation and pass only a minimal required environment to subprocesses.

Risk: Unpinned dependencies, custom API endpoints, cron jobs, and Slack delivery increase operational exposure.

Mitigation: Pin dependencies, restrict custom endpoints, and do not enable cron or Slack delivery until the release has been reviewed.

## Reference(s):

- [Claw News ClawHub Page](https://clawhub.ai/russellfei/skills/claw-news)
- [Kimi API Reference](artifact/references/kimi_api.md)
- [MiniMax API Reference](artifact/references/minimax_api.md)
- [Claude API Reference](artifact/references/claude_api.md)
- [RSS Sources Configuration](artifact/references/rss_sources.md)
- [RSS Output Templates](artifact/references/rss_templates.md)
- [Newsman Kimi API Setup](artifact/rss/SETUP.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown news digests, JSON news records, Slack/plain-text summaries, and command/configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can use configured interests, RSS categories, time windows, API keys, custom endpoints, cron schedules, and delivery channel settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
