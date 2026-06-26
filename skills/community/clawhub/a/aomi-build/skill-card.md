## Description: <br>
Builds, scaffolds, and updates Aomi apps and plugins from API docs, OpenAPI or Swagger specs, SDK docs, repository examples, endpoint notes, runtime interfaces, or product requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ceciliaz030](https://clawhub.ai/user/ceciliaz030) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert product APIs, runtime interfaces, SDK documentation, and repository examples into Aomi SDK app/plugin code, tool schemas, preambles, host interop flows, and validation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read project specs, SDK examples, and repository files while helping generate or update app code. <br>
Mitigation: Install it only in workspaces where that repository access is acceptable. <br>
Risk: Generated Aomi apps or patches may be incorrect, incomplete, or unsafe to run without review. <br>
Mitigation: Review generated apps, validation output, and any modified files before running or deploying them. <br>
Risk: Some integrations may require wallet access, API keys, or other sensitive credentials. <br>
Mitigation: Provide credentials only when a specific integration requires them, and prefer limited-scope credentials. <br>


## Reference(s): <br>
- [Aomi SDK Patterns](references/aomi-sdk-patterns.md) <br>
- [Spec To Tools](references/spec-to-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code, file edits, configuration details, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Aomi SDK crates, tool schemas, preambles, host interop flows, validation plans, and focused tests.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
