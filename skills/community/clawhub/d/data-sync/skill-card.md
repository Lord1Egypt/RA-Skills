## Description:

Data Sync helps agents coordinate Git and SSH synchronization of Claude Code configuration and knowledge repositories across devices through a relay server, with GitHub used for milestone archives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mwangxiang](https://clawhub.ai/user/mwangxiang)

### License/Terms of Use:


## Use Case:

Developers and Claude Code users use this skill to initialize, pull, push, back up, and inspect synchronized configuration, skill, hook, memory, and knowledge-base repositories across multiple computers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow syncs sensitive Claude configuration, hooks, skills, and memory through a fixed relay server.

Mitigation: Use the skill only with a relay server and GitHub account you own or explicitly trust, and review every file before pushing.

Risk: Root SSH access and copied private keys can broaden compromise if a device or relay is exposed.

Mitigation: Replace root SSH access with a restricted Git user and generate a unique SSH key for each device.

Risk: Personal access tokens in remote URLs or plaintext credential stores may expose GitHub credentials.

Mitigation: Avoid PATs in URLs or plaintext stores; use safer credential management and rotate any token that may have been exposed.

Risk: Basic secret scanning may miss credentials in configuration, hooks, skills, or memory files.

Mitigation: Run stronger secret scanning before synchronization and exclude sensitive files from tracked repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mwangxiang/skills/data-sync)
- [Publisher profile](https://clawhub.ai/user/mwangxiang)
- [Sync registry](sync-registry.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and operational status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command-oriented synchronization guidance and requires user confirmation for push and backup operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
