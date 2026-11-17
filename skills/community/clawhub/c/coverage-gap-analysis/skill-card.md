## Description:

Maps an organisation's risks against its insurance policy portfolio to identify uncovered, underinsured, or double-covered exposures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Insurance, risk, finance, and operations teams use this skill to compare an organisation's risk register with its policy portfolio, identify uninsured or underinsured exposures, review deductible stacking, and rank remediation recommendations by expected-loss severity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may share sensitive policy, risk register, financial, operational, or management concern information with the agent while using the skill.

Mitigation: Use approved handling procedures for confidential insurance and risk data, and limit shared inputs to what the organisation is permitted to process in the agent environment.

Risk: The analysis could be mistaken for a binding coverage determination or purchase recommendation.

Mitigation: Treat outputs as analytical support and confirm policy interpretation, placement, and retention decisions with a licensed broker, adviser, or counsel.

Risk: Incomplete policy wording, exclusions, sublimits, deductibles, or risk tolerance data can lead to incorrect gap findings.

Mitigation: Mark unavailable terms as to be confirmed, collect missing source documents, and validate assumptions before using the recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/coverage-gap-analysis)
- [Skill homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/coverage-gap-analysis.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown coverage gap analysis with tables, findings, ranked recommendations, and open questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces analytical support only; placement and retention decisions should be reviewed with a licensed broker, adviser, or counsel.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
