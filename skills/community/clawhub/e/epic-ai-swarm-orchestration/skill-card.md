## Description: <br>
Portable OpenClaw skill and runtime for running parallel AI coding agents with tmux worktrees, duty-table model selection, token-limit fallback, review loops, integration watching, and heartbeat notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkbag](https://clawhub.ai/user/linkbag) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering operators use this skill to plan, spawn, monitor, review, and integrate parallel AI coding agents across local git worktrees with provider CLI fallbacks and notification hooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous agents can change code, commit, push, and open pull requests. <br>
Mitigation: Use the skill only in trusted development repositories with branch protections, explicit human endorsement before spawning, and review of agent branches or PRs before accepting changes. <br>
Risk: The runtime can use reduced-safeguard or auto-approved provider modes to allow worktree and repository operations. <br>
Mitigation: Review duty-table assignments, provider CLI command templates, and sandbox or approval flags before enabling the runtime on a project. <br>
Risk: Provider credentials, OAuth sessions, API keys, and notification targets may be required on the host. <br>
Mitigation: Keep credentials host-local, do not place secrets in packaged templates or prompts, and audit swarm.conf and notification targets before running agents. <br>
Risk: The skill persists work logs, ESR/history entries, and status notifications that may contain project-sensitive details. <br>
Mitigation: Run it only where such persistence and external notification are acceptable, and review logs or notification files before sharing them outside the project team. <br>
Risk: Live model assessment and fallback probes can consume provider quota. <br>
Mitigation: Run model probes deliberately, prefer dry runs when checking configuration, and confirm provider budget or quota constraints before automated assessment. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Tools Reference](references/tools.md) <br>
- [Duty Table](references/duty-table.md) <br>
- [End of Run Log](references/eor-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces orchestration plans, task prompts, runtime commands, status checks, and handoff or end-of-run summaries for agent workflows.] <br>

## Skill Version(s): <br>
3.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
