## Description:

Agent Audit Log provides lightweight operational audit logging for AI assistants, agent workspaces, and personal automation systems that need structured records of high-value actions, risks, summaries, and follow-up items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lethehades](https://clawhub.ai/user/lethehades)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to create and maintain lightweight audit trails for safety-relevant actions such as installs, configuration changes, publishing, secret injection events, and unresolved follow-up risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rerunning scripts/init_audit.sh against an existing audit directory can erase the current day's raw audit events.

Mitigation: Review or change the initializer before use so it creates missing files without truncating existing JSONL logs, or back up existing audit logs before running it.

Risk: Audit events may describe sensitive operations such as secret injection or access changes.

Mitigation: Record concise, non-sensitive references and summaries, and redact plaintext secrets from audit logs.

## Reference(s):

- [README](README.md)
- [Schema](references/schema.md)
- [Risk Model](references/risk-model.md)
- [Export Safety](references/export-safety.md)
- [Open Items](references/open-items.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON and JSONL examples plus shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured audit log entries, indexes, summaries, and open-item records; audit content should avoid plaintext secrets.]

## Skill Version(s):

0.1.0 (source: server release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
