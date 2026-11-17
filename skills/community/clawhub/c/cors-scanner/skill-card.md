## Description:

Scans web endpoints for CORS misconfigurations, grades findings from A to F, and reports risky policies such as origin reflection, wildcard access, null-origin trust, credential exposure, subdomain trust, HTTP-origin trust on HTTPS, preflight issues, and private network access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and application teams use this skill to test web APIs and endpoints for CORS policy weaknesses and to generate scan output suitable for manual review or CI checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTPS certificate verification is disabled by default.

Mitigation: Review or fix TLS verification before use, and avoid running scans on untrusted networks until that behavior is addressed.

Risk: The scanner can be pointed at arbitrary endpoints and the evidence notes limited target-scope guardrails.

Mitigation: Use it only on endpoints you own or are explicitly authorized to test.

Risk: Secrets embedded in URLs could appear in scan commands, logs, or reports.

Mitigation: Do not place credentials, tokens, session identifiers, or other secrets in scanned URLs.

## Reference(s):

- [CORS Scanner ClawHub page](https://clawhub.ai/charlie-morrison/skills/cors-scanner)
- [STATUS.md](artifact/STATUS.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Text, JSON, or Markdown scan reports with A-F grades, findings, evidence, and remediation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports batch URL scanning and CI-friendly exit codes with --min-grade.]

## Skill Version(s):

1.0.1 (source: server release evidence; bundled script reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
