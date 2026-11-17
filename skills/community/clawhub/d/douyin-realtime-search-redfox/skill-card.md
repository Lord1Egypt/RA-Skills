## Description:

Searches Douyin works in real time by keyword through RedFox, with sorting, time-window filters, pagination, and optional daily keyword subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, strategy researchers, creators, influencers, and brand operators use this skill to search current Douyin content by keyword, compare engagement signals, refine filters, paginate through results, and optionally monitor a keyword daily.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key and sends Douyin search terms to redfox.hk.

Mitigation: Use a scoped or revocable key where possible, keep it in environment configuration, avoid hardcoding it, and approve searches only for terms you are comfortable sending to RedFox.

Risk: The daily subscription workflow can create recurring searches without detailed cancellation guidance.

Mitigation: Confirm the exact keyword and schedule before enabling a subscription, document where the scheduled job is created, and remove the job when recurring searches are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuanyi-github/skills/douyin-realtime-search-redfox)
- [RedFoxHub API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFoxHub](https://redfox.hk)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tables and guidance from JSON search results, with shell commands for API-key setup or scheduled subscriptions when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and sends user search keywords to RedFox.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
