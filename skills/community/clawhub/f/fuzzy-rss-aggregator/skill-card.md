## Description:

Monitor, filter, and summarize RSS/Atom feeds on a schedule, including keyword alerts, periodic digests, and optional routing to Discord, webhooks, or Notion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to monitor RSS or Atom feeds, filter entries by age or keywords, and produce recurring news digests or alerts for downstream channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled forwarding can send article titles, links, and summaries to Discord, webhooks, or Notion.

Mitigation: Use public feeds where possible, review destination configuration before enabling schedules, and avoid routing private or internal feed content to third-party services.

Risk: Feed text is untrusted input and may be summarized or reposted by an agent.

Mitigation: Treat feed content as untrusted, review generated summaries before broad distribution, and avoid executing instructions found inside feed entries.

Risk: The Python feed fetcher depends on external package behavior and remote feed availability.

Mitigation: Install dependencies in a pinned virtual environment and monitor scheduled jobs for empty, malformed, or unavailable feeds.

## Reference(s):

- [RSS Aggregator ClawHub listing](https://clawhub.ai/fuzzyb33s/skills/fuzzy-rss-aggregator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, Python, and JSON examples; script output is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scheduled automation recipes and optional forwarding to external services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
