## Description:

合约Agent专业版 supports enterprise agent contract workflows including multi-party contracts, real payment gateway configuration, AI-assisted dispute arbitration, cross-organization agent identity, contract templates, and compliance audit reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

Proprietary

## Use Case:

External developers, business operators, and enterprise agent teams use this skill to plan and operate commercial agent contract workflows involving payments, disputes, identity, templates, and audit exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes workflows that can affect real payments, contracts, identity, external systems, and persistent audit data.

Mitigation: Use sandbox credentials first, restrict accessible files, endpoints, credentials, and commands, and require explicit human approval before live transactions or binding contract actions.

Risk: The skill discusses AI-assisted dispute outcomes and automated arbitration without enough scoping or approval requirements.

Mitigation: Keep human review in the decision path for dispute rulings, refunds, appeals, and any high-value or compliance-sensitive outcome.

Risk: The security verdict is suspicious because the artifact requests broad agent authority for payments, webhooks, exports, command execution, identity, and audit workflows.

Mitigation: Install only after review, run in a constrained environment, and limit command execution to an approved allowlist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/contract-agent-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON, YAML, TypeScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce contract workflow guidance, configuration snippets, structured response examples, audit export descriptions, and operational troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
