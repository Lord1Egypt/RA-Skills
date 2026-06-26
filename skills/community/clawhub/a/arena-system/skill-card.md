## Description: <br>
Adversarial self-improvement for AI agents. Reduces hallucinations through Agent vs Anti-Agent debate loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zedit42](https://clawhub.ai/user/Zedit42) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to set up an adversarial self-critique loop where an agent alternates between builder and critic personas for code review, risk assessment, trading strategy review, or other tasks that benefit from structured challenge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rerunning setup can overwrite arena state and prompt files. <br>
Mitigation: Review setup.sh first and run it against a fresh or backed-up arena directory. <br>
Risk: Adding the heartbeat snippet can create recurring self-critique iterations in the agent workflow. <br>
Mitigation: Add the snippet only when recurring critique is intended, confirm the install path, and keep max_iterations bounded. <br>
Risk: The same model may retain shared blind spots across both personas or prolong analysis. <br>
Mitigation: Use human review for consequential outputs and stop the loop when additional critique is no longer improving the result. <br>


## Reference(s): <br>
- [Arena System on ClawHub](https://clawhub.ai/Zedit42/arena-system) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local state, prompt, heartbeat snippet, and output directories for an alternating Agent and Anti-Agent workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
