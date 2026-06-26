## Description: <br>
Agent training system for training multi-agent teams, maintaining training manuals, aligning goals and capabilities across sub-agents, and reviewing agent team configuration and evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zLiM5](https://clawhub.ai/user/zLiM5) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agent builders and operators use this skill to train new sub-agents, maintain a shared training manual, check agent configuration files, and coordinate ongoing team review and evolution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent agent memory and shared team notes may include sensitive personal details if users place them in USER.md, MEMORY.md, HEARTBEAT.md, EvoMap, or Capsule notes. <br>
Mitigation: Review shared memory and profile files before use, and avoid storing secrets or sensitive personal details unless broader agent reuse is intended. <br>
Risk: Team training guidance can propagate outdated or incorrect instructions across multiple agents. <br>
Mitigation: Use the skill's review and evolution checks to audit agent configuration files and update the training manual when behavior or requirements change. <br>


## Reference(s): <br>
- [Training Manual Template](references/training-manual-template.md) <br>
- [ClawHub Release Page](https://clawhub.ai/zLiM5/agent-training) <br>
- [Publisher Profile](https://clawhub.ai/user/zLiM5) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown training templates, checklists, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no external tool or MCP integration detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
