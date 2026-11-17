## Description:

Deploydevnlu lets an agent deploy the SupplyWhy application from Slack natural language commands by using SSH, optionally updating the deployment image target, applying Kubernetes configuration, and reporting rollout status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yusong-7456](https://clawhub.ai/user/yusong-7456)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators with authorized Slack access use this skill to trigger and monitor SupplyWhy application deployments to the development EC2/Kubernetes environment. It is intended for controlled release workflows where live infrastructure changes are expected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slack natural language input can trigger live deployment actions with weak validation.

Mitigation: Restrict Slack callers to authorized deployers, require an explicit confirmation step before running kubectl, and keep use to tightly controlled workspaces.

Risk: Environment selection from free text can cause accidental deployment to the wrong target.

Mitigation: Use an exact allowlist for permitted environments and map each environment to explicit infrastructure before any deployment command runs.

Risk: SSH and Kubernetes commands can affect live infrastructure if credentials are overprivileged.

Mitigation: Use least-privileged SSH credentials and Kubernetes access scoped only to the intended deployment resources.

Risk: Shell command construction around deployment inputs can introduce command-interpolation risk.

Mitigation: Avoid shell interpolation for untrusted values and pass validated deployment parameters through fixed command templates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yusong-7456/skills/deploydevnlu)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain text deployment status and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success or failure status after SSH and Kubernetes rollout checks.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
