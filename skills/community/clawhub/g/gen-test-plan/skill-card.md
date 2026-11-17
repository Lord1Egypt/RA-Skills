## Description:

Analyze repo, detect stack, trace changes to user-facing entry points, generate E2E YAML test plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to analyze repository changes, identify user-facing entry points, and generate an executable end-to-end YAML test plan for autonomous QA execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated E2E plans may include commands that start services, mutate databases, or save screenshots.

Mitigation: Review the generated plan before execution and run it in a disposable or test environment.

Risk: Generated test steps could accidentally duplicate existing automated test suites instead of exercising user-facing behavior.

Mitigation: Use the skill's hard gates to scan run steps and service commands for test-runner invocations before accepting the plan.

## Reference(s):

- [Stack Discovery Reference](references/stack-discovery.md)
- [Test Case Generation Reference](references/test-case-generation.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [YAML test plan plus Markdown summary with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates docs/testing/test-plan.yaml and includes validation gates for YAML structure, no automated-test duplication, and behavioral coverage.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
