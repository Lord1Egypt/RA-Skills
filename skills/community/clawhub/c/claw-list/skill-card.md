## Description: <br>
Claw List lets agents manage self-hosted todo lists through a central REST API with per-agent lists, optional categories, priorities, due dates, and a web UI for human oversight. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mbojer](https://clawhub.ai/user/mbojer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give agents a shared, self-hosted task system while keeping list and item operations behind a REST API instead of direct database access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthenticated admin endpoints and identity controls can expose or alter task data if the API or UI is reachable by untrusted users. <br>
Mitigation: Deploy only on trusted private networks or behind real authentication, TLS, and network access controls; keep default loopback bindings unless protected by a reverse proxy. <br>
Risk: Agent IDs act as bearer identity values and notes can contain conversation context or sensitive data. <br>
Mitigation: Treat agent IDs as secrets, avoid storing credentials, personal data, or raw transcripts in notes, and confirm destructive list or item actions before sending requests. <br>


## Reference(s): <br>
- [Claw List on ClawHub](https://clawhub.ai/mbojer/claw-list) <br>
- [Overview](docs/overview.md) <br>
- [API Reference](docs/api.md) <br>
- [Server README](server/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON API request bodies and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configured CLAW_LIST_URL and X-Agent-Id header; task notes may include user-provided context.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
