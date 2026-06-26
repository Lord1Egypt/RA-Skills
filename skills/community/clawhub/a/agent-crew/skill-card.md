## Description: <br>
Creates, manages, and awakens persistent multi-agent collaboration teams with standardized agent configuration files and .claude team structures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[201983290498](https://clawhub.ai/user/201983290498) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create, validate, and reload persistent multi-agent teams with role-specific configuration, memory, progress tracking, and private skill directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory and progress files are reused in generated prompts and can expose secrets or sensitive personal data if users store them there. <br>
Mitigation: Do not put API keys, passwords, tokens, regulated data, customer data, or confidential one-off details in memory.md or progress.md; review and prune team memory before awakening an existing team. <br>
Risk: The skill creates and reloads persistent local agent team state under .claude, which may affect future agent behavior. <br>
Mitigation: Review generated .claude/agents and .claude/teams files, keep team_charter.md synchronized with team changes, and run the validation script before instantiating agents. <br>
Risk: Agents could begin work from assumed requirements if confirmation checkpoints are skipped. <br>
Mitigation: Follow the documented confirmation gates: require user confirmation before creating agents and keep initial agent status alignment limited to reading progress and memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/201983290498/agent-crew) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Data contracts](artifact/data_contracts.md) <br>
- [Harness rules](artifact/harness_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with file templates, shell commands, and generated agent prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent local .claude team files and prompt-visible memory/progress content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
