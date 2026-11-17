## Description:

Generate deterministic unit/integration tests for critical behaviors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate focused unit, integration, or end-to-end tests for features, bug fixes, and characterization before refactoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports a metadata trigger issue that could cause activation outside explicit test-generation requests.

Mitigation: Verify or fix trigger metadata before broad use so the skill activates only for explicit test-generation workflows.

Risk: Generated tests can encode incorrect assumptions or unstable dependencies.

Mitigation: Review generated tests before committing them and keep time, network, credentials, and external services deterministic or mocked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzfshark/skills/axodus-test-generator)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, guidance]

**Output Format:** [Markdown with generated test code, run instructions, and fixture or mocking notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deterministic test artifacts and review notes; avoids real credentials or real external services by default.]

## Skill Version(s):

1.0.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
