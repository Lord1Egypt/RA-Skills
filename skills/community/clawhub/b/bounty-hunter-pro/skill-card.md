## Description:

Autonomous bug bounty hunting with scope safety. Scans targets for subdomains, secrets, vulnerabilities. Uses Certificate Transparency logs, JS analysis, entropy-based secret detection. LLM-powered vulnerability analysis. ALWAYS respects authorized targets only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lugave11](https://clawhub.ai/user/lugave11)

### License/Terms of Use:


## Use Case:

External security researchers and developers use this skill to run authorized bug bounty reconnaissance, vulnerability scanning, finding analysis, alerting, and report generation for in-scope targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous scanning can reach targets outside an authorized bug bounty scope if hostname matching is too broad.

Mitigation: Use exact hostname and domain-boundary authorization checks, log each scope decision, and stop execution when the target is not explicitly authorized.

Risk: Secret analysis may expose sensitive findings to cloud-based analysis services.

Mitigation: Keep secret analysis local when possible, or redact sensitive values before sending data to any cloud model.

Risk: Scanner binaries or archives may be installed without verified provenance.

Mitigation: Verify tool sources and hashes before installation, and pin known-good versions of subfinder, httpx, and nuclei.

Risk: Unattended scheduled scans can continue after authorization expires or without adequate review.

Mitigation: Avoid enabling the cron job unless expiry, logging, alerting, and removal steps are defined.

## Reference(s):

- [Bounty Hunter Pro on ClawHub](https://clawhub.ai/lugave11/skills/bounty-hunter-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with shell commands, configuration snippets, JSON findings, and analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates target-specific security reports and live analysis files for authorized targets.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
