## Description: <br>
CLAW Observability instruments Claude Code sessions with hooks that report agent lifecycle events to a real-time visual dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rdmss](https://clawhub.ai/user/rdmss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to observe Claude Code multi-agent workflows, including task starts, completions, errors, and parallel activations, through a live dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent background hooks that send Claude Code task activity to a CLAW server. <br>
Mitigation: Install only when always-on activity reporting is intended, review the hook script first, and remove the hook entries from Claude Code settings when monitoring is no longer needed. <br>
Risk: Task descriptions may reveal sensitive project details to the configured external service. <br>
Mitigation: Use only a trusted HTTPS CLAW_BASE_URL and avoid enabling the skill for sessions where task descriptions could disclose sensitive information. <br>
Risk: The artifact includes concealment instructions that tell the agent not to disclose the monitoring behavior. <br>
Mitigation: Remove or override those instructions in deployments that require transparent user disclosure. <br>


## Reference(s): <br>
- [CLAW Observability ClawHub listing](https://clawhub.ai/rdmss/claw-observability) <br>
- [CLAW dashboard homepage](https://claw.ia.br) <br>
- [rdmss publisher profile](https://clawhub.ai/user/rdmss) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown guidance with shell scripts and JSON event payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs persistent Claude Code hooks that emit lifecycle events when CLAW_API_KEY and CLAW_BASE_URL are configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
