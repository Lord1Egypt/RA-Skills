## Description:

Converts exported Dify workflow or Chatflow YAML DSL files into deployable standalone code projects, with Python and FastAPI as the default stack and Node.js and Express as an optional stack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[somkh](https://clawhub.ai/user/somkh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn exported Dify workflow or Chatflow YAML into a standalone service while preserving workflow structure and surfacing missing credentials, knowledge-base content, and deployment choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated verifier and service templates may execute untrusted workflow code.

Mitigation: Run analysis, verification, and generated services in a sandbox and avoid processing untrusted DSLs directly on a host environment.

Risk: Generated services can expose workflow execution paths or secrets without enough deployment safeguards.

Mitigation: Add authentication, rate limits, request size limits, env and secret name allowlists, and HTTP destination allowlists before exposing the service or loading real credentials.

Risk: Generated projects may not be deployment-hardened by default.

Mitigation: Review and harden generated code, pin dependencies, and scan the project before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/somkh/skills/dify-dsl-to-code)
- [Code generation and project assembly patterns](artifact/references/codegen-patterns.md)
- [Dify workflow and Chatflow component reference](artifact/references/dsl-components.md)
- [Dify DSL node type mapping reference](artifact/references/dsl-node-types.md)
- [User interaction completion playbook](artifact/references/interaction-playbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline commands plus generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Python/FastAPI or Node.js/Express project templates, Dockerfile, tests, and .env.example placeholders.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
