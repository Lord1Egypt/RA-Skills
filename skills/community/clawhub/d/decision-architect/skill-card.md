## Description:

决策架构师 helps agents structure decisions by comparing options, matching decision frameworks, flagging potential cognitive-bias signals, and prompting later reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, teams, and agent users use this skill when a conversation contains a meaningful tradeoff and they need structured option comparison, framework-guided analysis, bias checks, and review notes. It is suited to product, technical, business, and personal decision support where the user remains responsible for the final decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says declared command and file permissions are broader than the skill documentation says it needs.

Mitigation: Install only in agent environments where file and command access can be reviewed and scoped to the decision-architect working directory.

Risk: The release security guidance flags persistent local decision-memory access.

Mitigation: Avoid storing sensitive third-party data, credentials, medical information, or legal facts in decision memory, and review retained records periodically.

Risk: The release security guidance notes conflicting API and network documentation.

Mitigation: Confirm the skill does not require network or API-key access before enabling it, and prefer a version with the conflicting documentation removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/decision-architect)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance, Files]

**Output Format:** [Structured decision analysis with option comparisons, framework notes, cognitive-bias signals, confidence labels, and optional local decision-memory records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain local decision-memory files for preferences, decision records, and reversals when the host agent grants file access.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter lists 2.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
