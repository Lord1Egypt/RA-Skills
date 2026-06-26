## Description: <br>
Recipe: Export Recipes as installable SKILL.md files for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingconan](https://clawhub.ai/user/jingconan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams who manage DeepVista Recipes use this skill to export recipes as installable SKILL.md files for AI agents such as Claude Code, Cursor, OpenCode, and OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the DeepVista CLI and a prerequisite DeepVista recipe skill, so execution can fail or produce incomplete guidance when those dependencies are unavailable. <br>
Mitigation: Install the deepvista-cli package, ensure the deepvista binary is available, and load the deepvista-recipe prerequisite before using the export workflow. <br>
Risk: Exported recipe skills may be added to an agent environment and influence future agent behavior. <br>
Mitigation: Review and scan exported SKILL.md files before installing or sharing them with a team. <br>
Risk: The security scan guidance recommends checking exact commands before using maintainer-oriented workflows. <br>
Mitigation: Inspect proposed commands and repo diffs before execution, and use documented opt-outs such as --no-yolo or disabling fallback reviewers when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jingconan/deepvista-recipe-export-knowledge-as-skills) <br>
- [DeepVista CLI homepage](https://cli.deepvista.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent through listing DeepVista recipes, exporting each recipe as SKILL.md content, saving exported skills, and verifying agent discovery.] <br>

## Skill Version(s): <br>
0.1.0-alpha.21 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
