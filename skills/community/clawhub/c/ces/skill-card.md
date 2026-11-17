## Description:

Manage a self-hosted Trello-like WeKan board through `wekancli`, including creating, moving, archiving, restoring, and deleting boards, lists, cards, comments, and checklist items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manman1104](https://clawhub.ai/user/manman1104)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to manage tasks on a self-hosted WeKan server from a configured command-line session. It is suited for board, list, card, comment, and checklist workflows, not GitHub issues or simple reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned executable from a mutable GitHub repository.

Mitigation: Pin the CLI dependency to a reviewed commit or release before production use.

Risk: The skill uses an authenticated WeKan token with write access to board data.

Mitigation: Use a dedicated least-privileged WeKan account and avoid admin tokens unless the requested operation requires them.

Risk: Board, list, and card operations can move, archive, restore, or delete work items.

Mitigation: Confirm target board, list, card, and checklist IDs before executing write operations, and prefer archive over delete when recovery may be needed.

Risk: Login can print access tokens that may be exposed in chat or logs.

Mitigation: Avoid displaying tokens after login and keep `WEKAN_TOKEN` out of shared transcripts and logs.

## Reference(s):

- [WeKan CLI Reference](references/cli-examples.md)
- [WeKan CLI Skill Installation Notes](references/user-install.md)
- [ClawHub skill page](https://clawhub.ai/manman1104/skills/ces)
- [WeKan CLI install package](https://github.com/madsmith/wekan_cli.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON CLI output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose authenticated WeKan CLI operations that read or change board data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
