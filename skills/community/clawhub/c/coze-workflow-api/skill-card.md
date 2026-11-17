## Description:

Invokes the Coze Workflow stream_run API from OpenClaw using curl, workflow parameters, and a personal access token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chocolatemale](https://clawhub.ai/user/chocolatemale)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call trusted Coze workflows by supplying a workflow ID, JSON parameters, and a Coze PAT through the environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Coze personal access token could be exposed through shell history, logs, or copied examples.

Mitigation: Use a narrowly scoped PAT from an environment variable, avoid pasting real tokens into commands, and rotate the token if it may have been exposed.

Risk: Workflow parameters or results may contain secrets, regulated data, or sensitive business data.

Mitigation: Call only trusted workflows, avoid sending sensitive inputs unless approved, and write outputs to private paths with restrictive permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chocolatemale/skills/coze-workflow-api)
- [Coze Workflow stream_run API endpoint](https://api.coze.com/v1/workflow/stream_run)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The API response is streamed as line-delimited events and may optionally be redirected to a local file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
