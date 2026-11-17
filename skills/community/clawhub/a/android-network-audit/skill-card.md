## Description:

Use when auditing Android/Termux network exposure, connectivity, proxies, listeners, and unsafe ports from the device.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to perform read-only Android or Termux network audits before running services, sharing connectivity, or troubleshooting connectivity, DNS, proxy, listener, and exposure-risk issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit may miss or under-report some UDP listeners, IPv6 cases, fallback parser cases, or machine-readable JSON edge cases.

Mitigation: Treat results as a first pass and verify important findings with platform network tools before relying on the report.

Risk: Network audit reports can include sensitive local interface, DNS, proxy, and listener details.

Mitigation: Keep reports private unless sharing is necessary, and mask credentials or sensitive host details before disclosure.

Risk: Network exposure checks can be misused outside an authorized device or network scope.

Mitigation: Run the skill only on devices and networks where the user has authorization, and keep remediation actions separate from the read-only audit.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or text report with optional shell commands and JSON output from the bundled audit script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should remain read-only, mask credentials, and classify exposure risk as LOW, MEDIUM, or HIGH.]

## Skill Version(s):

1.2.0 (source: frontmatter, release evidence, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
