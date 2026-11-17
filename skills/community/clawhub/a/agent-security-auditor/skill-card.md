## Description:

Audits ERC-8004 agents by analyzing registry data, metadata, endpoints, payment configuration, and reputation signals to identify security risks and generate reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aviclaw](https://clawhub.ai/user/aviclaw)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to inspect ERC-8004 agent registrations before interacting with them, especially to spot missing metadata, suspicious endpoints, incomplete payment setup, and unavailable reputation checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit can fetch URLs controlled by the target agent.

Mitigation: Run it in an isolated environment with limited network reachability when auditing untrusted agents.

Risk: RPC URLs or API keys passed on the command line may be exposed through shell history or process listings.

Mitigation: Use non-sensitive RPC endpoints or environment-based secret handling, and avoid credential-bearing RPC URLs in command history.

Risk: Some advertised checks are incomplete or skipped, including reputation lookup and endpoint domain-control verification.

Mitigation: Treat results as triage guidance, not proof that endpoints or reputation were verified.

## Reference(s):

- [ERC-8004 Reference](references/ERC-8004.md)
- [ERC-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004)
- [Agent Security Auditor on ClawHub](https://clawhub.ai/aviclaw/skills/agent-security-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON audit report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a structured JSON report when an output file is requested.]

## Skill Version(s):

1.0.0 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
