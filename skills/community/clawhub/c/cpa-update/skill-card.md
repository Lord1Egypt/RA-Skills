## Description: <br>
Provides a safe Docker maintenance workflow for updating CLI Proxy API deployments while preserving configuration and authentication data with backup, testing, production deployment, and rollback steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JOJO587](https://clawhub.ai/user/JOJO587) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to plan and execute CLI Proxy API Docker image upgrades, configuration changes, validation, and rollback while preserving auth and config state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running maintenance commands against the wrong container, image, port, or mounted path could disrupt a CPA deployment. <br>
Mitigation: Verify the target container, image, ports, and mounted paths before executing commands, and test changes on an alternate port before production deployment. <br>
Risk: Configuration, API keys, OAuth material, or auth backups could be exposed through logs, pasted commands, or retained backup files. <br>
Mitigation: Avoid pasting or logging real API keys unnecessarily, preserve only required auth/config backups, and secure or prune backups when they are no longer needed. <br>
Risk: Using a moving Docker image tag can introduce unreviewed changes during future maintenance. <br>
Mitigation: After validation, prefer a pinned Docker image tag or digest for production use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JOJO587/cpa-update) <br>
- [CLI Proxy API Docker Hub repository](https://hub.docker.com/r/eceasy/cli-proxy-api) <br>
- [CLI Proxy API GitHub repository](https://github.com/router-for-me/Cli-Proxy-API) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash and Dockerfile code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes confirmation gates, backup steps, validation checks, and rollback guidance for Docker-based CPA maintenance.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release metadata and README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
