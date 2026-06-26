## Description: <br>
Orchestration skill for the codai-dev local environment. Routes user commands to the right plugin (proxy-manager, mysql-manager, postgres-manager, redis-manager, worktree-manager). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pereirajair](https://clawhub.ai/user/pereirajair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Codai to route local codai-dev environment requests to the right helper for proxy, MySQL, PostgreSQL, Redis, and worktree operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local environment actions can change Docker services and supporting infrastructure. <br>
Mitigation: Use explicit start, stop, and status commands and review the planned action before execution. <br>
Risk: Database operations such as dump or flush can alter local development data. <br>
Mitigation: Confirm the source and target database names before running database-changing commands. <br>
Risk: Worktree removal can delete containers, databases, git worktrees, branches, and environment files. <br>
Mitigation: Require an explicit confirmation prompt before any worktree removal action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pereirajair/codai) <br>
- [Publisher profile](https://clawhub.ai/user/pereirajair) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes requests to local helper scripts; generated guidance can affect Docker services, databases, and worktrees.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
