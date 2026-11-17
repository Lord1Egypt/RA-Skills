## Description:

Test Temporal workflows with pytest, time-skipping, mocked activities, replay testing, and local development setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement and debug Temporal Python workflow tests across unit, integration, replay, local development, and CI scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Replay testing examples may encourage exporting production workflow histories into local or CI environments.

Mitigation: Use sanitized or synthetic histories where possible, require explicit approval before exporting production histories, and prevent history files from entering logs, caches, or build artifacts.

Risk: Local setup examples include credentials, services, dependency images, and destructive reset commands.

Mitigation: Restrict credentials, pin dependencies and container images, bind services to localhost, and treat docker-compose down -v as a destructive operation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wu-uk/skills/fix-build-agentops-temporal-python-testing)
- [Temporal Python SDK Testing Suite](https://docs.temporal.io/develop/python/testing-suite)
- [Temporal Testing Patterns](https://github.com/temporalio/temporal/blob/main/docs/development/testing.md)
- [Temporal Python Samples](https://github.com/temporalio/samples-python)
- [Unit Testing Resource](artifact/resources/unit-testing.md)
- [Integration Testing Resource](artifact/resources/integration-testing.md)
- [Replay Testing Resource](artifact/resources/replay-testing.md)
- [Local Setup Resource](artifact/resources/local-setup.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python, YAML, INI, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; examples require adaptation to the user's Temporal workflows and environment.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
