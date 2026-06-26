## Description: <br>
Analyzes conversation topic continuity to manage context, switch between topics, compress drifting history, and reduce token usage for multitask agent conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicochow](https://clawhub.ai/user/nicochow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to track topic continuity across multi-task conversations, decide whether to continue, compress, or switch context, and monitor token usage. It is useful for project workflows, research sessions, and long-running conversations where saved context should stay relevant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores conversation snippets and topic history in a local state file, which may retain sensitive conversation content. <br>
Mitigation: Review before installing for confidential conversations, avoid passing secrets as conversation content, and clear memory/context_switch_state.json before first use. <br>
Risk: Automatic token optimization and context switching may change saved context when token usage or similarity thresholds are met. <br>
Mitigation: Set TOKEN_OPTIMIZER_ENABLED=false when context changes should be manual, and review configuration thresholds before deployment. <br>
Risk: A reset action may not be sufficient for every operational cleanup expectation unless the saved state file is inspected. <br>
Mitigation: Use the context_manager.py reset path and manually inspect memory/context_switch_state.json when context must be fully cleared. <br>


## Reference(s): <br>
- [Context Switch Token Optimizer on ClawHub](https://clawhub.ai/nicochow/context-switch-token-optimizer) <br>
- [Topic and Continuity Logic](artifact/docs/TOPIC_AND_CONTINUITY.md) <br>
- [Usage Guide](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, JSON configuration, and status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local context state and topic history in memory/context_switch_state.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
