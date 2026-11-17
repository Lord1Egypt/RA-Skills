## Description:

Run local Laya, Von, CLM, or hosted Jev typed decisions through Decidealot REST or MCP. Use for bounded classification or scoring, Docker deployment, model selection, or local model unloading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Decidealot to run bounded classification, scoring, and true-or-false decisions against a configured local or hosted model endpoint. They review typed answers and probabilities before deciding what action to take.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious because it reports optional plugin installation and Docker setup beyond the declared limits, along with network and filesystem scope and a mutable image.

Mitigation: Use the plugin or deploy a container only when needed; review the requested scope, use a trusted endpoint, and select an immutable image tag for a lasting deployment.

Risk: Decision state may be sent to the configured endpoint, including TypeSafe when a hosted Jev model is selected.

Mitigation: Send data only to a trusted endpoint and confirm it may leave the host before selecting a hosted model; keep authorization and consequential actions in the caller.

## Reference(s):

- [Run and connect to Decidealot](references/setup.md)
- [Decidealot API guide](https://github.com/psyb0t/decidealot/blob/main/docs/api.md)
- [Decidealot deployment guide](https://github.com/psyb0t/decidealot/blob/main/docs/deployment.md)
- [Decidealot ClawHub release](https://clawhub.ai/psyb0t/skills/decidealot)

## Skill Output:

**Output Type(s):** [API Calls, Structured decision results, Text]

**Output Format:** [Typed JSON results with probabilities, summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Choice, score, or true-or-false results; supports single and batched decisions.]

## Skill Version(s):

0.7.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
