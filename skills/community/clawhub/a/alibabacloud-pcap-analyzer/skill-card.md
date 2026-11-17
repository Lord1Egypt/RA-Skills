## Description:

Analyzes local pcap/pcapng captures to diagnose network transfer and connection problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Network and cloud engineers use this skill to analyze a user-provided packet capture and produce a Markdown diagnosis of likely transfer, connection, DNS, TLS, MTU, or VPN issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saving a report can accidentally overwrite the packet capture.

Mitigation: Keep a backup of the capture and write to stdout or a new, separate report file.

Risk: Reports can contain private IP addresses and domain names, and recommendations may change network settings.

Mitigation: Review reports before sharing, run analysis without administrator privileges, and review network-changing recommendations before applying them.

## Reference(s):

- [Analysis Rules](references/analysis-rules.md)
- [Report Structure](references/report-structure.md)
- [Limitations](references/limitations.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown diagnosis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sections vary with detected traffic; reports may contain private IP addresses and domain names.]

## Skill Version(s):

0.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
