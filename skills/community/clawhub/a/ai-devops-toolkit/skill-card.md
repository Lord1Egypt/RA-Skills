## Description:

DevOps observability toolkit for local AI fleet operations, covering request tracing, health checks, latency monitoring, capacity planning, and analytics backed by SQLite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to inspect Ollama Herd fleet health, request traces, latency behavior, per-application usage, and capacity signals for local LLM operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telemetry in local traces, logs, dashboards, and SQLite data can expose infrastructure details and usage patterns.

Mitigation: Review telemetry before sharing it and keep access limited to appropriate operators.

Risk: Installing an unpinned package can introduce unexpected dependency or behavior changes.

Mitigation: Install in a virtual environment or dedicated low-privilege account, and pin and verify ollama-herd where possible.

Risk: POST requests and other configuration-changing commands can alter the running local AI fleet.

Mitigation: Require explicit operator approval before running configuration-changing commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/ai-devops-toolkit)
- [ollama-herd PyPI package](https://pypi.org/project/ollama-herd/)
- [Ollama Herd repository](https://github.com/geeks-accelerator/ollama-herd)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, SQL queries, curl requests, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local SQLite telemetry, JSONL logs, and localhost Ollama Herd dashboard APIs.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
