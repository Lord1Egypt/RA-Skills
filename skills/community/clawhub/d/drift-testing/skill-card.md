## Description:

Verifies API implementations against OpenAPI specifications using the Drift CLI, catching spec drift and supporting Bi-Directional Contract Testing (BDCT).

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinrvaz](https://clawhub.ai/user/kevinrvaz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API engineers use this skill to create, run, and debug Drift contract tests against OpenAPI specs, check endpoint and response-code coverage, and identify implementation/spec drift before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global or latest-version installation examples can execute unpinned packages or binaries with broad local or CI privileges.

Mitigation: Pin package and binary versions, verify checksums, and prefer project-local installs for Drift and Prism.

Risk: Contract tests can mutate APIs when pointed at live systems, especially POST and DELETE scenarios.

Mitigation: Use mock, local, or dedicated test environments unless mutation is intentional, and use least-privilege test tokens that are not printed in logs.

Risk: Copied subprocess wrappers that use shell execution can expand command-injection impact.

Mitigation: Remove shell-based subprocess execution from copied wrappers and pass arguments as structured arrays.

## Reference(s):

- [Drift Test Cases Reference](references/test-cases.md)
- [Drift Authentication Reference](references/auth.md)
- [Local Testing with a Mock Server](references/mock-server.md)
- [Drift Lua API Reference](references/lua-api.md)
- [Drift CLI Reference](references/cli-reference.md)
- [PactFlow Integration and CI/CD](references/pactflow-and-cicd.md)
- [PactFlow Drift Documentation](https://pactflow.github.io/drift-docs/)
- [Drift Test Case Schema](https://download.pactflow.io/drift/schemas/drift.testcases.v1.schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML, Lua, shell command, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run local helper scripts for OpenAPI endpoint extraction, Drift coverage checks, mock-server startup, and test rerun loops.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
