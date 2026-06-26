## Description: <br>
Deploy applications, static sites, and edge functions to Azion using Azion CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[askrauthein](https://clawhub.ai/user/askrauthein) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to prepare, check, and run Azion CLI deployment flows for applications, static sites, and edge functions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish real projects to Azion targets. <br>
Mitigation: Use it only when deployment to Azion is intended, confirm the project directory and account, and verify the target before quickstart or automated deploy flows. <br>
Risk: Deployment tokens or environment files may expose access if handled carelessly. <br>
Mitigation: Use least-privileged, well-protected Azion tokens and keep .env files out of version control. <br>
Risk: Azion CLI installation steps may involve remote install scripts. <br>
Mitigation: Verify official Azion CLI installation methods before running remote install scripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/askrauthein/azion-deploy) <br>
- [Azion CLI Reference](references/azion-cli.md) <br>
- [Azion Build and Frameworks](references/azion-build-frameworks.md) <br>
- [Azion CLI overview](https://www.azion.com/pt-br/documentacao/produtos/azion-cli/visao-geral/) <br>
- [Azion deploy command](https://www.azion.com/pt-br/documentacao/produtos/azion-cli/comandos/deploy/) <br>
- [Azion framework-specific build guidance](https://www.azion.com/pt-br/documentacao/produtos/build/develop-with-azion/frameworks-specific/visao-geral/) <br>
- [Azion create an application guide](https://www.azion.com/pt-br/documentacao/produtos/guias/build/criar-uma-aplicacao/) <br>
- [Azion API v4 migration check](https://www.azion.com/pt-br/documentacao/produtos/guias/verifique-a-migracao-da-sua-conta-para-api-v4/) <br>
- [Azion workload main settings](https://www.azion.com/en/documentation/products/build/workload/workload-main-settings/) <br>
- [Azion workload deployments](https://www.azion.com/en/documentation/products/build/workload/deployments/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Azion CLI preflight, authentication, quickstart, and local deployment command guidance.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
