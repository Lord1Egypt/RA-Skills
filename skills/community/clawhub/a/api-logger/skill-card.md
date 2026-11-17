## Description:

API Logger helps agents install and use a local proxy and log viewers to record, analyze, and visualize LLM API prompts, responses, token usage, costs, slow requests, and failed requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaohuaishu](https://clawhub.ai/user/xiaohuaishu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to route LLM API traffic through a local logging proxy, inspect prompt and response history, troubleshoot failed or slow calls, and estimate token usage and costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The proxy can retain full prompts, responses, and token usage in local logs.

Mitigation: Use it only in a controlled environment, avoid secrets or regulated data, and protect the log directory as sensitive data.

Risk: API traffic can be forwarded through an upstream endpoint that may not use HTTPS.

Mitigation: Change the upstream configuration to an HTTPS endpoint before routing traffic through the proxy.

Risk: The installer configures an always-on LaunchAgent proxy.

Mitigation: Prefer on-demand operation unless continuous background logging is explicitly needed.

Risk: Feishu export can send logged conversation content to an external exporter and destination.

Mitigation: Use Feishu export only when the exporter, destination, and access controls are trusted.

## Reference(s):

- [API Logger ClawHub skill page](https://clawhub.ai/xiaohuaishu/skills/api-logger)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide installation of a local proxy, local JSONL log files, terminal summaries, browser-based log inspection, and optional Feishu document export.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
