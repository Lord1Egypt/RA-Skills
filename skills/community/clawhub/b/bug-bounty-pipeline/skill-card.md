## Description:

Automated Hunter-Killer pipeline for BlackArch reconnaissance, CVE-MCP enrichment, human-verified exploit triage, and bug bounty reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1beekeeper](https://clawhub.ai/user/1beekeeper)

### License/Terms of Use:

MIT-0

## Use Case:

External security practitioners and developers use this skill to plan and generate an authorized bug bounty workflow for target discovery, vulnerability scanning, CVE enrichment, manual triage, and report preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Aggressive automated reconnaissance and vulnerability scans may run outside authorized scope or exceed platform rate limits.

Mitigation: Run only in a controlled security-testing environment with written authorization, a machine-readable scope allowlist, excluded range blocking, enforced scan-rate limits, and confirmation before active scans.

Risk: CVE enrichment and external API lookups can disclose assessment metadata about targets and findings.

Mitigation: Treat enrichment APIs as disclosure channels, minimize submitted target details, and route enrichment through approved services for the engagement.

Risk: Generated exploit triage and report templates may still require human validation before disclosure.

Mitigation: Manually verify findings, avoid destructive testing and data exfiltration, preserve audit logs, and submit only through the relevant platform policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1beekeeper/skills/bug-bounty-pipeline)
- [Publisher profile](https://clawhub.ai/user/1beekeeper)
- [ARGUS homepage declared by artifact](https://github.com/nousresearch/argus)
- [FIRST EPSS API](https://api.first.org/data/v1/epss)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks, configuration tables, and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance and command/script examples for controlled, authorized security testing workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
