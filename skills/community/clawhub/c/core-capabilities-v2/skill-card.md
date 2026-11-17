## Description:

Core Capabilities V2 provides a work-assistant toolkit for Obsidian/Git synchronization, a SQLite-backed memory database, natural-language memory queries, cron-based sync, and a local monitoring page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awublack](https://clawhub.ai/user/awublack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and personal-workflow users use this skill to query and synchronize local memory notes, inspect sync status, and configure recurring memory updates for a work-assistant environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local monitoring server can expose memory data without authentication if run on a shared or network-reachable machine.

Mitigation: Run it only on a trusted local machine, bind it to localhost before use in shared environments, and add authentication before exposing it beyond the local host.

Risk: The cron setup installs recurring execution that writes persistent state and logs.

Mitigation: Review setup_cron.sh before running it, confirm the exact crontab entry, and document how to disable or remove the scheduled job.

## Reference(s):

- [Core Capabilities V2 on ClawHub](https://clawhub.ai/awublack/skills/core-capabilities-v2)
- [Publisher profile: awublack](https://clawhub.ai/user/awublack)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with shell commands and Python configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local SQLite query results, sync status text, cron setup instructions, and local monitor API output.]

## Skill Version(s):

2.0.1 (source: server release metadata and artifact metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
