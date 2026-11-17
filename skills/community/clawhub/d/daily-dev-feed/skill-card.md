## Description:

Curated developer content aggregation powered by daily.dev. Get real-time articles, trending topics, and personalized feeds from thousands of validated sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phancthanhduc](https://clawhub.ai/user/phancthanhduc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to gather current developer articles, trending topics, personalized feeds, bookmarks, and multi-source research from daily.dev.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A daily.dev API token may expose personalized content if copied into logs, shell history, examples, or untrusted tools.

Mitigation: Enter tokens through secure prompts or credential-manager flows, prefer environment variables only for local runtime use, and rotate tokens if exposure is suspected.

Risk: The skill relies on a separately installed daily-dev dependency.

Mitigation: Verify the daily-dev dependency publisher and version before installation or upgrade.

Risk: Automated feed collection can hit daily.dev rate limits.

Mitigation: Check rate-limit headers and back off or retry after the reset window when requests are throttled.

## Reference(s):

- [Daily Dev Feed on ClawHub](https://clawhub.ai/phancthanhduc/skills/daily-dev-feed)
- [phancthanhduc ClawHub Publisher Profile](https://clawhub.ai/user/phancthanhduc)
- [daily.dev Public API OpenAPI Spec](https://api.daily.dev/public/v1/docs/json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and API endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference daily.dev API responses and personalized feed data when the required dependency and API token are available.]

## Skill Version(s):

0.1.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
