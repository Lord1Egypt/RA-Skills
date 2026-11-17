## Description:

AI-powered banking system for intelligent agents with account management, transaction processing, and risk control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build agent-oriented banking workflows, including account management, transaction processing, digital wallets, marketplace escrow, AI-assisted customer support, and risk control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to install external packages whose ownership and source provenance are not verified by server-resolved import provenance.

Mitigation: Verify package ownership and source provenance before installation, and review the artifact in an isolated test environment.

Risk: The banking API may expose financial workflows with risky defaults if deployed beyond local testing.

Mitigation: Bind the server to localhost unless intentional exposure is required, and add authentication and authorization before any non-demo use.

Risk: Financial data or real accounts could be connected before the artifact has been independently reviewed.

Mitigation: Do not connect real financial accounts or production data based only on this artifact.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/banking-agent-os)
- [Project Homepage](https://github.com/ZhenStaff/openclaw-banking-agent-os)
- [README](https://github.com/ZhenStaff/openclaw-banking-agent-os/blob/main/README.md)
- [Quick Start](https://github.com/ZhenStaff/openclaw-banking-agent-os/blob/main/docs/QUICKSTART.md)
- [API Documentation](https://github.com/ZhenStaff/openclaw-banking-agent-os/blob/main/docs/API_DOCUMENTATION.md)
- [Architecture](https://github.com/ZhenStaff/openclaw-banking-agent-os/blob/main/docs/ARCHITECTURE.md)
- [npm Package](https://www.npmjs.com/package/openclaw-banking-agent-os)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline shell, JSON, Python, TypeScript, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoint guidance and environment configuration examples; requires an OpenAI API key for AI features.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
