## Description: <br>
Manages the full deploy cycle - build validation, GitHub push, Vercel deployment, and health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guifav](https://clawhub.ai/user/guifav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Deploy Pilot to plan, execute, and verify Next.js deployments to Vercel through GitHub, including preview and production releases, health checks, environment-variable checks, and rollback steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can push to GitHub, trigger Vercel deployments, promote deployments, update environment variables, and manage domains, which can affect production availability. <br>
Mitigation: Use project-scoped, least-privileged Vercel credentials, run only in trusted repositories, and require manual confirmation before production pushes, deployment promotion, environment-variable updates, domain changes, or PR merges. <br>
Risk: A deployment may ship incomplete changes, failing checks, missing environment variables, or database migrations that are not backward-compatible. <br>
Mitigation: Complete the planning protocol, run pre-deploy checks, verify feature handoff files, dependencies, environment variables, and migrations, and halt when checks fail. <br>
Risk: Post-deployment failures may go unnoticed or persist if rollback is delayed. <br>
Mitigation: Perform health checks, review logs and key pages within five minutes, and use the documented rollback procedure when validation fails. <br>


## Reference(s): <br>
- [ClawHub Deploy Pilot listing](https://clawhub.ai/guifav/deploy-pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with deployment plans, checklists, command snippets, and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands for git, GitHub CLI, Vercel CLI, curl, jq, and local test/build tooling.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
