## Description:

Tracks OpenClaw API usage and spending in real time with budget alerts, dashboard analytics, and model/session cost breakdowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[someone0070](https://clawhub.ai/user/someone0070)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users, teams, and developers use Clawmeter to monitor local session-log costs, compare model spending, and receive budget alerts from a self-hosted dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated dashboard and API access can expose usage and cost metadata if the service is reachable beyond a trusted local machine.

Mitigation: Use only on a trusted local machine, do not expose port 3377 to a network, and add authentication plus explicit loopback binding before broader deployment.

Risk: Browser rendering flaws can make dashboard display unsafe when stored values are rendered into the page.

Mitigation: Avoid ingesting untrusted logs and fix dashboard HTML escaping before relying on shared, remote, or production use.

Risk: Remote installation scripts and outdated dependencies can add supply-chain and maintenance risk.

Mitigation: Pin or bundle remote scripts, update dependencies, and review the package before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/someone0070/skills/clawmeter)
- [README](README.md)
- [OpenClaw skill guide](SKILL.md)
- [Quick start guide](docs/QUICKSTART.md)
- [Architecture](docs/ARCHITECTURE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, HTTP endpoint examples, JavaScript snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to query a local REST API and summarize cost, budget, model, session, or alert data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
