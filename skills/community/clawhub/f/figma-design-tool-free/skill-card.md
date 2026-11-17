## Description: <br>
Figma设计集成-免费版 helps agents browse Figma team projects and files, read file structure and node details, export images, and review comments or version history through a MorphixAI-brokered Figma connection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual designers and developers use this skill to inspect Figma workspaces, extract design structure, export assets, and review comments or file history. It is intended for single-file design asset handoff and design review workflows, not broad document conversion or generic file processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to a third-party API broker that can access Figma workspace design data. <br>
Mitigation: Use a least-privilege Figma account or workspace connection and avoid connecting sensitive Figma workspaces unless MorphixAI access is acceptable. <br>
Risk: The skill instructions are broad and partly inconsistent with its Figma-focused capability boundary. <br>
Mitigation: Use it only for Figma browsing, reading, exporting, comments, and version history; do not rely on it for generic document conversion or file processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/figma-design-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline command examples and structured JSON-style response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to call mx_figma actions and return status, result data, execution logs, and errors.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact/SKILL.md frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
