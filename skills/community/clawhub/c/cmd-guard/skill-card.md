## Description: <br>
Exec Guard classifies shell commands by intended effect before execution and guides agents to allow low-risk commands while requiring confirmation for system, network, and destructive actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wavmson](https://clawhub.ai/user/wavmson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Exec Guard as a command-execution safety layer for agents with shell access. It helps classify proposed commands and request user confirmation before higher-risk execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A command can be misclassified or chained with a higher-impact action than the first token suggests. <br>
Mitigation: Classify compound commands by their highest-risk operation and require confirmation for WRITE_SYSTEM, NETWORK, and DESTRUCTIVE actions. <br>
Risk: Destructive commands can delete data, reset work, or change services in ways that are hard to recover. <br>
Mitigation: Always explain the impact, suggest a safer alternative when available, and wait for explicit user approval before execution. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/wavmson/cmd-guard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with command classifications, risk explanations, and safer alternatives] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Applies a five-level command classification: READ, WRITE, WRITE_SYSTEM, NETWORK, and DESTRUCTIVE.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
