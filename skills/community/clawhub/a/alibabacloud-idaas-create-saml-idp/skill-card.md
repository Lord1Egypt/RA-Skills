## Description:

Guides users through creating, updating, inspecting, validating, and troubleshooting inbound SAML 2.0 identity providers in Alibaba Cloud IDaaS EIAM with Alibaba Cloud CLI, including metadata review and service-provider setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and identity administrators use this skill to configure and troubleshoot inbound SAML identity providers for Alibaba Cloud IDaaS EIAM. It guides metadata review, safe configuration planning, status checks, and the handoff of IDaaS service-provider details to the external identity provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flagged metadata retrieval that may reach private or loopback services or downgrade HTTPS; analysis was partial and the result signals concern without establishing malicious intent.

Mitigation: Review or correct metadata request behavior before installing, especially where the agent can reach private network services.

## Reference(s):

- [Alibaba Cloud CLI installation guide](https://www.alibabacloud.com/help/en/alibaba-cloud-cli/latest/installation-guide)
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-idaas-create-saml-idp)
- [EIAM SAML IdP OpenAPI reference](references/openapi.md)
- [RAM policies](references/ram-policies.md)
- [SAML IdP troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance and tables, CLI commands, and structured metadata or configuration output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SAML endpoints, public certificate fingerprints, warnings, and configuration-check results.]

## Skill Version(s):

0.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
