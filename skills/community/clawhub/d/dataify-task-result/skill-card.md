## Description:

Download the JSON result of a completed Dataify scraper task after a task succeeds or when the user asks to retrieve results for a known task ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve the JSON output for a known completed Dataify scraper task without exposing the API token in chat or command output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Dataify API token is sent to the download endpoint as a URL query parameter, which can be exposed through URL logging.

Mitigation: Use DATAIFY_API_TOKEN only for intended Dataify task downloads, prefer a narrowly scoped token if supported, and rotate the token if URL exposure is suspected.

## Reference(s):

- [Task Result API](references/task_result_api.md)
- [Dataify Task Result on ClawHub](https://clawhub.ai/dataify-server/skills/dataify-task-result)
- [Dataify Publisher Profile](https://clawhub.ai/user/dataify-server)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task-result output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads DATAIFY_API_TOKEN from the environment and redacts the API token from displayed URLs and provider responses.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
