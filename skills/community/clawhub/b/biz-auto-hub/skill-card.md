## Description: <br>
商业自动中枢 helps solo companies and small teams assess, design, quantify, and monitor business automations with ROI scorecards, workflow templates, and health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Owners, operators, and small-team developers use this skill to decide which business processes should be automated, design practical workflows, calculate ROI, and set up monitoring patterns for ongoing reliability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward command execution, scheduled jobs, and external integrations. <br>
Mitigation: Keep runs in planning or dry-run mode by default and require explicit approval before exec commands, cron creation, notifications, or external system writes. <br>
Risk: Automation workflows may affect finance, CRM, content publishing, or payment processes. <br>
Mitigation: Require human approval before finance or CRM writes, production payment actions, content publishing, new-vendor handling, low-confidence extraction, or missing purchase-order data. <br>
Risk: Automations can fail silently or continue with stale credentials or broken integrations. <br>
Mitigation: Use the skill's alert routing, health report, credential vault, and approval-gate patterns before deploying workflows beyond planning. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/biz-auto-hub) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with YAML templates, workflow examples, and command-oriented implementation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language automation planning material with optional execution, cron, notification, and integration steps that should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
