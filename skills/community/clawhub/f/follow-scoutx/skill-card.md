## Description:

Installable digest skill for OpenClaw or Claude Code. Use when the user wants a personalized ScoutX briefing with conversational setup, local preference storage, and minimal end-user configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangchao228](https://clawhub.ai/user/yangchao228)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw and Claude Code users use this skill to configure personalized AI digests from ScoutX curated media plus first-party X and podcast feeds. It stores local preferences, previews or delivers digests, and can help set up recurring OpenClaw delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring delivery can persist OpenClaw cron jobs and send digest output to chat or external channels.

Mitigation: Inspect the dry-run cron payload before applying it, use explicit delivery targets, and replace existing generated jobs deliberately when schedules change.

Risk: The helper fetches content from packaged feed URLs and can accept local service or environment feed URL overrides.

Mitigation: Install only when the feed provider and operator are trusted, and avoid untrusted feed URL overrides.

Risk: Local profile, service, and prompt files can contain user preferences or operator configuration.

Mitigation: Keep secrets out of local prompt and profile files, and review local overrides before sharing or reusing the skill environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangchao228/skills/follow-scoutx)
- [ScoutX public feed endpoint](https://input.reai.group/v1/public/feed)
- [ScoutX public metadata endpoint](https://input.reai.group/v1/public/meta)
- [Follow Builders X feed](https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-x.json)
- [Follow Builders podcast feed](https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-podcasts.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain-text digests, JSON payloads for validation, and shell commands for setup or OpenClaw delivery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Digest output may be split into multiple message chunks for delivery; local profile, state, service override, and prompt files are stored under ~/.follow_scoutx/.]

## Skill Version(s):

0.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
