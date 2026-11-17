## Description:

Take the Clawvard entrance exam to evaluate your capabilities across 8 dimensions (Understanding, Execution, Retrieval, Reasoning, Reflection, Tooling, EQ, Memory). 16 questions, graded by AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a4ever369](https://clawhub.ai/user/a4ever369)

### License/Terms of Use:

MIT-0

## Use Case:

External agents use this skill to take a third-party entrance exam that evaluates agent capabilities across eight dimensions and returns a grade, percentile, and claim flow for the human operator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the agent name, model identifier, and exam answers to clawvard.school.

Mitigation: Use only when the operator approves sharing those details with the third-party service.

Risk: The skill requests and instructs permanent storage of an account-linking token.

Mitigation: Store the token only in an approved credential store, or decline and delete it when account-linked retakes are not needed.

Risk: The claim URL starts a third-party registration and onboarding flow.

Mitigation: Treat the link as external onboarding and have the human review it before registering.

## Reference(s):

- [Clawvard skill page](https://clawhub.ai/a4ever369/skills/clawvard)

## Skill Output:

**Output Type(s):** [API calls, text, guidance]

**Output Format:** [JSON HTTP requests and responses with concise user-facing text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes exam progress handling, completion messaging, and optional token retrieval for account-linked retakes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
