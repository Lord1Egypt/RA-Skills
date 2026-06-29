## Description: <br>
Unified orchestration: plugin-driven model routing, session hooks, project context automation, sidecar dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genortg](https://clawhub.ai/user/genortg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate OpenClaw project work, including model routing, session and decision logging, project context setup, dashboard-based model management, and supporting shell workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dashboard and logging features may expose or persist local project, session, and model data more broadly than intended. <br>
Mitigation: Keep the dashboard on localhost unless authentication and restricted CORS are added, and review or disable session/context logging for sensitive projects. <br>
Risk: Onboarding, cron, PM2, provider probes, and shell scripts can create scheduled jobs, background services, or network checks. <br>
Mitigation: Run those commands only after confirming the exact files, endpoints, and scheduled commands involved. <br>


## Reference(s): <br>
- [ClawHub Package Page](https://clawhub.ai/genortg/genor-orchestrator) <br>
- [Skill Source Repository](https://github.com/GenorTG/genor-orchestrator-skill) <br>
- [Companion Plugin Repository](https://github.com/GenorTG/genor-orchestrator-plugin) <br>
- [Full Reference Documentation](references/README.md) <br>
- [Onboarding Guide](references/ONBOARDING.md) <br>
- [Execution Reference](references/EXECUTION.md) <br>
- [Model Routing Reference](ROUTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local orchestration data, project planning files, ADRs, logs, model catalog files, and dashboard configuration when used by an agent.] <br>

## Skill Version(s): <br>
2.3.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
