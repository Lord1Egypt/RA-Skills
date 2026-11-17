## Description:

Diagnoses public internet egress and fixed public IP availability for Alibaba Cloud gateways, SAE applications, and FC functions using read-only cloud queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud engineers and operators use this skill to check whether a confirmed Alibaba Cloud gateway, SAE application, or FC function can reach the public internet and whether its vSwitch has NAT/SNAT egress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic queries use the configured Alibaba Cloud CLI identity.

Mitigation: Use a read-only, least-privilege identity and confirm the product, region, and instance before running diagnostics.

Risk: Reports may reveal account identity, VPC/vSwitch details, NAT/SNAT status, and public egress IPs.

Mitigation: Share diagnostic output only with authorized recipients and redact sensitive infrastructure details when needed.

Risk: A local cache retains account identity information without credentials.

Mitigation: Restrict access to the local identity cache and remove it when no longer needed.

## Reference(s):

- [Instance lookup reference](references/module1_instance_lookup.md)
- [vSwitch egress reference](references/module2_vswitch_egress.md)
- [Read-only RAM policies](references/ram-policies.md)
- [Diagnosis report template](references/report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Human-readable diagnosis report and structured JSON diagnostic results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes egress conclusion, relevant VPC/vSwitch and NAT/SNAT findings, and recommended next steps.]

## Skill Version(s):

0.0.2 (source: server-resolved release metadata and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
