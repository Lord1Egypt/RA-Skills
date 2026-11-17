## Description:

滴答清单/TickTick task-management skill for creating, viewing, updating, completing, deleting, moving, and filtering tasks and projects through a Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woodcoal](https://clawhub.ai/user/woodcoal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent manage Dida365/TickTick tasks and projects through explicit CLI commands. It supports OAuth setup, project and task CRUD operations, checklist tasks, due-date queries, inbox lookup, completed-task search, and cache refresh workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores OAuth credentials, access tokens, refresh tokens, and cached task data in local plaintext files.

Mitigation: Protect .env, .dida-token.json, and .dida-cache.json with local file controls; avoid using the skill on accounts containing highly sensitive task data unless those files are secured.

Risk: The skill can create, update, complete, move, and delete live Dida365/TickTick tasks and projects.

Mitigation: Use the skill only for explicit Dida365/TickTick requests and require clear user confirmation before any create, update, complete, move, or delete action, with heightened confirmation for deletions.

Risk: Cached task and project data can become stale and lead to decisions based on old account state.

Mitigation: Use the --force option or clear the local cache when current account state matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/woodcoal/skills/dida365-skill)
- [Dida365 developer platform](https://developer.dida365.com/manage)
- [Dida365 OpenAPI endpoint](https://api.dida365.com/open/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON snippets; CLI execution produces plain text status messages or formatted JSON for task detail output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8+, Dida365 OAuth credentials, and local token/cache files for authenticated use.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
