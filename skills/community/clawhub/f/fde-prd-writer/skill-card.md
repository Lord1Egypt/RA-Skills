## Description:

Stage 3 of the FDE Delivery Loop turns an approved problem-discovery package and POC engagement charter into an English PRD specification handoff for engineering, QA, deployment, Agent Skill design, and POC execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xukun0821](https://clawhub.ai/user/xukun0821)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, consultants, product owners, and delivery teams use this skill to turn an approved problem-discovery package and POC engagement charter into a traceable PRD handoff for engineering, QA, deployment planning, agent skill design, POC execution, and adoption/value follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PRD requirements or acceptance criteria may be inaccurate, incomplete, or unsuitable for customer or engineering commitments.

Mitigation: Review generated requirements, priorities, scope changes, and acceptance criteria before sharing them with engineering or customers.

Risk: The local traceability checker can detect identifier and relationship gaps, but it cannot judge business correctness.

Mitigation: Use the checker as a structural aid, then manually validate requirements against the approved problem-discovery package and POC engagement charter.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xukun0821/skills/fde-prd-writer)
- [Method Selection](references/method-selection.md)
- [PRD Quality Gate](references/prd-quality.md)
- [PRD Writing Standards](references/prd-style.md)
- [Test Scenario Design](references/test-scenarios.md)
- [FDE Delivery Loop Handover Contract](references/upstream-downstream-contracts.md)
- [User Story Guidance](references/user-stories.md)
- [PRD Skeleton](templates/prd-skeleton.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown PRD handoff package with optional shell command for local traceability checking]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to English unless the user explicitly requests another language; generated PRDs should preserve traceable FR, AC, TS, POC, and SC identifiers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
