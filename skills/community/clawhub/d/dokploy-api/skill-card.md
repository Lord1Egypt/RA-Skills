## Description: <br>
Use for Dokploy-specific API operations across applications, deployments, databases, domains, backups, settings, and related Dokploy administration tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[achals-iglu](https://clawhub.ai/user/achals-iglu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage Dokploy resources through the Dokploy API. It supports module-routed workflows for applications, deployments, databases, domains, backups, settings, and platform administration while requiring inspect-first and verify-after handling for mutations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad administrator-level access to a Dokploy instance, including identity, billing, credential, SSH key, server, schedule, delete, restart, and infrastructure controls. <br>
Mitigation: Install only for agents that need Dokploy administration, use a narrowly scoped or revocable API key where possible, and require explicit confirmation for high-impact operations. <br>
Risk: The artifact includes a default third-party Dokploy API server URL. <br>
Mitigation: Confirm the API base URL points to the intended Dokploy server before use. <br>
Risk: API keys or tokens could be exposed through commands, logs, or summaries. <br>
Mitigation: Store credentials in environment or secure configuration, redact secrets in output, and avoid inline literal tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/achals-iglu/dokploy-api) <br>
- [Dokploy domain index](artifact/modules/_index.md) <br>
- [Dokploy OpenAPI snapshot](artifact/openapi.json) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown] <br>
**Output Format:** [Markdown guidance with API request details and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operation IDs, request payloads, verification steps, and recovery guidance; secrets should be redacted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
