## Description: <br>
Distributed mesh infrastructure operations - the unified remix of Docker, Git, GCP, Linux, SSH, systemd, cron, network, security, DevOps, infrastructure, and backup guidance into one reference for multi-node AI gateway meshes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill as a runbook for managing, debugging, securing, and recovering distributed OpenClaw gateway nodes across Docker, Linux, cloud, SSH, networking, scheduling, and backup workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Operational commands and configuration snippets can change running services, cloud resources, firewall rules, or access controls if executed without review. <br>
Mitigation: Review proposed commands against the target environment, run read-only diagnostics first, and require operator approval before restart, cleanup, firewall, IAM, or secret-access actions. <br>
Risk: The artifact includes concrete infrastructure details and an auth-like value in operational notes. <br>
Mitigation: Treat those details as examples or private deployment data, replace them before reuse, and avoid publishing or executing them outside the intended environment. <br>
Risk: The security evidence reports a clean result but notes that the available telemetry was not a full source-backed audit. <br>
Mitigation: Before installation, review the skill artifact and install metadata for expected commands, network access, credential handling, and persistence behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evezart/evez-mesh-ops) <br>
- [Publisher homepage](https://github.com/EvezArt) <br>
- [Node lifecycle reference](artifact/nodes.md) <br>
- [Mesh operations reference](artifact/mesh.md) <br>
- [Security and hardening reference](artifact/security.md) <br>
- [Incident response reference](artifact/incidents.md) <br>
- [Commands cheatsheet](artifact/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent responses may include operational checklists, diagnostic commands, service templates, hardening steps, and incident-response actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
