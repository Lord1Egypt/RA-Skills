## Description:

Detects and redacts common personally identifiable information in AI outputs through an instruction-only checklist or an optional paid MCP scan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daririnch](https://clawhub.ai/user/daririnch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data teams, and AI operators use this skill as a privacy checkpoint before sending, logging, or storing model output that may contain personal data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional paid live MCP mode sends the text being scanned to Fronesis Labs and may incur x402/USDC charges.

Mitigation: Use the free instruction-only checklist for offline review, or opt into live mode only after reviewing the server-returned tool terms and price at call time.

Risk: Checklist-style PII detection can miss context-specific identifiers or produce false positives.

Mitigation: Treat the skill as a privacy review aid and keep human review or domain-specific checks in place for regulated or high-impact data flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daririnch/skills/dcl-sentinel-trace)
- [DCL Trust Oracle MCP endpoint](https://mcp.fronesislabs.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and code examples when live MCP use is configured]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include redacted samples, verdicts, finding categories, and audit references when the optional live scan is used.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
