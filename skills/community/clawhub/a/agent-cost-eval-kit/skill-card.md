## Description:

Agent Token Cost Signal Kit helps find token waste, repeated calls, and risky routing changes before they become real cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[choosenobody](https://clawhub.ai/user/choosenobody)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to evaluate whether agent changes, retries, scheduled jobs, or routing choices create meaningful token waste or cost risk. It returns an evidence-based status, risk level, and recommended next action without changing production configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token, session, cron, and before/after evidence may contain sensitive operational details.

Mitigation: Redact secrets and private log contents before sharing evidence with the agent.

Risk: Rollback, routing, model, or schedule changes based on cost findings could affect production behavior.

Mitigation: Treat any configuration change as a separate human-reviewed action; the skill itself should remain read-only.

Risk: Sparse samples, mixed workloads, or cache-heavy sessions can produce misleading cost conclusions.

Mitigation: Use comparable before/after evidence and follow watch or investigate recommendations when evidence is incomplete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/choosenobody/skills/agent-cost-eval-kit)
- [Before/After Input Examples](references/before-after-examples.md)
- [Evidence-First Skill Design](references/evidence-first-skill-design.md)
- [OpenClaw Session Inspection Pattern](references/openclaw-session-inspection-pattern.md)
- [ops_cat Quick Check Case Study](references/ops-cat-quick-check-case-study.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown status report with checked evidence, waste signal, risk level, and recommended next action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only guidance; does not calculate exact billing or apply configuration changes.]

## Skill Version(s):

2.4.4 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
