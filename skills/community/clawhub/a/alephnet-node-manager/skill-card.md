## Description: <br>
Alephnet Node Manager helps agents manage AlephNet node workflows for distributed memory, multi-agent team orchestration, coherence validation, content storage, identity signing, and token-economy operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and enterprise teams use this skill to guide AlephNet node setup, shared memory-field management, SRIA agent team orchestration, coherence validation, wallet operations, and related troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad command and file access could let proposed node-management operations alter local state or run unintended commands. <br>
Mitigation: Review generated shell commands before execution and run only intended AlephNet node commands in a constrained environment. <br>
Risk: Wallet, staking, token-transfer, persistent memory, and agent orchestration actions can affect funds, stored data, or active agent behavior. <br>
Mitigation: Require explicit confirmation for send, stake, write, memory, and agent or team operations, and keep API keys narrowly scoped. <br>
Risk: The activation scope is broad enough that the skill could be invoked for unrelated AI chat or coding tasks. <br>
Mitigation: Use the skill only for AlephNet node management and avoid applying it to generic AI chat or unrelated development work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/alephnet-node-manager) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated commands, configuration, wallet actions, and memory writes should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
