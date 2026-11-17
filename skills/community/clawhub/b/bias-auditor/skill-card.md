## Description:

Checks user-provided text for potential group generalizations and stereotypes, then suggests less biased wording.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Content reviewers and developers use this skill to self-check model responses and people-facing copy for potential bias before publication. Findings are heuristic suggestions, not a certified fairness or compliance decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic scans may miss bias or flag benign wording.

Mitigation: Have a person review flagged text and unflagged high-impact content before relying on the results.

Risk: Broad fairness-related wording can trigger an audit when one is not needed.

Mitigation: Confirm the user's intended review scope before applying the skill.

Risk: Chinese-heavy findings may be difficult for some reviewers to interpret.

Mitigation: Translate or clarify findings for the reviewer before making a decision.

## Reference(s):

- [ClawHub bias-auditor release](https://clawhub.ai/zhaoxinghua09-cell/skills/bias-auditor)
- [LGD theory referenced by the skill](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text or JSON findings with suggested wording changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings and command-line output may be in Chinese.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
