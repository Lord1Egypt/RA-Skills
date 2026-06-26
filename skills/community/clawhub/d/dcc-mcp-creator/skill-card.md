## Description: <br>
Guides developers and agents through creating or modernizing DCC-MCP adapters for digital content creation hosts such as Nuke, Blender, 3ds Max, Unreal, ZBrush, Houdini, Maya, and custom studio tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loonghao](https://clawhub.ai/user/loonghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to scaffold, modernize, and validate DCC-MCP adapter repositories, including server composition, host dispatch, gateway integration, packaging, runtime lifecycle, and cross-DCC verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide shell command execution and file edits in a development workspace. <br>
Mitigation: Install and use it only when adapter scaffolding or modernization is expected, and review generated changes before applying them to important repositories. <br>
Risk: Adapter guidance may affect runtime integration, host dispatch, gateway behavior, or release validation. <br>
Mitigation: Follow the included testing and release references, run repository-native validation, and keep one live or HTTP-level smoke test for behavior that crosses process boundaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loonghao/dcc-mcp-creator) <br>
- [Skill homepage](https://github.com/dcc-mcp/dcc-mcp-core/blob/main/skills/dcc-mcp-creator/SKILL.md) <br>
- [Adapter Workflow](references/ADAPTER_WORKFLOW.md) <br>
- [Host Pattern Matrix](references/HOST_PATTERN_MATRIX.md) <br>
- [Core Escalation Checklist](references/CORE_ESCALATION_CHECKLIST.md) <br>
- [Testing And Release](references/TESTING_AND_RELEASE.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, configuration details, and proposed file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be reviewed before applying changes to important repositories.] <br>

## Skill Version(s): <br>
0.18.39 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
