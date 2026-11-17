## Description:

Deep behavioral security audit for AI agent skills and MCP tools that performs deterministic static analysis, cryptographic lockfile generation, and optional LLM-powered intent analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanguineseal](https://clawhub.ai/user/sanguineseal)

### License/Terms of Use:

AGPL-3.0 with commercial enterprise licensing available

## Use Case:

Developers, security reviewers, and agent platform operators use this skill to audit AI agent skills, tools, plugins, and MCP servers before installation, approval, or release. It helps produce risk-scored findings, lockfile verification guidance, and CI-friendly security reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an external PyPI command-line package over target directories.

Mitigation: Pin and review the aegis-audit package version, verify the PyPI publisher and source, and run scans in a least-privileged workspace.

Risk: Optional LLM analysis can send scanned code to a configured third-party provider.

Mitigation: Keep LLM analysis disabled for sensitive repositories unless the selected provider and data handling are acceptable.

Risk: Audit findings and generated commands can influence installation or release decisions.

Mitigation: Review reports before acting on them and treat the skill as an aid to human security review rather than an automatic approval gate.

## Reference(s):

- [Aegis source repository](https://github.com/Aegis-Scan/aegis-scan)
- [Aegis Audit PyPI package](https://pypi.org/project/aegis-audit/)
- [Skill Developer Best Practices](https://github.com/Aegis-Scan/aegis-scan/blob/main/docs/SKILL_DEVELOPER_GUIDE.md)
- [Aegis licensing details](https://github.com/Aegis-Scan/aegis-scan/blob/main/aegis-core/LICENSING.md)
- [ClawHub skill page](https://clawhub.ai/sanguineseal/skills/aegis-audit)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, JSON]

**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, and report descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide generation of signed lockfiles, CI JSON reports, badge markdown, and MCP configuration.]

## Skill Version(s):

0.1.10 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
