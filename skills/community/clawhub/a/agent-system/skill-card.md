## Description: <br>
OpenClaw agent-system routes user tasks through planning, execution, review, self-healing, and metrics flows based on task complexity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaxianb](https://clawhub.ai/user/xiaxianb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add an OpenClaw-oriented orchestration layer that classifies task intent, estimates complexity, and routes work through planner, executor, reviewer, and self-heal steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill acts as a broad planning layer that can influence how an agent routes and executes many task types. <br>
Mitigation: Keep explicit approval requirements for file changes, account actions, external posting, financial or business mutations, and other irreversible work. <br>
Risk: The skill instructs agents to continue with defaults or inferred values when information is missing. <br>
Mitigation: Require confidence labels for inferred conclusions and review outputs before using them for high-impact decisions. <br>
Risk: Logs, metrics, or learning-state paths may capture task content. <br>
Mitigation: Avoid passing secrets or sensitive user content through the skill's logging or metrics flows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaxianb/agent-system) <br>
- [orchestrator-reference.md](references/orchestrator-reference.md) <br>
- [README.md](README.md) <br>
- [AGENT_RULES.md](AGENT_RULES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON responses and Markdown guidance, with optional JavaScript code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include task plans, intent and complexity labels, quality metrics, self-heal status, degraded-mode status, and truncation markers.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, package.json, openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
