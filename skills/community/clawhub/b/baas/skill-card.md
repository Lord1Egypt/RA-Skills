## Description: <br>
Aipexbase supports end-to-end web application, management system, and vibe-coding workflows from requirements through BaaS-backed frontend implementation and deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuafuai](https://clawhub.ai/user/kuafuai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use this skill to turn product requirements into BaaS-backed web applications, including schema design, frontend code generation, API integration, data operations, and deployment packaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or modify BaaS applications, tables, data, and frontend files using administrative credentials. <br>
Mitigation: Install only when that authority is acceptable, use a least-privilege BaaS token when possible, and review generated schema and data operations before applying them to important resources. <br>
Risk: The skill stores powerful credentials in configuration files such as baas-config.json. <br>
Mitigation: Avoid committing or deploying credential-bearing configuration files, keep admin tokens out of project artifacts, and rotate tokens if they are exposed. <br>
Risk: Generated HTML may use unsafe DOM insertion patterns. <br>
Mitigation: Review generated HTML for unsafe innerHTML usage before deployment and sanitize untrusted content. <br>
Risk: Setup instructions include host-level package installation and remote installer commands. <br>
Mitigation: Approve curl, npm global install, and sudo apt-get commands explicitly before running them in the host environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kuafuai/baas) <br>
- [AipexBase JavaScript API quick reference](artifact/references/aipexbase-js-api.md) <br>
- [Deployment guide](artifact/references/deploy.md) <br>
- [PRD template](artifact/references/prd-template.md) <br>
- [HTML template](artifact/references/html-template.html) <br>
- [Frontend style guide](artifact/references/style-guide.md) <br>
- [CodeFlying account and API key portal](https://www.codeflying.net) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and generated frontend code/files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project files, BaaS app schemas, project configuration, and deployment packages.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
