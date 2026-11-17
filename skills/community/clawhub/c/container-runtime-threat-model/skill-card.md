## Description:

Generate container runtime threat models analyzing attack surfaces across container components, images, privileges, network exposure, and security controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to generate STRIDE threat models for containerized applications, including Docker, containerd, Kubernetes, and other cloud-native workloads. It helps assess component-level attack surfaces, container escape risks, privileges, network exposure, data sensitivity, compliance context, and prioritized mitigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends container architecture, image names, ports, mounted volumes, privilege settings, security controls, data sensitivity, and compliance context to a third-party API.

Mitigation: Use only with organization-approved third-party processing, avoid secrets and unnecessarily detailed sensitive internals, and redact or generalize infrastructure details before submission where possible.

Risk: The skill requires a ToolWeb API key and each successful API call may be tracked for billing.

Mitigation: Confirm the API key is authorized for this use, disclose expected API use to operators, and monitor rate limits and subscription usage.

Risk: The provided curl examples interpolate user-supplied architecture details into JSON and may be unsafe if copied without proper serialization.

Mitigation: Build JSON payloads with a structured serializer or carefully escape user-controlled values before sending requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/container-runtime-threat-model)
- [ToolWeb Container Runtime Threat Model API](https://portal.toolweb.in/apis/security/crtmg)
- [ToolWeb Platform](https://toolweb.in)
- [ToolWeb API Portal](https://portal.toolweb.in)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown threat-model report with risk scores, STRIDE categories, per-component findings, attack trees, and prioritized mitigations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and TOOLWEB_API_KEY; sends container architecture and security-context details to the ToolWeb API.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
