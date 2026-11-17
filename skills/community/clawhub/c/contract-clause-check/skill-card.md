## Description:

Screens Chinese-language contract text for missing breach, dispute, and jurisdiction terms and flags potentially risky clauses for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

People reviewing draft contracts use this skill for a preliminary check of missing clauses and potentially risky language before seeking legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published instructions describe an --input option, but the script requires --text.

Mitigation: Use --text to pass contract text and check --help before running; ask the publisher to correct the instructions.

Risk: Declared Write and WebFetch access is broader than needed for a local contract-text check.

Mitigation: Limit access to the supplied contract text and avoid granting unnecessary write or network permissions.

Risk: Keyword-based screening can miss legal issues or suggest unwarranted confidence in a contract.

Mitigation: Treat findings as preliminary and have important contracts reviewed by a qualified lawyer.

## Reference(s):

- [Contract Clause Check on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/contract-clause-check)
- [LGD governance theory (background)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain-text checklist or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports missing terms and risky phrases; missing terms cause FAIL, but risky phrases alone do not.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; bundled frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
