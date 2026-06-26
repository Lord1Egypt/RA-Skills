## Description: <br>
Manage Neon Serverless Postgres via CLI - projects, branches, databases, roles, endpoints, connection strings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Melvynx](https://clawhub.ai/user/Melvynx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage Neon Serverless Postgres resources through neonctl, including projects, branches, databases, roles, endpoints, context, and connection strings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands may affect real Neon cloud databases when valid credentials are available. <br>
Mitigation: Use least-privilege Neon credentials and review the target project, branch, database, or role before execution. <br>
Risk: Delete and reset commands can remove or overwrite Neon resources. <br>
Mitigation: Require explicit confirmation before running destructive neonctl commands such as delete or branch reset. <br>
Risk: Connection strings and API keys are sensitive secrets. <br>
Mitigation: Treat Neon connection strings and API keys as secrets and avoid exposing them in logs, chat transcripts, or generated files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI flags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Use --output json when calling neonctl programmatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
