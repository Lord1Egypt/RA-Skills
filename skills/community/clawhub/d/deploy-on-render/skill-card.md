## Description: <br>
Deploy and operate apps on Render by helping agents create or edit render.yaml Blueprints, generate Dashboard deeplinks, trigger or verify deployments through the Render API when RENDER_API_KEY is available, use Render MCP through mcporter, and configure services, databases, environment variables, health checks, scaling, previews, and projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ojusave](https://clawhub.ai/user/ojusave) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to prepare and operate Render deployments for web apps, static sites, workers, cron jobs, Postgres databases, and Key Value services. It helps agents analyze a codebase, produce deployment configuration, validate Render Blueprints, and guide deployment or verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help create, update, or redeploy live Render cloud resources when API credentials, MCP access, deploy hooks, or pushed Blueprint changes are available. <br>
Mitigation: Require explicit confirmation of the target workspace, repository, branch, service names, plans, regions, expected costs, and rollback path before any resource creation, redeploy, deploy-hook call, MCP action, git push, or API action. <br>
Risk: Render API keys, deploy hooks, and application secrets could be exposed if printed, committed, or written directly into render.yaml. <br>
Mitigation: Use temporary or scoped credentials where possible, keep RENDER_API_KEY out of logs and committed files, and store secrets as Render-managed values such as service-level sync:false environment variables. <br>
Risk: Incorrect Blueprint values can create failed deployments or misconfigured services. <br>
Mitigation: Validate render.yaml with the Render CLI or Validate Blueprint API before deployment, and review generated service types, runtimes, health checks, environment variables, database references, and Key Value configuration. <br>


## Reference(s): <br>
- [Render Skill](SKILL.md) <br>
- [Render Documentation](https://render.com/docs) <br>
- [Render Blueprint Quick Reference](references/blueprint-spec.md) <br>
- [Codebase Analysis](references/codebase-analysis.md) <br>
- [Direct API Deployment](references/rest-api-deployment.md) <br>
- [Render MCP Server](references/mcp-integration.md) <br>
- [Post-deploy Checks](references/post-deploy-checks.md) <br>
- [Basic Troubleshooting](references/troubleshooting-basics.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Render Blueprint examples, API call examples, deployment checklists, and troubleshooting steps.] <br>

## Skill Version(s): <br>
3.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
