## Description:

CIS benchmark compliance assessment for network infrastructure devices, mapping configuration checks to Management Plane, Control Plane, and Data Plane controls across Cisco IOS, PAN-OS, JunOS, and Check Point.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Network security engineers, auditors, and compliance teams use this skill to collect read-only evidence and map network device settings to CIS benchmark areas for audits, commissioning, post-upgrade checks, and remediation planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Read-only network audit output can still expose secrets, usernames, hashes, community strings, and sensitive topology.

Mitigation: Use least-privilege audit accounts, redact sensitive values where practical, avoid storing raw command output in tickets or reports, and treat generated evidence as confidential.

Risk: Using the wrong CIS benchmark version or applying controls to an unsuitable device role can produce misleading compliance conclusions.

Mitigation: Select the benchmark that matches the platform and OS version, document version gaps and not-applicable controls, and review findings against the device role before remediation.

## Reference(s):

- [CIS Benchmark Audit CLI Reference](references/cli-reference.md)
- [CIS Benchmark Control Reference](references/control-reference.md)
- [CIS Benchmark Audit on ClawHub](https://clawhub.ai/vahagn-madatyan/skills/cis-benchmark-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with read-only CLI commands, compliance scoring guidance, and remediation planning text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [References CIS control IDs for traceability and expects operators to obtain the applicable CIS benchmark document.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
