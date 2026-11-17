## Description:

Autopilot Guiones F100K searches daily AI news, selects three relevant stories for creators, and turns them into Spanish short-form video scripts with structured hooks, CTAs, and optional delivery to Telegram and Yapper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and F100K operators use this skill to turn current AI news into three ready-to-record Spanish scripts for short-form video. The skill provides source-aware script structure, verbal and visual hooks, on-screen text, and CTAs for each script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scripts can be sent to external services using account credentials.

Mitigation: Confirm the intended Telegram, Yapper, and Gmail destinations, verify token scope, and run manually before enabling any schedule.

Risk: The artifact conflicts about Gmail behavior, saying there is no Gmail draft in one section while later instructing draft creation.

Mitigation: Decide whether Gmail drafts are intended before installation; remove or disable Gmail access if Telegram and Yapper are the only approved destinations.

Risk: Scheduled daily runs could repeatedly deliver generated content before the workflow is fully understood.

Mitigation: Avoid scheduled runs until each destination is configured, tested, and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/autopilot-guiones-f100k)
- [Formula100K publisher profile](https://clawhub.ai/user/formula100k)
- [Yapper application](https://yapper.formula100k.app/app)
- [Yapper scripts API endpoint](https://yapper.formula100k.app/api/scripts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance]

**Output Format:** [Markdown-formatted Spanish video scripts with source URLs, hook fields, CTA sections, and delivery status confirmations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Markdown script files, Telegram messages or documents, Yapper script records, and Gmail drafts when configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
