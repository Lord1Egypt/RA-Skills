## Description:

Guides an agent through ACMG/AMP germline small-variant review by collecting evidence, assigning criteria, checking conflicts, and producing a provisional classification summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex4xu](https://clawhub.ai/user/alex4xu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and clinical genomics reviewers use this skill to run a structured, review-oriented ACMG/AMP workflow for germline SNVs and indels. It helps normalize variant intake, track criteria evidence, identify unresolved conflicts, and draft a review-ready provisional classification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A provisional ACMG/AMP result could be mistaken for a final clinical diagnosis.

Mitigation: Present outputs as decision support only and require expert manual review before clinical use.

Risk: Identifiable patient data could be entered into an environment that is not approved for clinical or privacy-sensitive information.

Mitigation: Avoid identifiable patient data unless the deployment environment is approved for that data.

Risk: Pathogenic and benign evidence conflicts may lead to overconfident classification if not reviewed.

Mitigation: Manually review conflicting evidence and prefer VUS when conflicts remain unresolved.

## Reference(s):

- [ACMG Variant Classification SOP](references/sop.md)
- [Classifier Test Cases](references/test_cases.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance and tables, with optional JSON results from the classifier helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review-only decision support; final classification requires expert manual review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
