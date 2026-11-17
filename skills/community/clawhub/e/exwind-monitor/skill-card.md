## Description:

Monitors the EXWIND website every 10 minutes and prompts the agent to send a Feishu message when new content appears.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lorexxar](https://clawhub.ai/user/lorexxar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor EXWIND updates, detect new articles, and prepare formatted Feishu notifications without duplicate sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled execution may repeatedly open EXWIND, write local state, and trigger Feishu notifications.

Mitigation: Confirm the cron schedule, destination, and notification workflow before enabling the skill.

Risk: The monitor stores sent article IDs in a shared /tmp state file.

Mitigation: Move the state file to a user-owned or application-owned path before running on a shared machine.

Risk: The script uses a shell command wrapper for browser operations.

Mitigation: Harden the wrapper by avoiding shell=True or otherwise constraining command inputs before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lorexxar/skills/exwind-monitor)
- [Publisher profile](https://clawhub.ai/user/lorexxar)
- [EXWIND](https://exwind.net/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON status output with an optional Markdown message body for Feishu delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tracks sent article IDs in a local state file and formats up to five new articles per notification.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
