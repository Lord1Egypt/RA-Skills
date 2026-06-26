## Description: <br>
Deploy applications and set up infrastructure, including CI/CD, Docker, hosting, domains, SSL, monitoring, environment variables, staging, production, rollback, and related deployment work for solo founders without a dedicated ops team. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emersonbraun](https://clawhub.ai/user/emersonbraun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and solo founders use this skill to plan and execute practical web application deployments, CI/CD pipelines, environment management, monitoring, rollbacks, and platform choices without a dedicated operations team. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment commands can affect cloud resources, production services, costs, or data availability if applied to the wrong account, project, environment, or region. <br>
Mitigation: Review every command before execution and confirm the target account, project, environment, region, and cost impact before creating resources, scaling services, rolling back deployments, or deleting backups. <br>
Risk: Secrets or credentials could be exposed if pasted into chat, committed to source control, or baked into Docker images. <br>
Mitigation: Use provider secret-management interfaces, keep .env files out of git, commit only placeholder .env.example values, and avoid placing secrets in container images. <br>
Risk: Backup and rollback examples can cause data loss or downtime if used without validation. <br>
Mitigation: Test restores in a non-production database, verify health checks, and review rollback steps against the specific deployment platform before production use. <br>


## Reference(s): <br>
- [Deployment Guides Reference](references/deployment-guides.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/emersonbraun/eb-devops-deploy) <br>
- [Publisher Profile](https://clawhub.ai/user/emersonbraun) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include deployment plans, CI/CD snippets, Dockerfiles, environment variable guidance, rollback steps, and platform recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
