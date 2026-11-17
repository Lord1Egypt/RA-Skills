## Description:

Apply engineering judgment across systems, constraints, trade-offs, failure modes, and verification before acting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and operations teams use this skill to structure ambiguous engineering problems into constraints, interfaces, trade-offs, failure modes, execution plans, and verification evidence before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional local memory can persist sensitive preferences or project details if used carelessly.

Mitigation: Enable ~/engineer/ memory only after explicit user consent, and keep stored notes to non-sensitive engineering defaults.

Risk: Engineering guidance can be over-trusted when source evidence is incomplete.

Mitigation: State assumptions, confidence, pass/fail criteria, and the evidence that would change the recommendation.

Risk: Troubleshooting or rollout advice can obscure safety, quality, or restartability constraints under time pressure.

Mitigation: Use hold points, containment steps, rollback paths, and verification checks before irreversible action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/engineer)
- [Skill homepage](https://clawic.com/skills/engineer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Concise Markdown with tables, checklists, decision records, troubleshooting plans, and verification plans when useful.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose optional local memory under ~/engineer/ only with user consent.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
