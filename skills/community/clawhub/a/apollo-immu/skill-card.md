## Description: <br>
Intercepts risky agent operations before execution and uses a local trust database to reduce repeated confirmations for trusted recipient-operation pairs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add a confirmation gate before sensitive actions such as file deletion, external messages, command execution, and permission changes. It is intended to make routine trusted actions less noisy while still pausing for higher-risk operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic trust learning may reduce confirmations for sensitive actions based on weak conversation cues. <br>
Mitigation: Keep explicit confirmation enabled for sends, command execution, permission changes, and non-temporary deletes, or disable conversational auto-learning before deployment. <br>
Risk: The skill stores confirmation counts in a persistent local trust database. <br>
Mitigation: Review the trust database before reuse across users or environments and reset entries that should not carry forward. <br>


## Reference(s): <br>
- [Apollo Immu ClawHub page](https://clawhub.ai/nic-yuan/apollo-immu) <br>
- [Risk levels reference](references/risk_levels.md) <br>
- [Auto-learn reference](references/auto_learn.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON interceptor decisions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local trust database for recipient-operation confirmation counts.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
