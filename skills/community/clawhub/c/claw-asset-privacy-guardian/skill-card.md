## Description:

Scans local files for credential, account-security, privacy-configuration, and digital-asset risks, then generates anonymized reports and remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[betsymalthus](https://clawhub.ai/user/betsymalthus)

### License/Terms of Use:

MIT

## Use Case:

Developers, security reviewers, teams, and privacy-conscious users use this skill to scan local projects and configurations for sensitive information, account-security gaps, and asset-related exposure. It helps produce anonymized security reports and practical remediation guidance without intentionally sending scan contents to external services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scan boundaries and privacy promises may not fully match implementation behavior.

Mitigation: Use the tool only on directories you intend to inspect and treat reports as sensitive until a human reviews paths, locations, and summary details.

Risk: Exclude patterns may not provide strict privacy boundaries, especially when scanning untrusted repositories or symlink-heavy trees.

Mitigation: Avoid scanning untrusted repositories with symlinks and do not rely on excludePatterns as the only control for sensitive files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/betsymalthus/skills/claw-asset-privacy-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Console text, JSON, and Markdown reports, with CLI and Python API usage examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are intended to be anonymous and local, but paths and locations should be reviewed before sharing.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
