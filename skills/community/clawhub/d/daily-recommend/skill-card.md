## Description:

Daily Recommend sends concise Chinese-language recommendations for books, poems, quotes, films, and documentaries through scheduled or user-requested prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billxfan](https://clawhub.ai/user/billxfan)

### License/Terms of Use:

MIT-0

## Use Case:

External and individual users use this skill to receive one thoughtful Chinese-language literature or arts recommendation at a time, either through scheduled daily delivery windows or direct requests such as asking for a poem, book, or film recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled recommendations may notify users more often than they want.

Mitigation: Confirm the daily Cron schedule and notification frequency before enabling scheduled delivery.

Risk: Personalization records user preference signals in a local workspace memory file.

Mitigation: Tell users where preference data is stored and review or clear the local memory file when preferences should not persist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/billxfan/skills/daily-recommend)
- [Publisher profile](https://clawhub.ai/user/billxfan)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Feishu-compatible Markdown recommendation message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one recommendation at a time and may update a local workspace preference memory file for personalization.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
