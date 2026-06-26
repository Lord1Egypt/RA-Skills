## Description: <br>
Helps agents design and audit observability and reliability practices across structured logging, metrics, tracing, SLOs, alerting, incident response, post-mortems, on-call operations, chaos engineering, and cost optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, platform engineers, and SRE teams use this skill to assess observability maturity and produce practical monitoring, logging, tracing, SLO, alerting, dashboard, runbook, incident response, post-mortem, on-call, chaos engineering, and cost optimization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated runbooks, rollback steps, chaos experiments, alert-routing updates, or status communications could affect production systems if applied without review. <br>
Mitigation: Confirm whether the task is read-only or change-making, and require explicit approval before rollbacks, pod deletion, chaos tests, alert-routing changes, or public status updates. <br>
Risk: Logging and tracing guidance may expose secrets or sensitive personal data if copied without local redaction controls. <br>
Mitigation: Apply secret and personal-data redaction, validate scrub patterns, and review retention settings before adopting logging examples in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1kalin/afrexai-observability-engine) <br>
- [AfrexAI context packs](https://afrexai-cto.github.io/context-packs/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with tables, templates, YAML examples, and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; review production changes before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
