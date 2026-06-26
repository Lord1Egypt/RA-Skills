## Description: <br>
Beautiful Mermaid renders Mermaid diagrams as SVG, PNG, or ASCII art with built-in themes, style presets, CSS-level customization, interactive preview, and batch rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chouraycn](https://clawhub.ai/user/chouraycn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to turn Mermaid source into polished diagrams for terminal, chat, web, and documentation workflows. It supports one-off rendering, batch rendering, preview-driven styling, and rich HTML diagram collections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The renderer reads Mermaid files and writes SVG, PNG, ASCII, or HTML outputs to user-selected paths. <br>
Mitigation: Review input and output paths before running render or batch commands, especially when operating in shared workspaces. <br>
Risk: The preview tool stores preferences and custom diagram code in browser localStorage. <br>
Mitigation: Avoid entering sensitive diagram content in the preview when using shared browsers or machines. <br>
Risk: Preview or exported HTML may contact Google Fonts unless blocked or modified. <br>
Mitigation: Use network controls or modify exported HTML when offline operation or third-party font isolation is required. <br>
Risk: Installing the skill brings npm dependencies into the execution environment. <br>
Mitigation: Review dependency policy and install from trusted package sources before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chouraycn/beautiful-mermaid) <br>
- [Publisher Profile](https://clawhub.ai/user/chouraycn) <br>
- [Project Homepage](https://github.com/chouraycn/beautiful-mermaid) <br>
- [API Configuration Reference](references/api-config.json) <br>
- [Mermaid Documentation](https://mermaid.js.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Mermaid examples, shell commands, and rendering guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides an agent to produce Mermaid render commands and files such as SVG, PNG, ASCII text, or rich HTML outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
