## Description:

Performs token contract security and degraded address risk assessment using read-only Gate Info MCP data, then produces structured risk reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check token or contract safety signals such as honeypot risk, taxes, holder concentration, name risk, and open-source status. It also handles address-safety requests in a degraded mode that returns basic on-chain address information without treating it as compliance clearance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on shared runtime rule files outside the packaged artifact, so installed behavior may depend on files the package does not include.

Mitigation: Install only when the publisher is trusted and the shared runtime rule files can be verified in the target environment.

Risk: Address-safety mode is degraded and does not provide definitive compliance, sanctions, or blacklist clearance.

Mitigation: Treat address output as basic on-chain information only and use independent compliance checks before making safety decisions.

Risk: Automated token-risk checks can miss risks or return incomplete data.

Mitigation: Keep report warnings visible, label unavailable data, and combine results with manual due diligence before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gaixianggeng/skills/gate-info-risk-check-staging)
- [Gate.com](https://www.gate.com)
- [MCP Specification](references/mcp.md)
- [Scenarios and Prompt Examples](references/scenarios.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown risk report or plain-language clarification/degradation notice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token security reports include risk overview, high-risk details, tax analysis, holder concentration, name risk, project context, overall assessment, and warnings.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter version 2026.4.3-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
