## Description: <br>
Provides a reusable AI agent operating-system template that separates identity, operations, and knowledge files for modular agent design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huamu668](https://clawhub.ai/user/huamu668) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill as a file-based template for defining an agent's identity, operating rules, long-term memory, shared context, and verification workflow. It is most useful when starting or standardizing an opinionated agent architecture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad persona and role instructions may steer agent behavior beyond the user's intended workflow. <br>
Mitigation: Review and narrow role, agent, and activation rules before deployment. <br>
Risk: Persistent memory and shared-context files can accumulate sensitive or stale information. <br>
Mitigation: Make memory writes explicit, avoid storing secrets or sensitive personal data, and periodically review memory contents. <br>
Risk: Shell scripts are used for startup and architecture verification. <br>
Mitigation: Review scripts before execution and run them only in an intended workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huamu668/agent-os-three-layer) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with bash script entry points] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes persistent memory and shared-context files that may be updated during agent use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
