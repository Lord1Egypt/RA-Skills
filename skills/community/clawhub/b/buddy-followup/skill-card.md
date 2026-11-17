## Description:

Buddy Followup helps agents schedule timed follow-ups for long-running tasks and resume with the saved task context on configured OpenClaw channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiyishr](https://clawhub.ai/user/baiyishr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to set timed reminders after launching builds, scripts, sub-agents, downloads, API calls, or other long-running work. It is intended to help the agent check status later and provide the promised user update.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scheduler has a command-injection bug around delay handling.

Mitigation: Review before installing, use only simple delay values such as 30s, 5m, or 2h, and require a hardened delay parser before sensitive use.

Risk: Saved task context may be broadcast automatically to every configured messaging channel.

Mitigation: Avoid secrets or private project details in task context and verify configured channel recipients before scheduling follow-ups.

Risk: Unverified installation sources can increase supply-chain exposure.

Mitigation: Prefer a pinned, verified install command for deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baiyishr/skills/buddy-followup)
- [Publisher profile](https://clawhub.ai/user/baiyishr)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text, Configuration]

**Output Format:** [Markdown guidance with inline bash command examples and scheduled follow-up message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw gateway, openclaw CLI, and at least one configured messaging channel.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
