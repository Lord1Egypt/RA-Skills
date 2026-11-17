## Description:

Diagnoses TLS/SSL certificate issues for user-provided domains by checking DNS resolution, TCP connectivity, certificate trust, hostname/SAN matching, and certificate validity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to investigate browser certificate errors, HTTPS failures, hostname/SAN mismatches, trust-chain problems, and certificate expiration for domains they explicitly provide.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The diagnostic script makes DNS, TCP, and TLS connections to supplied targets.

Mitigation: Run checks only for domains you are authorized to test, and confirm the target domain before execution.

Risk: Batch input can expand a diagnostic request across many endpoints.

Mitigation: Review batch files before use and avoid broad scans unless explicitly authorized.

Risk: Results depend on local command-line tools, OpenSSL behavior, network reachability, and the system CA bundle.

Mitigation: Verify required tools and CA certificate configuration from the prerequisites reference when results appear incomplete or platform-specific.

## Reference(s):

- [DNS Diagnosis Reference](references/dns_diagnosis.md)
- [Output JSON Schema](references/output_schema.md)
- [Prerequisites](references/prerequisites.md)
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-tls-cert-diagnosis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, json, guidance]

**Output Format:** [Markdown guidance with shell commands and human-readable or structured JSON diagnostic results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script can check a single domain, a custom port, or a batch file of domains and emits JSON by default.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
