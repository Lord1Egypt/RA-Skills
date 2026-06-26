## Description: <br>
Ai Company guides an agent to scaffold a lightweight AI-company operating system with AI employee roles, event-driven coordination, scheduled workflows, configuration, and example Python code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sendwealth](https://clawhub.ai/user/sendwealth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create an AI-company prototype with specialized agent roles for market research, product design, development, sales, support, monitoring, and finance. It is best treated as an automation scaffold that requires human review before connecting credentials, schedules, deployments, or customer-facing channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to connect credentials and external accounts for automation, email, social posting, deployment, and scheduled jobs. <br>
Mitigation: Start in an isolated workspace with throwaway or least-privilege accounts, and keep social posting, email sending, deployment, and cron jobs disabled until reviewed. <br>
Risk: Autonomous business workflows could publish, contact customers, deploy code, or make operational decisions without sufficient oversight. <br>
Mitigation: Add human approval gates, rate limits, logging, privacy controls, rollback plans, and staged testing before any production or customer-facing use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sendwealth/ai-company) <br>
- [Design documentation](docs/design.md) <br>
- [API documentation](docs/api.md) <br>
- [Examples README](examples/README.md) <br>
- [Examples quickstart](examples/QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and YAML examples, shell commands, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scaffolding guidance and example automation code; generated projects require user-supplied credentials and human review before operation.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
