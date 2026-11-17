## Description:

Use the Dida365 Node.js CLI to manage Dida365 tasks, projects, tags, completed-task queries, full sync, and batch task-management workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oymy](https://clawhub.ai/user/oymy)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to ask an agent for Dida365 CLI commands and workflows for task, project, tag, completed-task, sync, and batch operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI requires broad access to a Dida365 account through cookie-based authentication.

Mitigation: Use it only with accounts and data scopes you are comfortable exposing to the CLI, and avoid sharing cookies in terminals, prompts, logs, or transcripts.

Risk: Commands such as `sync all`, batch operations, and delete operations can expose or change sensitive task-management data.

Mitigation: Review command arguments before execution, prefer JSON outputs only where needed, and treat exported sync data as sensitive account data.

Risk: The documented `npx dida365` installation path may execute an unpinned package version.

Mitigation: Verify the npm package identity and version before running or installing it.

Risk: The skill documents private, unofficial Dida365 API endpoints that may change without notice.

Mitigation: Confirm the CLI still matches Dida365 behavior before relying on it for important workflows.

## Reference(s):

- [Dida365 Open API](https://developer.dida365.com/)
- [Dida365 API base endpoint referenced by the skill](https://api.dida365.com/api/v2)
- [ticktick-py private API implementation reference](https://github.com/lazeroffmichael/ticktick-py)
- [ClawHub skill page](https://clawhub.ai/oymy/skills/dida365-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON-oriented command flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account-affecting Dida365 CLI operations and JSON output options.]

## Skill Version(s):

3.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
