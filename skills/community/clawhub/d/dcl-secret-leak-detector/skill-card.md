## Description:

Scans AI agent outputs, tool results, and pipeline data for exposed secrets and credentials before they reach users, logs, or downstream systems, either through a free checklist or an optional paid live MCP regex scan with audit proof.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daririnch](https://clawhub.ai/user/daririnch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevSecOps engineers, and agent operators use this skill to check generated outputs, tool results, and pipeline content for exposed API keys, tokens, private keys, database URLs, and .env-style secrets before release or logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live MCP mode sends scanned text to a third-party service and uses an x402 payment flow.

Mitigation: Use the free checklist for highly sensitive material or when network transmission is not acceptable; use live mode only after accepting the Fronesis Labs service and payment flow.

Risk: Live scan audit records include input hashes and finding metadata on-chain.

Mitigation: Treat scan results as security-sensitive records and avoid placing raw secret values in prompts, logs, or downstream reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daririnch/skills/dcl-secret-leak-detector)
- [DCL Trust Oracle MCP endpoint](https://mcp.fronesislabs.com/mcp)
- [Fronesis Labs privacy policy](https://fronesislabs.com/#privacy)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with checklist results; optional live MCP scan returns JSON-style findings, verdict, redacted samples, transaction hash, and verification URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free mode stays in-agent; live mode transmits text to the DCL Trust Oracle MCP server and records input hash and finding metadata on-chain.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
