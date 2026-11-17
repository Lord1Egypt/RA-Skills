## Description: <br>
Figma Tw Designer Free helps agents interact with Figma files by reading file structure, exporting selected layers, and reviewing recent comments through the Figma REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, product managers, and front-end developers use this skill to inspect Figma file hierarchy, export individual design assets, and review recent comments from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests read, write, and execution capabilities and documents mutation-style operations beyond its stated read, export, and comment-review purpose. <br>
Mitigation: Review the requested action before execution and allow create, modify, delete, or reset-style operations only when the user explicitly asks for them. <br>
Risk: Figma personal access tokens can expose account or file access if pasted into chat logs, files, or repositories. <br>
Mitigation: Use a least-privilege Figma token when possible, pass it through an environment variable or secret manager, and rotate or revoke it if exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/figma-tw-designer-free) <br>
- [Skill Homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON-shaped responses, and exported design assets when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce exported PNG, JPG, SVG, or PDF assets from user-specified Figma node IDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
