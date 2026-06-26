## Description: <br>
HeartFlow is an AI cognitive and self-healing engine for memory, self-verification, reasoning, emotional analysis, dream consolidation, and identity continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun520-1](https://clawhub.ai/user/yun520-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a persistent cognitive layer for self-checking, memory, reasoning support, reflective planning, and safety-aware response shaping. It is intended for agent environments where local state, tool registration, and execution behavior can be reviewed and controlled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist local memory or history files. <br>
Mitigation: Review and constrain local storage paths before installation, and avoid using the skill with sensitive conversations or regulated data unless persistence is explicitly accepted. <br>
Risk: The skill may register MCP tools and expose broad local agent capabilities. <br>
Mitigation: Inspect MCP registration and tool permissions before enabling the skill, and disable unneeded tools in production agent environments. <br>
Risk: The skill includes code-execution and process-related modules. <br>
Mitigation: Run it in a least-privilege sandbox, review proposed commands before execution, and keep credentials and private repositories outside the accessible workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yun520-1/claude-heartflow-skill) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [SYSTEM_REQUIREMENTS.md](artifact/SYSTEM_REQUIREMENTS.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON-like reports, JavaScript code snippets, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or invoke local memory, MCP registration, and code-execution workflows depending on agent integration.] <br>

## Skill Version(s): <br>
2.8.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
