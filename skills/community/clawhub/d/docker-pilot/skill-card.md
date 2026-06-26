## Description: <br>
Safe, intelligent Docker container management for fleet status, lifecycle operations, cleanup, Compose stacks, troubleshooting, and security hardening with READ, RISKY, and DESTRUCTIVE command gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wahajahmed010](https://clawhub.ai/user/wahajahmed010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Docker fleets, plan container lifecycle actions, manage cleanup and Compose workflows, and troubleshoot Docker issues while preserving explicit approval gates for risky or destructive commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad persistent changes to containers or host Docker configuration may affect more services than intended. <br>
Mitigation: Require the agent to list affected containers and obtain explicit approval before package installs, restart-policy changes, cleanup, daemon.json edits, Compose down actions, or monitoring jobs. <br>
Risk: Cleanup and volume operations can remove data or disrupt running services. <br>
Mitigation: Audit current Docker state first, show the exact impact, inspect volumes before removal, and require explicit confirmation before destructive commands. <br>


## Reference(s): <br>
- [Docker Pilot on ClawHub](https://clawhub.ai/wahajahmed010/docker-pilot) <br>
- [Publisher Profile](https://clawhub.ai/user/wahajahmed010) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [services.yaml](artifact/services.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Docker actions are classified as READ, RISKY, or DESTRUCTIVE and should include impact summaries and confirmations before state-changing commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
