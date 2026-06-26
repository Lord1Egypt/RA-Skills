## Description: <br>
Manages Docker container status reports, log analysis, and controlled restarts through docker-socket-proxy with whitelist-based safeguards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elston](https://clawhub.ai/user/elston) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check container health, inspect recent logs, summarize resource usage, and restart explicitly whitelisted Docker containers through docker-socket-proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Docker access can affect running services if container scope or restart permission is too broad. <br>
Mitigation: Keep the whitelist minimal, configure docker-socket-proxy with least privilege, and set can_restart only for services where disruption is acceptable. <br>
Risk: Container logs may include secrets or credentials. <br>
Mitigation: Sanitize log excerpts before displaying or sharing them, and review output for tokens, passwords, connection strings, and authorization headers. <br>
Risk: Repeated restarts can interrupt service availability. <br>
Mitigation: Require an explicit restart request, enforce the per-container cooldown, emit an audit line, and verify container status after restart. <br>


## Reference(s): <br>
- [Docker Commands Reference](references/docker-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and structured status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Docker command execution is constrained to whitelisted container names, capped log windows, and timeout-wrapped operations.] <br>

## Skill Version(s): <br>
0.4.0 (source: server evidence and changelog, released 2026-03-20) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
