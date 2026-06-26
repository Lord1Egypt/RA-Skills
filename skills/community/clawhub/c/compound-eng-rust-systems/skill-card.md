## Description: <br>
Rust patterns for CLI tools, backend services, and general application code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for Rust application work, including Cargo workspaces, CLI tools, axum/tokio services, async concurrency, testing, observability, CI, and production resilience patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backend examples may be mistaken for production-ready code without project-specific review. <br>
Mitigation: Review generated service patterns before production use, especially internal error handling and CORS configuration for authenticated services. <br>
Risk: The skill discusses systems that may require credentials or secrets in real projects. <br>
Mitigation: Keep credentials in the user's environment or secret manager and do not store them in skill files or generated examples. <br>


## Reference(s): <br>
- [Rust CLI Tools](references/cli-tools.md) <br>
- [Axum HTTP Services](references/axum-service.md) <br>
- [Build Profiles](references/build-profiles.md) <br>
- [Rust CI Pipeline](references/ci-pipeline.md) <br>
- [Observability for Rust Services](references/observability.md) <br>
- [Production Resilience](references/production-resilience.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline Rust, TOML, YAML, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory implementation patterns for agent responses; it does not execute code.] <br>

## Skill Version(s): <br>
4.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
