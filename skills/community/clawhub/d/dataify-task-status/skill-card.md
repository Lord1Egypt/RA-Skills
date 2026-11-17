## Description:

Check whether a known Dataify scraper task is processing, successful, or failed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check a Dataify scraper task ID and report whether it is processing, successful, or failed. When Dataify reports success, the bundled status command fetches and prints the completed JSON result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A status check can automatically download and print completed Dataify task results, which may expose sensitive task output or exceed user expectations.

Mitigation: Run it only for task IDs whose completed JSON can be displayed in the session, use a narrowly scoped or disposable Dataify API token where possible, and prefer a version that separates status checks from result downloads when that behavior matters.

## Reference(s):

- [Task Status API](references/task_status_api.md)
- [Dataify Task Status Skill Page](https://clawhub.ai/dataify-server/skills/dataify-task-status)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and provider JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DATAIFY_API_TOKEN and a Dataify task ID; dry-run output redacts the API token.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
