## Description:

Monitor RSS and Atom feeds for new content across YouTube, Reddit, GitHub releases, blogs, and other feeds, with optional webhook notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runawaydevil](https://clawhub.ai/user/runawaydevil)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation operators use this skill to configure RSS or Atom feed monitoring, track new items, and send update notifications to webhook-based services while preserving local feed state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can repeatedly fetch arbitrary feed URLs, including private, internal, or local endpoints.

Mitigation: Only add trusted public feed URLs, avoid private or internal addresses, and add URL validation before routine use.

Risk: Enabling cron before verification can repeatedly contact untrusted feeds.

Mitigation: Run manual scans first and enable scheduled execution only after the configured feeds are reviewed.

Risk: Webhook notifications can disclose feed names, article titles, links, and dates to an external service.

Mitigation: Use WEBHOOK_URL only with trusted notification endpoints and account for the data sent in each notification.

Risk: Unpinned dependency ranges can change installed behavior over time.

Mitigation: Pin dependencies before regular or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runawaydevil/skills/feed-watcher)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with shell commands, environment configuration, CLI text output, JSON webhook payload examples, and local state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes feed state to ~/.feed-watcher/feeds.json and may send feed names, item titles, links, and dates to the configured webhook.]

## Skill Version(s):

0.0.1 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
