## Description: <br>
Comprehensive 1Panel server management skill for AI agents. Manage Linux servers, Docker containers, databases, websites, SSL certificates, and more through 580+ API endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EaveLuo](https://clawhub.ai/user/EaveLuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users use this skill to let an AI agent administer 1Panel-managed Linux servers, containers, websites, databases, files, monitoring, backups, and security settings through API calls and CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over a 1Panel server, including command execution, deletes, disk, SSH, firewall, backup restore, and credential-changing actions. <br>
Mitigation: Require human confirmation before high-impact actions and install only when the publisher and target server administration workflow are trusted. <br>
Risk: The skill requires a 1Panel API key, and misconfigured transport or shell profiles can expose credentials. <br>
Mitigation: Use a least-privileged API key where possible, prefer HTTPS, and avoid storing the key in broadly loaded shell profiles. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EaveLuo/1panel-skill) <br>
- [1Panel](https://1panel.cn/) <br>
- [npm package](https://www.npmjs.com/package/1panel-skill) <br>
- [Project homepage declared by skill](https://github.com/EaveLuo/1panel-skill) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration] <br>
**Output Format:** [JSON responses, TypeScript library calls, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and ONEPANEL_API_KEY; optional host, port, and protocol settings configure the target 1Panel server.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
