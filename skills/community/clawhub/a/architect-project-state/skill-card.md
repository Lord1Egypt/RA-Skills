## Description:

Maintains versioned, source-traceable architectural project state, including briefs, decisions, change logs, open questions, and bounded task pools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caninlew](https://clawhub.ai/user/caninlew)

### License/Terms of Use:

MIT-0

## Use Case:

Architects, project teams, and agents use this skill to ingest design briefs, meeting notes, consultant feedback, planning conditions, and revisions into controlled project-state records. It supports auditable handoffs by separating source observations, current facts, decisions, open questions, proposals, and bounded tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project-state records may be relied on before human review, even when source authority or confirmation status is incomplete.

Mitigation: Use a narrow project root, review generated state files before relying on them, and keep client, regulatory, statutory, and professional sign-off behind explicit human confirmation.

Risk: Unconfirmed notes, proposals, or agent recommendations could be mistaken for approved project decisions.

Mitigation: Preserve the skill's separation between source observations, stakeholder statements, recommendations, confirmed decisions, and bounded tasks, and do not carry agent recommendations forward without named human approval.

## Reference(s):

- [Project-state schema](references/state-schema.md)
- [Server-resolved GitHub provenance](https://github.com/caninlew/evidence-driven-project-state/tree/main/skills/architect-project-state)
- [ClawHub skill page](https://clawhub.ai/caninlew/skills/architect-project-state)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance, Configuration]

**Output Format:** [Markdown project-state files and change logs using compact tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source IDs, authority domains, confirmation status, version metadata, and review gates.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
