## Description: <br>
Deploy and manage Vercel projects via CLI - deploy, env, domains, logs, teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Melvynx](https://clawhub.ai/user/Melvynx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to ask an agent for Vercel CLI commands and guidance for deployments, environment variables, domains, projects, logs, teams, and local development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vercel CLI commands can affect live deployments, domains, projects, teams, and environment variables. <br>
Mitigation: Before production deploys, rollbacks, removals, team switching, env pulls, or commands using --yes, verify the project, team scope, working directory, and exact target. <br>
Risk: Vercel tokens and .env.local contents can expose secrets if shared in chat or logs. <br>
Mitigation: Avoid exposing tokens or environment file contents, and prefer scoped tokens and redacted command output when an agent assists. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Melvynx/cli-vercel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and command reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends JSON output for programmatic CLI calls and may include commands that affect live Vercel resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
