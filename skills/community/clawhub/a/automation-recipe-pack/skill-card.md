## Description: <br>
自动化配方 provides 10 practical automation recipes for file handling, data conversion, batch operations, and workflow orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations teams, and automation users use this skill to plan and generate recipes for routine file processing, data cleanup and conversion, batch operations, and workflow orchestration. It is best suited to explicit, repeatable tasks rather than work requiring human creative judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad file and command authority can modify, rename, sync, or delete user files. <br>
Mitigation: Use explicit source and target folders, preview or dry-run steps where possible, and keep backups before destructive operations. <br>
Risk: Vague external API or networked workflow guidance may expose data or credentials. <br>
Mitigation: Do not provide API keys or allow network calls unless the exact service, data sent, and purpose are clear. <br>
Risk: Generated automation recipes may be unsuitable for unsupported formats, large inputs, or tasks requiring creative judgment. <br>
Mitigation: Test on small samples, validate input and output formats, and review logs and results before applying broadly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/automation-recipe-pack) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and structured JSON-style result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file read, write, rename, sync, and cleanup operations; review paths and destructive actions before execution.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
