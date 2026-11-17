## Description:

Generate ServerRequest tests using VaporTesting with typed request and response validation for Show, Create, Update, and Delete operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foscomputerservices](https://clawhub.ai/user/foscomputerservices)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to generate Swift/VaporTesting test suites for FOSMVVM ServerRequest implementations. It helps cover CRUD paths, typed response and error validation, localization checks, route setup, and isolated test fixtures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated create, update, and delete tests can mutate data if pointed at a real application environment.

Mitigation: Review generated tests before running them and use isolated test fixtures or test databases.

Risk: The guidance is specific to FOSMVVM and VaporTesting conventions.

Mitigation: Install and use it only in projects that follow the FOSMVVM/VaporTesting ServerRequest patterns.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/foscomputerservices/skills/fosmvvm-serverrequest-test-generator)
- [Skill definition](artifact/SKILL.md)
- [Reference templates](artifact/reference.md)

## Skill Output:

**Output Type(s):** [code, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with Swift test code blocks and optional YAML fixture templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated tests should be reviewed before execution and should target isolated test fixtures or test databases.]

## Skill Version(s):

2.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
