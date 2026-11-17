## Description:

Security audit and threat model for OpenClaw gateway hosts. Use to verify OpenClaw configuration, exposure, skills/plugins, filesystem hygiene, and to produce an OK/VULNERABLE report with evidence and fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misirov](https://clawhub.ai/user/misirov)

### License/Terms of Use:


## Use Case:

Developers, operators, and security engineers use this skill to audit OpenClaw gateway hosts they control, collect verified local evidence, identify exposure and configuration risks, and produce a remediation-focused security report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically collects and saves sensitive host, configuration, approval, plugin, and command-output details.

Mitigation: Run it only on OpenClaw hosts you control, choose a private output path, use restrictive file permissions, and treat verified-bundle.json as sensitive.

Risk: Redaction may be imperfect, so generated evidence or reports could still expose sensitive local details.

Mitigation: Review and sanitize verified-bundle.json and the final report before sharing them outside the trusted operational context.

Risk: The optional deep probe expands local gateway testing beyond the default collection.

Mitigation: Use the deep probe only when explicitly intended and after reviewing the collection script for the target host.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/misirov/skills/clawdstrike-test)
- [Required checks](references/required-checks.md)
- [Report format](references/report-format.md)
- [Evidence template](references/evidence-template.md)
- [Threat model template](references/threat-model.md)
- [Verified mode allowlist](references/verified-allowlist.md)
- [Redaction rules](references/redaction.md)
- [Gateway exposure and auth](references/gateway.md)
- [Network evidence checks](references/network.md)
- [Supply chain checks](references/supply-chain.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown audit report with redacted evidence, severity labels, and safe remediation guidance; local verified evidence is saved as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires verified-bundle.json as the report evidence source; optional deep probing is only for explicitly requested local gateway probes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
