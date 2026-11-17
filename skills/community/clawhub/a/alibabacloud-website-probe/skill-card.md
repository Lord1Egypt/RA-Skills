## Description:

Multi-region website availability probing and nationwide multi-ISP network testing over a public probing platform (HTTP / Ping / DNS / MTR / traceroute), with an optional mobile 4G/5G perspective.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site reliability engineers use this skill to diagnose regional and carrier-specific website or API availability, latency, HTTP, DNS, and routing problems through public multi-region probes.

### Deployment Geography for Use:

China nationwide across three major carriers; overseas probe coverage is limited.

## Known Risks and Mitigations:

Risk: Full target URLs are sent to the public probing provider and may contain credentials or confidential information.

Mitigation: Probe authorized public targets and remove passwords, signed links, tokens, and confidential endpoints from URLs.

Risk: Availability results do not establish TLS security because target certificate verification is disabled by default.

Mitigation: Assess certificate and TLS security separately before relying on a target's HTTPS configuration.

Risk: Network probe conclusions may be incomplete or lead to incorrect configuration changes.

Mitigation: Compare the reported regional evidence, verify conclusions, and keep dependencies updated before changing configurations.

## Reference(s):

- [Boce public probing platform](https://boce.aliyun.com/)
- [Diagnostic rules](references/diagnostic-rules.md)
- [User guide](references/user-guide.md)
- [RAM policies and cloud authorization](references/ram-policies.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [Diagnostic text summaries and JSON probe result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Probe findings compare results across regions and carriers.]

## Skill Version(s):

0.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
