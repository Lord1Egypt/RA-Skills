## Description:

Send Bark (day.app) push notifications after Codex completes a task, including device name, project name, status, and summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caopulan](https://clawhub.ai/user/caopulan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to notify themselves when Codex or Claude work completes, with enough task context to understand the result without returning to the terminal immediately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notifications can expose task titles, project names, machine name, status, or summaries to Bark.

Mitigation: Keep notification summaries brief and avoid secrets, sensitive incident details, customer data, or other confidential content.

Risk: A changed Bark base URL could route notification content or credentials to an untrusted endpoint.

Mitigation: Set CODEX_BARK_BASE_URL only to a trusted HTTPS Bark endpoint.

Risk: Dry-run output can reveal a real Bark key in logged environments.

Mitigation: Avoid using --dry-run with a real Bark key where terminal output is logged or shared.

## Reference(s):

- [Bark API endpoint](https://api.day.app)
- [ClawHub skill page](https://clawhub.ai/caopulan/skills/bark-notification)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends concise task metadata to a configured Bark HTTPS endpoint; dry runs print the destination, title, and body.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
