## Description:

App Maker helps agents transform natural-language application requirements into full-stack project plans, generated code, configuration, debugging guidance, and deployment steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chall2015](https://clawhub.ai/user/chall2015)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to accelerate full-stack application creation from requirements analysis through UI design, database modeling, code generation, visual debugging, and deployment preparation. It is suited for rapid prototyping, MVP development, and repetitive application scaffolding tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API keys for multiple external model providers.

Mitigation: Use environment variables or a secret manager instead of plaintext keys, and never publish screenshots or generated files containing real credentials.

Risk: The skill can generate files, package manifests, dependency commands, and deployment steps that may affect a local system or cloud account.

Mitigation: Run generation in an isolated project directory, inspect generated files and package manifests before installing dependencies, and confirm deployment target, costs, and public exposure before deployment.

Risk: The security verdict is suspicious because safeguards around external model calls, package execution, deployment, and generated file writes are weak.

Mitigation: Review the skill before installation, pin and verify package commands, scan generated code, and deploy only after human review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chall2015/skills/app-maker)
- [Publisher profile](https://clawhub.ai/user/chall2015)
- [README](artifact/README.md)
- [Quickstart](artifact/QUICKSTART.md)
- [Configuration example](artifact/config.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and generated project files with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce application source files, tests, deployment configuration, preview/debug guidance, and model configuration instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
