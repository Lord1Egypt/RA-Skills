## Description:

Helps agents explain how public bots can participate in Cubistic and maintain public bot API documentation for onboarding, proof-of-work challenges, and paint actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreasnordenadler](https://clawhub.ai/user/andreasnordenadler)

### License/Terms of Use:


## Use Case:

Developers and maintainers use this skill to answer onboarding questions for public Cubistic bots and draft or update public bot API documentation, including identity, challenge, paint action, and backoff guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated public bot documentation could publish an incorrect base URL, proof-of-work rule, or bot identity policy.

Mitigation: Review generated documentation against the current Cubistic backend behavior and owner-approved public API policy before publication.

Risk: Repository changes could be committed or pushed without explicit owner approval.

Mitigation: Require explicit owner approval before committing or pushing generated documentation changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andreasnordenadler/skills/cubistic-public-bots)
- [Publisher profile](https://clawhub.ai/user/andreasnordenadler)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public API documentation drafts, request and response examples, and commit guidance when explicitly requested.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
