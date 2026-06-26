## Description: <br>
GateCrash Forms helps agents generate self-hosted HTML forms from JSON schemas, configure SMTP-backed notifications, serve forms locally, and initialize form-response storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Phoenix2479](https://clawhub.ai/user/Phoenix2479) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, site owners, and agent operators use this skill to create contact forms, feedback forms, event registrations, surveys, and lead-capture forms without relying on a hosted form service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Global npm installation can execute third-party package code and alter the user's environment. <br>
Mitigation: Review the package source and version before installation, and prefer an isolated or low-privilege environment for agent execution. <br>
Risk: SMTP passwords entered in agent-visible commands may be exposed in chat logs, shell history, or process metadata. <br>
Mitigation: Use a dedicated low-privilege SMTP account or app password and avoid pasting real credentials directly into agent-visible commands. <br>
Risk: Locally stored form responses can contain personal or sensitive data. <br>
Mitigation: Protect response directories with appropriate filesystem permissions, retention rules, and deployment access controls. <br>
Risk: Serving generated forms beyond localhost can expose collection endpoints and stored responses if deployment is not hardened. <br>
Mitigation: Verify network exposure, TLS, authentication, and storage protections before publishing the server outside localhost. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Phoenix2479/gatecrash-forms) <br>
- [npm package](https://www.npmjs.com/package/gatecrash-forms) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON form schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local HTML form files, response-storage paths, and SMTP configuration steps.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
