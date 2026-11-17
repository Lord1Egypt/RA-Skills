## Description:

Collect structured Google Shopping product records in bulk by keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify Google Shopping keyword collection tasks, wait for completion, and retrieve structured product records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags mismatched localized instructions, token handling, and an unpinned helper-code import.

Mitigation: Review the localized Chinese instructions and the external dataify-task-operations dependency before installation.

Risk: API tokens may be exposed if passed directly on the command line.

Mitigation: Use a session-scoped DATAIFY_API_TOKEN or a secret manager, and never print token values.

Risk: The helper task_runtime code is imported from an adjacent dataify-task-operations dependency.

Mitigation: Verify the helper dependency comes from a trusted, pinned source before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-google-shopping-keywords)
- [Dataify Scraper API builder endpoint](https://scraperapi.dataify.com/builder?platform=1)
- [Dataify dashboard](https://dashboard.dataify.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON collection results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a task ID and resume command if monitoring times out or is interrupted.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
