## Description: <br>
Verifies API implementations against OpenAPI specifications using the Drift CLI, catching spec drift and supporting Bi-Directional Contract Testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinrvaz](https://clawhub.ai/user/kevinrvaz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to write, run, and debug Drift tests for API contract conformance, endpoint coverage, and spec drift detection against OpenAPI specifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live API verification can exercise state-changing POST, PUT, PATCH, or DELETE operations. <br>
Mitigation: Prefer mock or staging APIs, use disposable test data, and avoid production write or delete runs unless explicitly reviewed. <br>
Risk: Drift tests and publishing flows may require sensitive API or PactFlow credentials. <br>
Mitigation: Use least-privilege test tokens, keep secrets in environment variables or CI secret stores, and avoid embedding credentials in generated files. <br>
Risk: Generated tests, hooks, and feedback loops can repeat incorrect or destructive behavior if accepted without review. <br>
Mitigation: Review generated Drift YAML and Lua hooks before running loops, especially setup and cleanup code for stateful endpoints. <br>
Risk: Helper scripts may install or invoke external tools such as Drift, Prism, uv, npm packages, or PactFlow bundles. <br>
Mitigation: Pin or preinstall tools where possible, inspect bundles before publishing, and run commands in controlled development or CI environments. <br>


## Reference(s): <br>
- [Drift Test Cases Reference](references/test-cases.md) <br>
- [Drift Authentication Reference](references/auth.md) <br>
- [Local Testing with a Mock Server](references/mock-server.md) <br>
- [Drift Lua API Reference](references/lua-api.md) <br>
- [Drift CLI Reference](references/cli-reference.md) <br>
- [PactFlow Integration and CI/CD](references/pactflow-and-cicd.md) <br>
- [Drift Documentation](https://pactflow.github.io/drift-docs/) <br>
- [Drift Test Case Schema](https://download.pactflow.io/drift/schemas/drift.testcases.v1.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with YAML, Lua, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or review Drift test files, helper scripts, coverage reports, and command sequences for local or CI execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
