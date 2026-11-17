## Description:

Two-phase daily memory persistence for AI agents. v3.0: unified pack+dispatch cron, smart silence handling, memory importance tiers, cross-group correlation, OQ health tracking, and schedule priority system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffchang2024](https://clawhub.ai/user/jeffchang2024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw administrators use DeepSleep to schedule nightly memory consolidation, per-group memory snapshots, and selective morning briefs for active group sessions. The skill is intended for environments where the operator explicitly wants the agent to retain and restore cross-session context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad cross-session access may expose private or unrelated group and main-session histories.

Mitigation: Enable the skill only in administered OpenClaw environments, use an explicit chat allowlist where possible, and exclude private or direct-message sessions by default.

Risk: Scheduled background runs can persist derived conversation memories without a fresh human review each day.

Mitigation: Review the generated daily summaries and periodically purge memory files according to the organization's retention expectations.

Risk: Automatic Feishu dispatch can send inaccurate or over-broad briefs to group chats.

Mitigation: Require human review before dispatch in sensitive deployments and verify that per-group briefs contain only that group's own summary.

Risk: The optional quality audit can modify instruction files if left fully autonomous.

Mitigation: Require human approval before audit findings change skill instructions or operational policy.

## Reference(s):

- [DeepSleep design document](references/design.md)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub DeepSleep listing](https://clawhub.ai/jeffchang2024/skills/deepsleep)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown files, chat brief text, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates daily summaries, per-group snapshots, schedule entries, dispatch logs, and operational setup guidance.]

## Skill Version(s):

3.0.0 (source: ClawHub release metadata; README version history v3.0, released 2026-04-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
