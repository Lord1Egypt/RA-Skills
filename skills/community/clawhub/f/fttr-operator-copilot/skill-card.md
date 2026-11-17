## Description:

Connects OpenClaw to FTTR Copilot operator cloud-control APIs through ConnectRPC for managed-device lookup, alert operations, regional stats, network diagnostics, and real-time FTTR query commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fttrai](https://clawhub.ai/user/fttrai)

### License/Terms of Use:

MIT-0

## Use Case:

FTTRAI operators and support engineers use this skill to list managed devices, inspect alerts, check regional stats, run network diagnostics, and issue authorized real-time FTTR query commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured endpoint can receive the operator bearer token and device data.

Mitigation: Use the official HTTPS FTTRAI endpoint or a trusted internal HTTPS endpoint, and protect FTTRAI_OPERATOR_AUTH_TOKEN as a privileged secret.

Risk: mark_alerts_as_read changes FTTRAI alert state.

Mitigation: Confirm the alert IDs and user intent before using the state-changing alert operation.

Risk: Operator data access is limited by the token user's region and permissions.

Mitigation: State when live FTTRAI data is missing or insufficient, and ask for the next identifier or symptom instead of inventing operating procedures.

## Reference(s):

- [FTTR Operator Copilot on ClawHub](https://clawhub.ai/fttrai/skills/fttr-operator-copilot)
- [FTTR Copilot ConnectRPC endpoint](https://fms-main.fttrai.com/api/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON CLI results with concise text or Markdown summaries for agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and FTTRAI_OPERATOR_AUTH_TOKEN; operator API scope depends on token permissions.]

## Skill Version(s):

0.1.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
