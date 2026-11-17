## Description:

Creates compact, privacy-aware audit records for important agent decisions, including checks performed, failures, changes, evidence, and residual risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to produce concise decision logs for guardrail gates, high-impact actions, refusals, escalations, corrections, and changed plans. The logs help reviewers see what was checked, what remained unverified, how private data was handled, and what risk remains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decision logs may expose sensitive records if raw private details are copied into the log.

Mitigation: Use redacted summaries and avoid secrets, full records, private messages, sensitive logs, and unrelated private data.

Risk: A decision log may be mistaken for a compliance check or proof that unperformed checks passed.

Mitigation: Record only checks actually performed, list unverified items explicitly, and avoid unsupported verification or compliance claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-decision-log)
- [Artifact README](artifact/README.md)
- [Decision log JSON schema](artifact/schemas/decision-log.schema.json)
- [Redacted decision log example](artifact/examples/redacted-decision-log.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Compact Markdown-style decision log bullets or a JSON object matching the bundled decision log schema]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be concise, truthful about checks actually performed, and redacted to avoid secrets or raw private records.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
