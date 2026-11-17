## Description:

A prompt-only executive assistant skill that helps CEOs and executives clarify goals, plan strategy, decompose work, guide execution, support decisions, and review progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nemo-ryanniddel](https://clawhub.ai/user/nemo-ryanniddel)

### License/Terms of Use:

MIT-0

## Use Case:

Executives, founders, operators, and supporting staff use this skill to turn objectives into milestones, tasks, and next actions, while receiving concise planning, decision-support, execution guidance, and review outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger keywords and executive-assistant framing may cause this prompt to activate in many planning, project, strategy, or decision contexts.

Mitigation: Install only where broad executive workflow behavior is desired, and override or disable the skill for narrower specialist workflows.

Risk: Autonomous-execution language could encourage an agent with connected tools to act on messages, records, files, or commitments too readily.

Mitigation: Require explicit user confirmation before sending messages, changing business records, accessing private files, making commitments, or taking externally visible actions.

Risk: Decision-support guidance can be incomplete, outdated, or inappropriate for regulated legal, medical, financial, or business-critical contexts.

Mitigation: Treat outputs as planning assistance, verify important facts, and route regulated or high-impact decisions to qualified human review.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured bullets, checklists, numbered plans, and review sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are intended to be concise and to end with one concrete next recommended action.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
