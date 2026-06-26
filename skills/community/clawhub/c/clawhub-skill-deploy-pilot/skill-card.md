## Description: <br>
Provides deployment automation guidance and scripts for Docker Compose stacks, with documented LXC, approval, rollback, and history features that should be verified before production use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariusfit](https://clawhub.ai/user/mariusfit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to configure, run, and review container deployment workflows for Docker Compose stacks and related health checks. Teams should verify or add the advertised approval, rollback, blue-green, LXC, cron, and history controls before relying on them for production change management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises approval, rollback, blue-green, LXC, cron, and history controls that are incomplete or missing in the artifact. <br>
Mitigation: Verify the implemented behavior and add the required controls before relying on those features for production deployments. <br>
Risk: The artifact can run high-impact Docker, SSH, Proxmox, and shell-hook commands. <br>
Mitigation: Run it with the least Docker, SSH, and Proxmox privileges needed, and review commands and hooks before execution. <br>
Risk: Stack definitions, health checks, and hooks are effectively trusted code. <br>
Mitigation: Limit who can modify deployment configuration and review stack files, health checks, and hook scripts before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mariusfit/clawhub-skill-deploy-pilot) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Artifact package metadata](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe or invoke Docker, SSH, Proxmox, and shell-hook workflows; outputs should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
