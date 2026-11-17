## Description:

Predicts anti-drug antibody risk for selected biologic therapies from patient clinical, pharmacogenomic, and treatment variables and returns a risk score, tier, and monitoring recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptoreumd](https://clawhub.ai/user/cryptoreumd)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical informatics users, healthcare developers, and reviewing clinicians can use this skill to run an informational ADA risk stratification workflow for biologic therapy scenarios. It produces risk scores, tiers, therapeutic drug monitoring timing, and recommendation text for qualified clinician review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides patient-specific treatment and monitoring recommendations without clear clinical safety limits.

Mitigation: Treat outputs as informational only, not medical advice or validated decision support; require qualified clinician review and local validation before patient-specific use.

Risk: The local predictor may be exposed through an API or agent workflow that runs sensitivity analysis over clinical inputs.

Mitigation: Use bounded runtime controls and review deployment controls before integrating it into any clinical workflow.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cryptoreumd/skills/ada-predictor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python code and command-line usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces patient-level ADA probability, 0-100 risk score, risk tier, recommended TDM interval, recommendation text, and Monte Carlo sensitivity statistics.]

## Skill Version(s):

1.0.0 (source: server release evidence, created 2026-03-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
