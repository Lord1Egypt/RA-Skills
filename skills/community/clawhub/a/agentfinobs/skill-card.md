## Description: <br>
AI Agent Financial Observability for monitoring, budgeting, and analyzing spending across AI agents, including cost tracking, budget alerts, anomaly detection, and metrics exports across payment rails such as x402/USDC, Stripe/ACP, and Polymarket CLOB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oc127](https://clawhub.ai/user/oc127) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to add financial observability to AI agents, including spend tracking, budget enforcement, anomaly detection, dashboard views, and JSONL, webhook, or Prometheus exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard and Prometheus endpoints can expose sensitive agent spending telemetry if bound to untrusted networks without authentication. <br>
Mitigation: Bind services to localhost where possible, firewall dashboard and metrics ports, or place them behind an authenticated reverse proxy before deployment. <br>
Risk: Transaction descriptions, tags, error messages, JSONL files, and webhook exports may contain secrets, prompts, or sensitive business data. <br>
Mitigation: Avoid recording secrets or sensitive prompts in telemetry fields, review exporter destinations, and restrict access to local logs and webhook receivers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oc127/agentfinobs) <br>
- [README](README.md) <br>
- [Publisher profile](https://clawhub.ai/user/oc127) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide agents to produce local JSONL records, HTTP dashboard output, webhook payloads, and Prometheus metrics.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact pyproject.toml reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
