## Description:

Enable Kubernetes pods to obtain Alibaba Cloud access tokens via IDaaS EIAM without static credentials (AccessKey). Covers OIDC federated credential provider setup (three JWKS source modes), M2M client application creation, kubernetes-mode application federated credential, PAM feature permission authorization, id-token-bearer exchange verification, and SDK client-config.json generation. Use for Kubernetes pods without AccessKey, ServiceAccount token exchange, OIDC federated credential providers, static JWKS, kubernetes verification mode, id-token-bearer, pod workload identity, K8s-to-EIAM/IDaaS access tokens, or the Kubernetes path of PAM-to-STS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to configure Kubernetes ServiceAccount OIDC federation with Alibaba Cloud IDaaS EIAM, exchange tokens without static AccessKeys, and prepare SDK client configuration.

### Deployment Geography for Use:

China, Hong Kong, Malaysia, Singapore, South Korea, and Germany (documented EIAM regions)

## Known Risks and Mitigations:

Risk: The security evidence flags TLS weaknesses in the workflow.

Mitigation: Avoid installation until the TLS bypasses are addressed and the affected material has been reviewed.

Risk: The workflow handles live Kubernetes ServiceAccount tokens.

Mitigation: Do not paste live tokens into a conversation or pass secrets as command-line arguments; keep tokens in protected files and remove temporary copies after use.

Risk: Installation relies on a remotely downloaded installer, whose integrity is flagged for review.

Mitigation: Verify the installer source and integrity before running it, and defer installation until those checks are in place.

Risk: The workflow can change persistent CLI settings and update plugins.

Mitigation: Review the proposed CLI changes first and apply them only to the intended profile and environment.

Risk: The workflow performs cloud resource and permission operations beyond basic setup.

Mitigation: Review each requested operation and use the documented minimal RAM policy where possible.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sdk-team/skills/alibabacloud-idaas-kubernetes-m2m-federated-credential)
- [API and federation behavior reference](references/api-and-pitfalls.md)
- [RAM permissions reference](references/ram-policies.md)
- [Aliyun CLI installation guide](references/cli-installation-guide.md)
- [Official Aliyun CLI documentation](https://help.aliyun.com/zh/cli/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown guidance, shell commands, JSON client configuration, and Java sample code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow includes token exchange verification and produces SDK onboarding configuration.]

## Skill Version(s):

0.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
