## Description:

Provides a practical runbook for monitoring live AI agents through logging, quality review, alerts, incident response, human escalation, and weekly review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create an operations runbook for a production AI agent, covering traceable runs, workload-specific quality and cost signals, alert ownership, rollback, human review, and recurring review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trace logs can expose sensitive inputs, outputs, or tool data.

Mitigation: Redact sensitive fields and define log access and retention before enabling full-run logging.

Risk: Pausing or rolling back a production agent can disrupt service or business workflows.

Mitigation: Agree in advance on who is authorized to pause or roll back the agent and how those decisions are escalated.

## Reference(s):

- [Google SRE: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [OpenTelemetry GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions-genai)
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [NIST AI Risk Management Framework 1.0](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
- [OpenAI: Sycophancy in GPT-4o](https://openai.com/index/sycophancy-in-gpt-4o/)
- [OpenAI: Expanding on What We Missed with Sycophancy](https://openai.com/index/expanding-on-sycophancy/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown one-page operations runbook with labeled fields and a checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tailored to the workload's own metrics, thresholds, alert recipients, and escalation rules; no universal numeric thresholds are prescribed.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
