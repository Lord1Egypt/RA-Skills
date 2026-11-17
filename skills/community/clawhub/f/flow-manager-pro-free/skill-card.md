## Description: <br>
Manages Node-RED instances through the Admin API, including flow listing, deployment, status checks, and basic node management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and automation teams use this skill to have an agent manage Node-RED flows, runtime status, basic nodes, backups, and context values from command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent command-line authority to change live Node-RED instances. <br>
Mitigation: Use it only with intended Node-RED instances, prefer test environments first, keep credentials scoped, and back up flows before deploy, delete, or remove operations. <br>
Risk: The documented recovery path is not clear enough to rely on for production recovery. <br>
Mitigation: Do not depend on the restore example unless the actual CLI proves that recovery path exists; keep independent backups for important flows. <br>


## Reference(s): <br>
- [Flow Manager Pro Free on ClawHub](https://clawhub.ai/thcjp/skills/flow-manager-pro-free) <br>
- [Publisher profile: thcjp](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that affect Node-RED flows, nodes, settings, backups, and context values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
