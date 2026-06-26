## Description: <br>
帮助代理用 HTML、Docker、DNS 和域名配置快速部署公共网站。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and agents use this skill to prepare website files, build and push a Docker image, deploy a container to a server, and configure DNS for a public domain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish containers and change public server or DNS state without explicit approval and rollback guardrails. <br>
Mitigation: Confirm the project directory, image name, registry account, server host, ports, domain, and DNS records before execution, and prepare rollback steps for containers, pushed images, and DNS records. <br>
Risk: Deployment commands and Docker builds may expose secrets if sensitive files are present in the build context or command flow. <br>
Mitigation: Review the build context before running Docker commands and keep secrets out of website files, Docker build inputs, shell history, and deployment logs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, HTML, Dockerfile, and DNS configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deployment guidance should be reviewed before running commands against public infrastructure.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
