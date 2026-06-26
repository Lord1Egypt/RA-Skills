## Description: <br>
Manage Docker containers, stacks, templates, images, networks, volumes, users, and system resources through the Arcane Docker Management API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cougz](https://clawhub.ai/user/cougz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to get agent-generated guidance, API calls, commands, and code examples for administering an Arcane-managed Docker environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact Docker and Arcane administration actions such as exec, deploy, update, stop, restart, remove, prune, user, role, password, and API-key operations. <br>
Mitigation: Require explicit human approval before executing privileged or destructive operations, and review generated commands against the intended environment. <br>
Risk: Generated examples may involve bearer tokens, API keys, passwords, or other sensitive operational credentials. <br>
Mitigation: Use least-privilege credentials, keep secrets out of shared chats and logs, prefer environment variables or secret stores, and rotate API keys regularly. <br>
Risk: The default API endpoint in the artifact uses plain HTTP localhost, while remote or production use can expose credentials or administrative actions if transported insecurely. <br>
Mitigation: Prefer HTTPS for non-local or production access and restrict Arcane API access with appropriate network and role controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cougz/arcane-docker-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline curl, Bash, Python, JSON, and Docker Compose examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include privileged Docker and Arcane API operations that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
