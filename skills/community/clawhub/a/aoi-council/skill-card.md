## Description:

AOI Council provides multi-perspective decision synthesis templates for stress-testing plans and decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmonddantesj](https://clawhub.ai/user/edmonddantesj)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and operators use this skill to send a plan or topic through a structured council of perspectives for decision review, risk identification, recommendations, open questions, and next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Future additions under agents/ can change the perspectives included in the council output.

Mitigation: Review new or modified Markdown files under agents/ before installing or releasing an updated package.

Risk: Council output is decision-support guidance and may surface incomplete or incorrect recommendations.

Mitigation: Review synthesized recommendations before using them for operational, security, or product decisions.

## Reference(s):

- [AOI Council on ClawHub](https://clawhub.ai/edmonddantesj/skills/aoi-council)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style decision synthesis with per-perspective findings and next actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script emits JSON containing the council template and discovered perspective files.]

## Skill Version(s):

0.1.2 (source: server release, _meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
