## Description:

Logs autonomous-agent operations, data access, decisions, and budget changes with local hash-chained audit entries for later review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trypto1019](https://clawhub.ai/user/trypto1019)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to record and inspect local activity logs for autonomous-agent actions, decisions, data access, budget changes, integrity checks, exports, and summaries. It is best treated as a convenience activity log unless filesystem permissions and retention are managed separately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit trail may be described more strongly than its local mutable plaintext storage supports.

Mitigation: Treat the output as a convenience activity log and pair it with independent access controls, retention policy, and external log protection for compliance or incident-response use.

Risk: Audit details can contain secrets, tokens, personal data, or sensitive financial/account information.

Mitigation: Avoid logging sensitive values directly; redact details before logging and manage filesystem permissions for ~/.openclaw/audit/.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trypto1019/skills/arc-compliance-audit)
- [Publisher profile](https://clawhub.ai/user/trypto1019)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local JSON audit files under ~/.openclaw/audit/ when commands are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
