## Description:

AI-powered contract review that identifies risky clauses, missing provisions, and compliance issues in legal documents for informed decision-making.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

External users and legal or commercial reviewers use this skill to screen contract text for high-risk clauses, missing standard provisions, compliance concerns, and suggested negotiation or remediation points. Its output should support, not replace, review by qualified counsel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review accuracy and risk labels can be wrong, including scoring logic and legal-risk summaries.

Mitigation: Treat results as screening output, verify important findings with qualified legal counsel, and test scoring behavior before relying on it for decisions.

Risk: Bundled helper scripts can write files or import code in unsafe ways.

Mitigation: Run the skill in a confined workspace, review scripts before execution, and limit write permissions to intended input and output directories.

Risk: Contract text may contain sensitive or confidential information.

Mitigation: Process sensitive contracts in controlled local or air-gapped environments and avoid shared paths for confidential inputs and reports.

## Reference(s):

- [Contract Review Skill on ClawHub](https://clawhub.ai/534422530/skills/contract-review-skill)
- [README](artifact/README.md)
- [High-risk clause patterns](artifact/legal_patterns/high_risk.json)
- [Required clause patterns](artifact/legal_patterns/required_clauses.json)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable contract review report or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a risk score, findings, summary counts, and remediation suggestions; batch mode can write JSON reports.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence; artifact SKILL.md reports 1.0.0 and claw.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
