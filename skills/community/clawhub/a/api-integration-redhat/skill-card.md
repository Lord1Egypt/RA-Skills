## Description:

Integrate third-party APIs with auth, retries, timeouts, and logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build reusable REST or WebSocket API clients with explicit authentication, bounded retries, timeouts, normalized errors, logging, and tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated API clients may mishandle secrets, timeouts, retry bounds, or logging for authenticated third-party APIs.

Mitigation: Review generated clients for configured secret sources, explicit timeouts, bounded retry policy, and log redaction before use.

Risk: Malformed trigger metadata may affect installation or runtime behavior.

Mitigation: Correct the trigger metadata before release or deployment; treat the artifact as non-executable guidance until metadata is fixed.

## Reference(s):

- [API integration skill documentation](artifact/api-integration.md)
- [ClawHub skill page](https://clawhub.ai/mzfshark/skills/api-integration-redhat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with code and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces client module paths, config/env contracts, usage examples, and test guidance.]

## Skill Version(s):

1.0.0 (source: server release and skill.yml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
