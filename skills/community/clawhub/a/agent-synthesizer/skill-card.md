## Description: <br>
Enable and configure Agent Synthesizer for OpenClaw to improve autonomy and execution throughput. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rylena](https://clawhub.ai/user/rylena) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install, configure, troubleshoot, and optimize Agent Synthesizer for OpenClaw by following the referenced repository README. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to follow a changing repository README and run setup commands from it. <br>
Mitigation: Require the agent to show the exact README commands before execution and review them in a low-privilege or disposable environment. <br>
Risk: Setup may request tokens, credentials, or environment-specific access during installation. <br>
Mitigation: Do not provide credentials unless the README need is clear, current, and reviewed for the target environment. <br>


## Reference(s): <br>
- [Agent Synthesizer ClawHub page](https://clawhub.ai/rylena/agent-synthesizer) <br>
- [Agent Synthesizer setup repository](https://github.com/rylena/agent-synth) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes the current README step, exact commands to run, success criteria, and the next step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
