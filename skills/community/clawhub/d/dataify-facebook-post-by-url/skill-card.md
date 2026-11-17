## Description:

Collect a Facebook post and its structured post data from a known post URL. Do not use for post comments, profiles, or events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify Builder jobs for Facebook post URLs, monitor the returned task, and receive the collected JSON result. It is scoped to Facebook post collection by URL, not comments, profiles, or events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script loads a local dataify-task-operations runtime that can execute code and receive the API token.

Mitigation: Use the helper script only with a trusted and reviewed dataify-task-operations runtime, and keep DATAIFY_API_TOKEN in the environment.

Risk: Facebook post URLs, file names, and task metadata are sent to Dataify and may consume Dataify credits.

Mitigation: Submit only authorized inputs, review the target URLs before execution, and confirm that Dataify credit usage is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-facebook-post-by-url)
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill)
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task/result payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit a remote Dataify Builder task, wait for completion, and return a summarized or raw JSON result.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
