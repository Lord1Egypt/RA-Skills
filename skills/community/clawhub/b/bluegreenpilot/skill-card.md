## Description: <br>
Guide safe blue-green deployments with persistent repo config, environment state, health checks, explicit switch confirmation, and rollback discipline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluegreenpilot](https://clawhub.ai/user/bluegreenpilot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure and operate blue-green deployment workflows for applications, including deployment planning, slot verification, traffic switch confirmation, and rollback discipline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated .bluegreenpilot configuration or state files could encode an incorrect topology, active slot, rollback path, or database policy. <br>
Mitigation: Review generated .bluegreenpilot files before committing or using them for deployment decisions. <br>
Risk: Secrets could be accidentally placed in deployment config or state files. <br>
Mitigation: Keep secrets out of config/state and reference environment variables or secret managers instead. <br>
Risk: A production traffic switch or rollback could affect live users if executed from an incomplete plan or vague approval. <br>
Mitigation: Require explicit human approval with target environment, slot, release, healthcheck, and rollback details before any production switch or rollback. <br>


## Reference(s): <br>
- [BlueGreenPilot Configuration](references/configuration.md) <br>
- [Database Policy](references/database.md) <br>
- [Docker and Mixed Docker Deployments](references/docker.md) <br>
- [No-Docker, Script, Manual, and CI Deployments](references/no-docker.md) <br>
- [ClawHub skill page](https://clawhub.ai/bluegreenpilot/bluegreenpilot) <br>
- [Project homepage](https://github.com/ThiagoCAltoe/bluegreenpilot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown plans with inline shell commands and YAML configuration/state examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .bluegreenpilot config and state files through explicit commands; production switch and rollback steps require human confirmation.] <br>

## Skill Version(s): <br>
2026.6.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
