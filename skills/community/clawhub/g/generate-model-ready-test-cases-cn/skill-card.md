## Description: <br>
Generates standardized, model-ready automated test case suites as JSON so Codex can turn requirements, prototypes, API docs, user stories, defect reports, or natural-language requests into executable UI, API, end-to-end, regression, smoke, and acceptance tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deathknightorg](https://clawhub.ai/user/deathknightorg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and automated testing agents use this skill to convert Chinese requirements, prototypes, API documentation, user stories, and defect reports into structured JSON test suites. It is especially suited for model-driven automation across Web UI, API, end-to-end workflows, smoke tests, regression tests, and acceptance scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated tests may include production, payment, deletion, bulk-change, or other irreversible workflows if the input materials describe them. <br>
Mitigation: Review generated suites before execution, run them against test systems, and keep destructive or high-impact cases disabled until explicitly approved. <br>
Risk: Generated locators, requests, assertions, or assumptions may be incomplete when source requirements are incomplete or ambiguous. <br>
Mitigation: Inspect assumptions and placeholders, validate saved JSON with the bundled validator, and adjust unstable selectors or assertions before another agent executes the tests. <br>


## Reference(s): <br>
- [Test suite schema](references/test-suite-schema.md) <br>
- [Test design playbook](references/test-design-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, guidance] <br>
**Output Format:** [JSON, usually in a single json code block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured test suites with stable case IDs, step IDs, actions, assertions, assumptions, placeholders, cleanup notes, and enabled flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
