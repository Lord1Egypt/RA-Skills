## Description:

Persona-weighted pre-send email governance for AI systems that produces APPROVE, BLOCK, or REWRITE decisions, writes decision artifacts to the board ledger, and returns strict machine-parseable JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to gate customer-facing, sales, policy, or other sensitive outbound email drafts before delivery. It returns an approval, block, or rewrite decision with structured rationale and audit artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe emails could receive authoritative-looking approvals if trust or validation assumptions are weak.

Mitigation: Review before installing in real outbound-email workflows and treat decisions as advisory unless constraints come from trusted configuration.

Risk: External votes or reputation weights can influence approval decisions.

Mitigation: Limit external_agent mode to authenticated trusted voters and derive reputation weights from trusted board state.

Risk: State path or guard setting control by untrusted callers could affect decision artifacts or policy behavior.

Mitigation: Use a dedicated non-privileged state directory and do not let untrusted callers control guard settings or vote payloads.

Risk: Dependency drift could change guard behavior over time.

Mitigation: Use pinned, reviewed dependencies and keep them updated through the normal release process.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaicianflone/skills/consensus-send-email-guard)
- [consensus-guard-core npm Package](https://www.npmjs.com/package/consensus-guard-core)
- [consensus-guard-core](https://github.com/kaicianflone/consensus-guard-core)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [JSON, Files, Guidance]

**Output Format:** [Machine-parseable JSON with decision metadata, vote aggregation, final_decision, optional rewrite_patch, and board_writes references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write decision artifacts under the configured consensus state path]

## Skill Version(s):

1.1.15 (source: server release evidence and package.json; SKILL.md frontmatter lists 1.1.14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
