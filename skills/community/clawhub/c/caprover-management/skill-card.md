## Description: <br>
Manage CapRover PaaS instances via API, including app creation and updates, Docker image or Dockerfile deployments, ports, volumes, environment variables, logs, and Docker Swarm serviceUpdateOverride settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guim4dev](https://clawhub.ai/user/guim4dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to have an agent plan or generate CapRover API calls, helper code, and configuration guidance for deploying, configuring, troubleshooting, and reading logs for apps on a CapRover server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent administrative control over a CapRover server, including deploy, delete, registry, volume, port, and serviceUpdateOverride changes. <br>
Mitigation: Use only when the agent is intended to administer that server, restrict credentials to the intended environment, and review proposed administrative changes before execution. <br>
Risk: The artifact demonstrates disabling TLS certificate verification while handling CapRover credentials. <br>
Mitigation: Prefer a valid certificate, custom CA bundle, or certificate pinning instead of disabling TLS verification. <br>
Risk: CapRover credentials and session tokens may appear in CLI output or logs. <br>
Mitigation: Avoid running the helper where command output is logged and redact passwords or tokens from transcripts and stored logs. <br>


## Reference(s): <br>
- [CapRover API Reference](references/api.md) <br>
- [CapRover Python Helper](scripts/caprover.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with Python and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CapRover API payloads, Dockerfile tar packaging guidance, and review steps for administrative changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
