## Description:

Agent fleet coordinator for OpenClaw that sends change-only briefings, priority-sorts errors and handoffs, detects trends against a 7-day average, and can retrigger missed cron jobs across Telegram, Discord, or Slack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waltspence](https://clawhub.ai/user/waltspence)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor OpenClaw agent fleets, receive change-only briefings, and review errors, handoffs, trend anomalies, and missed cron jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured workspace reads may expose credentials, secrets, or sensitive work product.

Mitigation: Restrict the monitored workspace list to the minimum needed and exclude workspaces or paths that contain secrets or sensitive data.

Risk: Briefing content is sent to external messaging platforms.

Mitigation: Use private Telegram, Discord, or Slack destinations and review the briefing contents before enabling delivery.

Risk: Copied or reused agent credentials may grant broader access than the coordinator needs.

Mitigation: Use dedicated scoped credentials with read access to approved workspaces and write access only to configured messaging channels.

Risk: Self-healing cron retriggers can duplicate work or side effects.

Mitigation: Leave self-healing disabled unless each retriggerable cron job is approved and idempotent.

## Reference(s):

- [Coordinator Agent on ClawHub](https://clawhub.ai/waltspence/skills/coordinator-agent)
- [waltspence publisher profile](https://clawhub.ai/user/waltspence)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown briefings and setup guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for silent operation when no fleet changes are detected; messages are delivered to Telegram by default and optionally Discord or Slack.]

## Skill Version(s):

1.2.0 (source: release evidence; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
