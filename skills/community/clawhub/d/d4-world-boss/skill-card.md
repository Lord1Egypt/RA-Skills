## Description:

Retrieves Diablo IV world boss countdown and status data from the Caimogu map site, then asks whether to set a reminder when a future spawn is pending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crazzies](https://clawhub.ai/user/crazzies)

### License/Terms of Use:


## Use Case:

External Diablo IV players use this skill to check the current world boss, spawn status, and countdown. When the boss is not already active, the agent may offer reminder guidance before the expected spawn window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional cron reminders can create persistent host changes.

Mitigation: Before allowing a reminder, require the agent to show the exact cron entry, confirm it is one-time or bounded, and provide the removal command.

Risk: The skill depends on live data fetched from map.caimogu.cc.

Mitigation: Treat unavailable or malformed responses as a failed lookup and avoid acting on reminder prompts when the countdown cannot be verified.

## Reference(s):

- [Caimogu Diablo IV Map Data Source](https://map.caimogu.cc/d4.html)
- [ClawHub Skill Page](https://clawhub.ai/crazzies/skills/d4-world-boss)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text status report with optional reminder guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask the user before creating a cron-based reminder.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
