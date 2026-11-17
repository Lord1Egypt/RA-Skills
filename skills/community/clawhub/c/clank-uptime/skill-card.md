## Description:

Track website uptime, response times, and availability with CSV-based history, 24-hour stats with visual bars, and average, minimum, and maximum latency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t3mr0i](https://clawhub.ai/user/t3mr0i)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and agents use this skill to check website availability, record response-time history, and summarize 24-hour uptime and latency from local CSV data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores monitored URLs and uptime history under ~/.clank-uptime.

Mitigation: Only add sites you intend to monitor, and handle the local history according to your privacy and retention requirements.

Risk: Cron automation can create recurring external requests to configured sites.

Mitigation: Enable scheduled checks only when recurring monitoring is intended, and choose an interval appropriate for the monitored service.

## Reference(s):

- [Clank Uptime ClawHub release](https://clawhub.ai/t3mr0i/skills/clank-uptime)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and CLI output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cron examples and local file paths for uptime configuration and CSV history.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
