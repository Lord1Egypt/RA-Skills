## Description:

DCL Skill Auditor performs pre-install static security analysis on ClawHub skills, checking SKILL.md files, scripts, and manifests for malicious patterns and returning a structured PASS, WARN, or BLOCK verdict with audit proof.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daririnch](https://clawhub.ai/user/daririnch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent operators use this skill to review ClawHub skills before installation or update. It supports security checkpoints by identifying credential exfiltration, prompt injection, suspicious shell or network behavior, obfuscation, permission abuse, and behavioral mismatch risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional live MCP check can send hash and verdict metadata to Fronesis Labs or on-chain infrastructure and may require a USDC payment.

Mitigation: Use the free local checklist mode unless the operator explicitly accepts the metadata disclosure and payment flow.

Risk: Scanner examples include credential-exfiltration and malicious-network patterns that could be mistaken for active payloads during review.

Mitigation: Treat those snippets as illustrative examples from the skill documentation and rely on the authoritative security verdict for release risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daririnch/skills/dcl-skill-auditor)
- [DCL Trust Oracle MCP endpoint](https://mcp.fronesislabs.com/mcp)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON with optional code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns PASS, WARN, or BLOCK verdicts with findings, hashes, proof identifiers, and an optional live-check transaction hash.]

## Skill Version(s):

1.0.3 (source: release metadata; artifact text also contains 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
