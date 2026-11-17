## Description:

Provides agent-facing guidance and API examples for using RheumaScore's remote clinical scoring service, which claims to compute 165 clinical scores with fully homomorphic encryption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptoreumd](https://clawhub.ai/user/cryptoreumd)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to register for RheumaScore API access, discover supported clinical score schemas, and request individual or batch score computations. Users should verify the service's privacy, encryption, logging, retention, and compliance claims before sending real patient data or PHI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service's privacy and FHE claims conflict with examples that submit readable clinical values.

Mitigation: Treat submitted clinical values as visible to the remote provider unless the publisher supplies verifiable client-side FHE encryption and an auditable protocol.

Risk: The skill targets clinical data workflows that may involve patient data or PHI.

Mitigation: Do not send real patient data or PHI without confirming legal agreements, retention and logging behavior, compliance claims, and data-minimization controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cryptoreumd/skills/fhe-service)
- [Publisher profile](https://clawhub.ai/user/cryptoreumd)
- [RheumaScore website](https://rheumascore.xyz)
- [RheumaScore FHE API base URL](https://rheumascore.xyz/fhe/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API registration, authorization, score schema lookup, single-score computation, batch computation, pricing, health check, and error-handling guidance.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
