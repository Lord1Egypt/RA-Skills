## Description:

Contract Risk Helper scans Chinese or English contract text for common risky clauses, classifies severity, and suggests negotiation or revision points for preliminary risk spotting only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to perform local, preliminary contract-risk spotting on Chinese or English contract text before seeking formal legal review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake preliminary contract risk spotting for legal advice.

Mitigation: Treat outputs as common-pattern flags only and consult a qualified lawyer for important contracts, full factual review, and current local rules.

Risk: General contract-review prompts may invoke this skill.

Mitigation: Confirm that contract-risk scanning is intended before relying on the result, especially when handling sensitive contract text.

## Reference(s):

- [Common Contract Risk Patterns](references/common-risks.md)
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/contract-risk-helper)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Bilingual Markdown report with severity-grouped findings, clause categories, and suggested negotiation or revision points]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a result string and summary counts for total, critical, warning, and advisory findings]

## Skill Version(s):

1.2.0 (source: skill.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
