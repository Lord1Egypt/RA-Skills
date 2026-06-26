## Description: <br>
Test Temporal workflows with pytest, time-skipping, and mocking strategies. Covers unit testing, integration testing, replay testing, and local development setup. Use when implementing Temporal workflow tests or debugging test failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design and debug Temporal Python workflow tests, including time-skipping unit tests, mocked integration tests, replay determinism checks, and local pytest setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Replay testing can expose sensitive production workflow histories when histories are exported into local files or CI artifacts. <br>
Mitigation: Use sanitized or non-production histories where possible; export production histories only with explicit authorization, least-privilege read-only access, redaction or minimization, protected storage, short retention, and controls that prevent raw histories from being committed or uploaded as CI artifacts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wu-uk/fix-build-agentops-temporal-python-testing) <br>
- [Temporal Python SDK Testing](https://docs.temporal.io/develop/python/testing-suite) <br>
- [Temporal Testing Patterns](https://github.com/temporalio/temporal/blob/main/docs/development/testing.md) <br>
- [Temporal Python Samples](https://github.com/temporalio/samples-python) <br>
- [Unit Testing Resource](resources/unit-testing.md) <br>
- [Integration Testing Resource](resources/integration-testing.md) <br>
- [Replay Testing Resource](resources/replay-testing.md) <br>
- [Local Development Resource](resources/local-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python, YAML, INI, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes progressive disclosure resources for unit, integration, replay, and local setup workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
