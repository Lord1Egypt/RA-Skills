## Description:

Collects Facebook personal profile data from a known profile URL through Dataify and returns the final collection result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit Dataify collection jobs for one or more Facebook personal profile URLs, monitor the resulting task, and return the final JSON result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Facebook personal profile URLs to Dataify and may spend account credits.

Mitigation: Use only authorized, necessary profile URLs and confirm scope or bulk collection before execution when cost could materially change.

Risk: The skill depends on a long-lived DATAIFY_API_TOKEN.

Mitigation: Configure the token through an environment variable or secret manager, never paste it into chat, and do not commit it to project files.

Risk: The default wait-and-result flow relies on a separate dataify-task-operations helper in the runtime environment.

Mitigation: Use the default retrieval flow only in runtimes where that helper is trusted and available; otherwise keep the returned task_id and resume through a trusted path.

Risk: Implicit invocation is enabled for a workflow that collects personal-profile data.

Mitigation: Review the target URL and collection scope before execution when the request is ambiguous or involves multiple profiles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-facebook-profile-by-url)
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON results with concise Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task_id, status, submitted parameters, file name, and the final collected result; large payloads may be summarized while preserving access to the raw result.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
