## Description:

CrawlHub is a professional web data extraction platform that provides structured data from social media and messaging platforms (X/Twitter, Instagram, Telegram, LinkedIn, YouTube, TikTok, Facebook, Threads, and more).

This skill is ready for commercial/non-commercial use.

## Publisher:

[wolflabs88](https://clawhub.ai/user/wolflabs88)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and data teams use this skill to work with CrawlHub APIs for public social and messaging platform data extraction, brand monitoring, market intelligence, and data pipeline workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent through broad account, team, API-key, billing, profile, subscription, DELETE, PATCH, or PUT actions.

Mitigation: Keep use read-only by default and require explicit user confirmation before any mutating, billing, team, profile, subscription, or API-key operation.

Risk: Using the skill can require giving an agent access to CrawlHub account tokens.

Mitigation: Use least-privilege credentials, store tokens securely, avoid logging secrets, and install only when CrawlHub access is intended.

Risk: Social and messaging platform data collection may create compliance, privacy, or platform-rule obligations.

Mitigation: Verify that each collection is authorized and compliant with applicable platform rules, privacy obligations, and organizational policy before execution.

## Reference(s):

- [CrawlHub API base URL](https://api.thecrawlhub.com/api/v1)
- [ClawHub skill page](https://clawhub.ai/wolflabs88/skills/crawlhub-reseller)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API endpoint examples, JSON payloads, and shell-style request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API authentication steps, endpoint selection guidance, request examples, response interpretation, and operational safeguards.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
