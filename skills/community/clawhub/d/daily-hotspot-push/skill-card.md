## Description:

A self-contained OpenClaw skill for creating, listing, updating, testing, and removing scheduled daily news and hotspot subscriptions with timezone-aware QQBot delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zykkk-power](https://clawhub.ai/user/zykkk-power)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw operators use this skill to manage recurring or test news brief subscriptions for QQBot delivery. It is intended for scheduled pushes, not one-time ad hoc news summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates, updates, and deletes persistent OpenClaw cron jobs that can send future prompts to QQ targets.

Mitigation: Use it only with trusted callers and confirm the target, time, timezone, and topics before creating or changing a scheduled job.

Risk: Weak controls around job ownership and prompt content may allow incorrect scheduled deliveries or user-supplied topics to shape future agent prompts.

Mitigation: Restrict use in shared environments, validate job ownership and topics, and periodically review active subscriptions and cron jobs.

Risk: The skill stores QQ target timezone and subscription data for scheduled delivery.

Mitigation: Treat stored subscription and timezone records as user data, limit access to the skill state files, and delete records when subscriptions are removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zykkk-power/skills/daily-hotspot-push)
- [Publisher profile](https://clawhub.ai/user/zykkk-power)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Concise text or Markdown responses with inline shell commands and JSON command results from the bundled management script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled deliveries produce concise Chinese news briefs grouped by topic, with each item containing a title, source, and short takeaway.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
