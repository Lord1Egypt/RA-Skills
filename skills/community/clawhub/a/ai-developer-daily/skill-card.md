## Description:

AI开发者日报 prepares a daily AI and developer news digest with international news first, China news second, numbered source links, and optional detail expansion when a user replies with an item number.

This skill is ready for commercial/non-commercial use.

## Publisher:

[homer212416](https://clawhub.ai/user/homer212416)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to receive a recurring or on-demand digest of recent AI and developer news, with numbered items that can be expanded into short briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup workflow creates a recurring daily OpenClaw cron message to the current conversation.

Mitigation: Review scheduled cron jobs after setup and remove or change the job when automatic posts are no longer wanted.

Risk: News summaries and expanded briefings depend on external source availability and current web content.

Mitigation: Review linked original sources before relying on a summarized item for decisions or publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/homer212416/skills/ai-developer-daily)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown digest with numbered source links and inline shell command blocks for scheduled delivery setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create a daily OpenClaw cron message to the current conversation when the setup workflow is used.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
