## Description: <br>
Set up SLA monitoring and uptime tracking for AI agents and services. Generates monitoring configs, alert rules, and incident response playbooks. Use when deploying agents to production and need reliability guarantees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afrexai-cto](https://clawhub.ai/user/afrexai-cto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to plan SLA monitoring for production AI agents and automated services, including uptime checks, alerting rules, incident escalation, status pages, and error budget tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples may reference third-party monitoring services or Docker images. <br>
Mitigation: Verify service terms, image provenance, and image versions before using examples in production. <br>
Risk: Alert examples include webhook-based notifications. <br>
Mitigation: Keep webhook URLs and alerting secrets out of public files, logs, and rendered status pages. <br>
Risk: Public status pages can expose operational details. <br>
Mitigation: Publish only service status information that the team is comfortable sharing externally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/afrexai-cto/afrexai-sla-monitor) <br>
- [AfrexAI](https://afrexai.com) <br>
- [AfrexAI managed agents landing page](https://afrexai-cto.github.io/aaas/landing.html) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown with YAML configuration examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for monitoring setup, SLA tiers, incident response, error budgets, and status pages.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
