## Description:

Helps an agent require biometric second confirmation for sensitive operations such as pause, terminate, modify, delete, reset, or similar actions while allowing ordinary view, list, query, and export actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a second-confirmation step before sensitive actions and to return structured allow or deny outcomes for biometric verification flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the skill as an enforceable biometric gate even though the artifact does not include the biometric service it instructs the agent to run.

Mitigation: Review before installing and supply, scope, and test a real biometric verification integration before relying on the skill to protect sensitive actions.

Risk: Sensitive-operation approval depends on token generation and verification behavior that is described but not implemented in the artifact.

Mitigation: Validate the token issuer, verifier, expiration handling, and denial paths in the deployed environment before enabling sensitive operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/biometric-confirm)

## Skill Output:

**Output Type(s):** [guidance, shell commands, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sensitive actions require a token; the described token lifetime is five minutes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
