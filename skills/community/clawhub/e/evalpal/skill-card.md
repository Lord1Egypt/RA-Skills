## Description:

Run AI agent evaluations via EvalPal: trigger eval runs, check results, and list available evaluations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewengman](https://clawhub.ai/user/matthewengman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI operations teams use this skill from OpenClaw agents to run EvalPal evaluation definitions, poll run status, and list available evaluations in chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the EvalPal API key to any configured API URL.

Mitigation: Leave EVALPAL_API_URL unset unless you control and trust the exact HTTPS endpoint.

Risk: Evaluation data may be sent to EvalPal or a configured service.

Mitigation: Avoid running sensitive or regulated evaluations unless policy permits sending that data to the service.

Risk: An API key may have been exposed to an untrusted endpoint.

Mitigation: Use a dedicated, low-privilege EvalPal API key and rotate it if it may have been used with an untrusted endpoint.

## Reference(s):

- [EvalPal](https://evalpal.dev)
- [EvalPal API documentation](https://evalpal.dev/api/docs)
- [ClawHub Evalpal skill page](https://clawhub.ai/matthewengman/skills/evalpal)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries and plain-text status or error messages from shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EVALPAL_API_KEY, curl, and jq; run-eval polls for up to 5 minutes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
