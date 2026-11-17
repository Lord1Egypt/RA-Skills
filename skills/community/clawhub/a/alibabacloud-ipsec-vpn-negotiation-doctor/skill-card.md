## Description:

Diagnoses Alibaba Cloud IPSec VPN negotiation failures, interruptions, and failed recovery using connection details, negotiation logs, and third-party device configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud network operators and customer support engineers use this agent to diagnose Alibaba Cloud IPSec VPN negotiation failures, interruptions, and failed recovery by reviewing read-only connection data and negotiation logs alongside peer-device settings. It provides likely causes and plain-language configuration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install or upgrade local CLI software without a clear approval step.

Mitigation: Use a reviewed, preinstalled CLI and VPC plugin; obtain approval before installing or changing software.

Risk: Retrieved VPN configuration and negotiation logs can expose sensitive network details.

Mitigation: Limit cloud credentials to the documented read operations for the target VPN, and treat retrieved configuration and logs as sensitive.

## Reference(s):

- [IPSec troubleshooting knowledge](references/ipsec_knowledge.md)
- [Diagnostic patterns](references/diagnostic_patterns.json)
- [Required RAM policies](references/ram-policies.md)
- [ClawHub release page](https://clawhub.ai/sdk-team/skills/alibabacloud-ipsec-vpn-negotiation-doctor)

## Skill Output:

**Output Type(s):** [Analysis, Configuration guidance, Markdown]

**Output Format:** [Natural-language diagnosis and recommendations in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only status and log analysis; credential values are withheld.]

## Skill Version(s):

0.0.1 (source: references/manifest.json, server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
