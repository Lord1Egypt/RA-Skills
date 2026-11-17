## Description:

Append-only, hash-chained audit log for AI agents that records agent actions, tool calls, decisions, and external writes with provenance, timestamps, and sha256 chain integrity for EU AI Act Article 12 logging support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roosch269](https://clawhub.ai/user/roosch269)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of AI agents use this skill to add an append-only NDJSON audit log that records actions, tool calls, decisions, external writes, and provenance for compliance review and tamper-evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates durable local records of agent activity that may include sensitive session, credential, wallet, transaction, or other operational metadata.

Mitigation: Restrict audit-log file permissions, define a retention policy, and redact sensitive identifiers and metadata before using the log for compliance or incident evidence.

Risk: The security evidence notes reliability flaws in the sample integrity logic, including the need to fix hash-chain genesis behavior and writer coordination.

Mitigation: Fix the hash-chain genesis mismatch and use locking or a single-writer design before relying on the log for compliance or incident evidence.

Risk: Companion skills may extend agent behavior or integrations beyond this audit trail.

Mitigation: Verify companion skills before installing or wiring them into an agent workflow.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local NDJSON audit-log setup and verification guidance; persistent logs may contain sensitive activity metadata.]

## Skill Version(s):

2.1.0 (source: frontmatter, _meta.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
