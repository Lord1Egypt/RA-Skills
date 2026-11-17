## Description:

Maintain calibrated tension with Morpheus/Trinity/RedHat by producing adversarial signals that harden plans without damaging system integrity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Agents, developers, and reviewers use this skill to challenge upstream plans, surface weak assumptions, and request clarifications before execution. It is intended for planning review, not for autonomous execution or financial recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may invoke the skill more often than expected during planning conversations.

Mitigation: Install it only when adversarial planning review is desired, and review generated objections before acting on them.

Risk: Adversarial feedback can introduce incorrect or misleading objections into a plan review.

Mitigation: Treat outputs as review guidance and confirm objections, unknowns, and block decisions against governance and safety requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzfshark/skills/adversarial-alignment)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Analysis]

**Output Format:** [Markdown or structured text containing an adversarial_alignment_result with verdict, objections, required clarifications, unknowns, and a response draft.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output is bounded by the skill policy, including max_objections and max_words when supplied.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
