## Description: <br>
FocalPoint is an AI cognitive operating system for persistent memory, attention management, workflow orchestration, workbench context preparation, and Three-Province review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeff0052](https://clawhub.ai/user/jeff0052) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add local persistent project memory, task tracking, context preparation, and review workflows to MCP-capable agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables persistent local memory and automatic logging across conversations, which may capture sensitive project details, secrets, or regulated personal data. <br>
Mitigation: Decide what projects are safe to store, avoid secrets and regulated personal data, and review the local SQLite database and log file locations before use. <br>
Risk: Retention, deletion, and opt-in behavior are not clearly documented in the available evidence. <br>
Mitigation: Review the package behavior and establish retention and cleanup practices before relying on the memory store for ongoing work. <br>
Risk: Optional GitHub or Notion sync may broaden access to project data. <br>
Mitigation: Verify the focalpoint package source and version, then review external-account permissions before enabling any sync integration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeff0052/focalpoint-memory) <br>
- [FocalPoint homepage](https://github.com/jeff0052/founderOSclaudecode) <br>
- [FocalPoint PyPI package](https://pypi.org/project/focalpoint/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, YAML configuration, and agent workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP server setup steps, tool-use guidance, and local memory workflow recommendations.] <br>

## Skill Version(s): <br>
0.3.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
