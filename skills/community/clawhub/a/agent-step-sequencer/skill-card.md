## Description: <br>
Multi-step scheduler for in-depth agent requests that detects when a request needs multiple steps, proposes a plan, persists state, and runs a heartbeat-aware flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gostlightai](https://clawhub.ai/user/gostlightai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to break larger approved tasks into sequenced steps, persist progress, retry failed steps, and keep work moving through a heartbeat-driven runner. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heartbeat automation can continue approved multi-step work longer than intended. <br>
Mitigation: Review the generated plan and state.json before sensitive work, then disable the heartbeat or mark state DONE when automation should stop. <br>
Risk: A misconfigured STEP_AGENT_CMD or STEP_RUNNER could invoke an unintended local command. <br>
Mitigation: Set STEP_AGENT_CMD and STEP_RUNNER only to trusted local commands or paths; the runner also rejects shell interpreters and shell command flags. <br>
Risk: Sensitive values placed in step instructions or state may be persisted during the workflow. <br>
Mitigation: Avoid putting secrets in step instructions, generated plans, or state.json. <br>


## Reference(s): <br>
- [Agent Step Sequencer on ClawHub](https://clawhub.ai/gostlightai/agent-step-sequencer) <br>
- [Publisher Profile](https://clawhub.ai/user/gostlightai) <br>
- [State Schema](references/state-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON state examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update a persisted state.json workflow file when the agent follows the skill.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and CHANGELOG, released 2026-02-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
