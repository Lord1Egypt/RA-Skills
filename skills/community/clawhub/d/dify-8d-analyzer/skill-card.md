## Description:

Calls a Dify API for 8D problem analysis when the user's message starts with "调用 8D 报告分析助手".

This skill is ready for commercial/non-commercial use.

## Publisher:

[langwang1pm](https://clawhub.ai/user/langwang1pm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and quality teams use this skill to send 8D report analysis requests to a Dify-backed assistant and receive the script output as the agent response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User messages and open_id values are passed to an external Dify routing script and backend.

Mitigation: Use only with a trusted operator, and avoid confidential reports or personal data unless data handling, destination, and retention are documented.

Risk: Command arguments may allow shell-command injection if the external script or executor handles user text unsafely.

Mitigation: Review the dify_router.sh deployment and argument handling before installation, and require safe argument passing without shell interpretation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/langwang1pm/skills/dify-8d-analyzer)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text response from the Dify routing script, with shell command guidance for invocation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires timeout, curl, and jq; Dify processing may take 30 to 120 seconds and the command timeout is configured for 180 seconds.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
