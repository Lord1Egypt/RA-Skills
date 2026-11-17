## Description:

Completion Audit helps an agent determine whether a claimed task outcome is complete by reconstructing success criteria and checking fresh evidence before declaring work done.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raguets](https://clawhub.ai/user/raguets)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to audit completion claims before accepting work as done. It is suited to tasks where the agent should compare claims against observable criteria, direct artifacts, logs, tests, or other authoritative evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mark work as NOT PROVEN when authoritative evidence is unavailable, even if the work may have succeeded.

Mitigation: Provide access to the relevant source artifacts, test outputs, logs, database checks, or direct observations before asking the agent to audit completion.

Risk: Incorrectly derived completion criteria could lead to an incomplete or overly strict audit.

Mitigation: Review the derived criteria against the original objective, constraints, and acceptance conditions before relying on the verdict.

## Reference(s):

- [Overpowered suite](https://github.com/raguets/overpowered)
- [ClawHub skill page](https://clawhub.ai/raguets/skills/completion-audit)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit summary with criteria, evidence, status, verdict, and remaining-work notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses explicit PROVEN, NOT PROVEN, and NOT APPLICABLE status labels.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
