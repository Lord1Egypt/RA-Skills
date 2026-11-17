## Description:

Deep Strategy helps knowledge workers decompose, plan, and delegate strategic tasks while prioritizing user-provided requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realroc](https://clawhub.ai/user/realroc)

### License/Terms of Use:


## Use Case:

External users and knowledge workers use this skill to turn broad strategy, research, data-analysis, and writing requests into planned workstreams with delegated subtasks and final deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill attempts to control agent priorities, transparency, and tool choice beyond ordinary task-planning behavior.

Mitigation: Review the skill instructions before installation and use it only where its routing and delegation behavior is acceptable.

Risk: The skill instructs agents to pass required attachments to subordinate tools, which may expose sensitive user-provided files to additional processing steps.

Mitigation: Use it only with attachments that are appropriate for delegated research, retrieval, analysis, or writing workflows.

Risk: The skill directs refusal of internal-instruction disclosure, which may reduce transparency during review or debugging.

Mitigation: Assess the source instructions directly during governance review instead of relying on runtime self-description.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realroc/skills/deep-strategy)
- [ClawHub publisher profile](https://clawhub.ai/user/realroc)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown or plain text task plans, delegation instructions, research materials, and written deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route work through subordinate research, analysis, retrieval, and writing tools when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
