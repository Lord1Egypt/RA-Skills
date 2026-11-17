## Description:

Ai Act Risk Check provides a preliminary classification of an AI system as high-risk or low-risk against EU AI Act Annex III categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluesbell](https://clawhub.ai/user/bluesbell)

### License/Terms of Use:


## Use Case:

Developers, auditors, and compliance reviewers use this skill for an initial screen of whether a described AI system may fall under EU AI Act Annex III high-risk categories. Its output is a rough aid for triage and should not be used as the sole basis for legal or compliance decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's output may be mistaken for legal or compliance advice.

Mitigation: Use it only as a preliminary screening aid and have qualified reviewers confirm any AI Act classification before relying on it.

Risk: User-provided system descriptions may be processed by the Gemini CLI or provider configured in the user's environment.

Mitigation: Avoid entering confidential or regulated details unless that processing path is acceptable for the user's organization.

Risk: The artifact under-discloses the actual LLM dependency and privacy boundary.

Mitigation: Review the dependency and data-handling behavior before installing or using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bluesbell/skills/ai-act-risk-check)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text classification with a short disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill returns HIGH-RISK with category numbers or LOW-RISK for systems not listed in Annex III.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
