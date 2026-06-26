## Description: <br>
Cognitive Brain Deploy helps OpenClaw users deploy a Cognitive Brain semantic memory stack with PostgreSQL, pgvector, Redis, scheduled jobs, hooks, and setup guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare an OpenClaw semantic memory deployment, including local services, database schema, configuration, scheduled maintenance jobs, and hook activation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment script installs packages, enables services, edits database state, and creates persistent cron jobs on the host. <br>
Mitigation: Review the script before execution, run it only on an intended host, inspect existing crontab entries first, and confirm PostgreSQL, Redis, cron, and OpenClaw hook persistence are acceptable. <br>
Risk: The deployment materials include a default database password and can overwrite Cognitive Brain configuration. <br>
Mitigation: Use a unique database password, update config.json consistently, and avoid reusing the documented default credential outside a disposable test environment. <br>
Risk: Troubleshooting steps can affect stored memory data, including table rebuilds. <br>
Mitigation: Back up memory data before running SQL repair or reset steps. <br>
Risk: The Cognitive Brain repository is referenced as a manual clone target before npm install and hook setup. <br>
Mitigation: Verify the repository source and review its package and hook contents before installing dependencies or enabling hooks. <br>


## Reference(s): <br>
- [Cognitive Brain Deploy release page](https://clawhub.ai/hongjiahao371-pixel/cognitive-brain-deploy) <br>
- [Deployment guide](references/deploy-guide.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, SQL, JSON, and crontab snippets plus a deployment shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Execution guidance can make persistent local system changes when the deployment script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
