## Description:

DCL Provenance Tracker helps agents compare baseline and candidate ClawHub skill versions for supply-chain drift, permission creep, suspicious instruction changes, and deterministic provenance proof output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daririnch](https://clawhub.ai/user/daririnch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent operators use this skill after ClawHub skill updates or before deployment to compare a trusted baseline against a candidate release and decide whether version drift should pass, warn, or block.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional DCL Trust Oracle MCP cross-checks may contact an external endpoint and involve transaction metadata or service pricing.

Mitigation: Verify the endpoint, price, and submitted metadata before using the optional cross-check; use pasted baseline and candidate skill contents for the core local diff workflow.

Risk: Incomplete baseline or candidate skill contents can produce misleading PASS, WARN, or BLOCK decisions.

Mitigation: Provide complete prior and candidate skill files, including scripts when present, and review findings before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daririnch/skills/dcl-provenance-tracker)
- [DCL Trust Oracle MCP server](https://mcp.fronesislabs.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with structured JSON provenance-check output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes PASS, WARN, or BLOCK verdicts, risk scores, findings, hashes, and a deterministic DCL fingerprint when the user provides baseline and candidate skill contents.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
