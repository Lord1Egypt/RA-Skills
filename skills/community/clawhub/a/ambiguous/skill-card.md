## Description:

Control an Ambiguous Workspace - tasks, docs, wiki, drive, calendar, CRM, mail, chat, and more - via the `ambiguous` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ambiguous](https://clawhub.ai/user/ambiguous)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover and run authenticated Ambiguous Workspace CLI operations for workspace data such as tasks, docs, wiki pages, drive items, calendar events, CRM records, mail, and chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an unpinned npm CLI that can change behavior between runs.

Mitigation: Use a verified, pinned version of the `ambiguous` CLI before installing or running workspace operations.

Risk: Authenticated CLI commands can read and modify broad workspace data.

Mitigation: Use least-privilege workspace credentials and require explicit user approval before writes, deletes, mail sending, or cross-domain actions.

Risk: The CLI stores API credentials in `~/.ambi/config.json`, and pasted tokens may be captured in shell history or logs.

Mitigation: Treat the config file as sensitive credential storage and avoid pasting real API tokens directly into shell commands.

## Reference(s):

- [Ambiguous homepage](https://ambi.cc)
- [ClawHub skill page](https://clawhub.ai/ambiguous/skills/ambiguous)
- [ClawHub publisher profile](https://clawhub.ai/user/ambiguous)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, json]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI output may be JSON for piped or `--json` use, or human-readable tables and records in an interactive terminal.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
