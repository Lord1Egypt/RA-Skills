## Description: <br>
Unified orchestration: plugin-driven model routing, session hooks, project context automation, sidecar dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genortg](https://clawhub.ai/user/genortg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate AI-assisted software projects, manage model routing rules, log sessions and decisions, scaffold project context, and run a local dashboard for model and project state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores project and session history on disk, which can retain sensitive prompts, decisions, model configuration, and project state. <br>
Mitigation: Set ORCHESTRATOR_DATA_DIR deliberately, avoid logging secrets or sensitive prompts, and review retained files before sharing the workspace. <br>
Risk: The dashboard exposes local model, project, and document controls and can update configuration and project files. <br>
Mitigation: Keep the dashboard bound to localhost or behind authentication, review access before starting it, and avoid exposing the port to untrusted networks. <br>
Risk: PM2 or cron setup can keep the dashboard and maintenance tasks running persistently. <br>
Mitigation: Review the exact PM2 and scheduled-command behavior before enabling persistence, and disable it when the orchestration service is not needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/genortg/genor-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/genortg) <br>
- [Skill homepage](https://clawhub.com/packages/genor-orchestrator) <br>
- [Routing reference](ROUTING.md) <br>
- [Full reference documentation](references/README.md) <br>
- [Execution reference](references/EXECUTION.md) <br>
- [Onboarding guide](references/ONBOARDING.md) <br>
- [Review notes](references/REVIEW.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated files, JSON configuration, and local dashboard updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local orchestration data, project documentation, session logs, ADRs, model inventory, and dashboard configuration.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
