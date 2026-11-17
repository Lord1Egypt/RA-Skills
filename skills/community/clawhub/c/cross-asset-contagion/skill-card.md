## Description:

This retired signal previously provided a cross-asset contagion risk score and is no longer available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Financial analysts and developers previously used the signal to review systemic spillover risk across assets. It is retired, its endpoint returns HTTP 410, and agents should not be configured to call it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The signal endpoint is retired and returns HTTP 410, so any configured calls will fail.

Mitigation: Do not configure an agent to call the endpoint. The artifact states there is no direct replacement.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/kynto2001-ctrl/skills/cross-asset-contagion)
- [Signal status page](https://apexrunner.ai/signals/cross-asset-contagion)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown status and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents the retired status and former purpose; it does not provide an active signal score.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
