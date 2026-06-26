## Description: <br>
Generate deterministic unit/integration tests for critical behaviors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzfshark](https://clawhub.ai/user/mzfshark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create deterministic unit, integration, or end-to-end tests for features, bug fixes, and refactors. It guides behavior identification, boundary selection, fixture setup, test writing, and stable test execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated tests may encode incorrect assumptions or misleading coverage if accepted without review. <br>
Mitigation: Review generated tests against the intended behavior and acceptance criteria before committing them. <br>
Risk: Tests could be pointed at real credentials, production services, or live external systems if the user configures them that way. <br>
Mitigation: Run tests in development or CI environments and avoid real credentials, production services, and live external systems unless intentionally configured. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mzfshark/axodus-test-generator) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, markdown, guidance] <br>
**Output Format:** [Markdown with generated or modified test files, run instructions, and fixture or mocking notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be deterministic and reviewed before committing or running in CI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
