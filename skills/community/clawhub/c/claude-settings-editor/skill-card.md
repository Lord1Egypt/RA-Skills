## Description: <br>
Use when the user wants to update Claude settings, hooks, permissions, MCP server toggles, or other JSON config safely and with scope awareness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to safely edit Claude settings, hooks, permissions, MCP server toggles, and related JSON configuration while preserving the intended scope and existing settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Changes to permissions, hooks, plugins, or MCP settings can affect future agent behavior or broaden access. <br>
Mitigation: Specify the exact Claude settings file or scope, review the diff before accepting writes, and be especially careful with hook, permission, plugin, or MCP changes. <br>
Risk: Whole-file rewrites can remove unrelated user settings or leave JSON configuration invalid. <br>
Mitigation: Read the current settings file before editing, apply the smallest valid JSON change, preserve unrelated settings, and validate JSON after editing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration edits and risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scope explanation, JSON validation expectations, and risk notes for sensitive configuration changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
