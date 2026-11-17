## Description:

Deploy applications, static sites, and edge functions to Azion using Azion CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[askrauthein](https://clawhub.ai/user/askrauthein)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run Azion CLI preflight, authentication, project linking, build, and local deployment flows for applications, static sites, and edge functions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer commands shown in the skill documentation can pipe downloaded scripts directly into a shell.

Mitigation: Review installer scripts before execution and prefer a trusted package or verified installation method when available.

Risk: Token-based examples can expose deployment credentials through shell history, process listings, logs, or sourced environment files.

Mitigation: Use secure secret injection or an authenticated CLI session, avoid literal token arguments, and grant Azion tokens only the minimum deployment permissions needed.

Risk: The security scan verdict is suspicious because the skill contains deployment automation with risky setup and token-handling patterns.

Mitigation: Review and harden the Azion setup steps before installing or running the skill in a production environment.

## Reference(s):

- [Azion CLI Reference](references/azion-cli.md)
- [Azion Build and Frameworks](references/azion-build-frameworks.md)
- [Azion CLI Overview](https://www.azion.com/pt-br/documentacao/produtos/azion-cli/visao-geral/)
- [Azion Deploy Command](https://www.azion.com/pt-br/documentacao/produtos/azion-cli/comandos/deploy/)
- [Azion Build Frameworks](https://www.azion.com/pt-br/documentacao/produtos/build/develop-with-azion/frameworks-specific/visao-geral/)
- [Azion Create Application Guide](https://www.azion.com/pt-br/documentacao/produtos/guias/build/criar-uma-aplicacao/)
- [Azion API v4 Migration Check](https://www.azion.com/pt-br/documentacao/produtos/guias/verifique-a-migracao-da-sua-conta-para-api-v4/)
- [Azion Workload Main Settings](https://www.azion.com/en/documentation/products/build/workload/workload-main-settings/)
- [Azion Workload Deployments](https://www.azion.com/en/documentation/products/build/workload/deployments/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash and an authenticated Azion CLI session or scoped Azion token.]

## Skill Version(s):

0.1.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
