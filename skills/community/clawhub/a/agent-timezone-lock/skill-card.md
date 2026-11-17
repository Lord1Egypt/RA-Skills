## Description:

Helps OpenClaw agents report the user's local time accurately instead of mistaking UTC for local time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ferrentinomj-dev](https://clawhub.ai/user/ferrentinomj-dev)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agents configure a user's timezone and check current local time when time accuracy matters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional setup can add persistent timezone instructions that affect future agent sessions.

Mitigation: Use the optional --patch-agents flag only after reviewing the proposed change and confirming that persistent instructions are wanted.

Risk: The skill does not automatically correct every time the agent reports.

Mitigation: Run the supplied time-check script before reporting current local time.

## Reference(s):

- [Timezone skill on ClawHub](https://clawhub.ai/ferrentinomj-dev/skills/agent-timezone-lock)
- [Timezone conversion rules](references/timezone_rules.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Plain text and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Current local time and timezone when the time script is run; setup saves a local timezone configuration.]

## Skill Version(s):

1.2.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
