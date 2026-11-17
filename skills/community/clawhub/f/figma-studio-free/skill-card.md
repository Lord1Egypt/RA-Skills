## Description: <br>
Figma Studio Free helps agents generate Figma API scripts and guidance for OAuth setup, file and node reads, comment handling, image export, and design token extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and product teams use this skill to ask an agent for ready-to-adapt Figma REST API examples that read design files, export node images, summarize comments, and turn design tokens into implementation assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The free/read-only framing can conflict with comment-posting examples that modify shared Figma files. <br>
Mitigation: Use comment-posting only when intentionally modifying a file, and require the agent to show the target file, node, and comment text before any write operation. <br>
Risk: Figma credentials can expose private design files if embedded in generated scripts or logs. <br>
Mitigation: Keep tokens and OAuth credentials in environment variables or credential files, and prevent generated commands from printing secrets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/figma-studio-free) <br>
- [Publisher Profile](https://clawhub.ai/user/thcjp) <br>
- [Skill Homepage](https://skillhub.cn) <br>
- [Figma API Base Endpoint](https://api.figma.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python, Node.js, shell, JSON, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include executable Figma API examples for file reads, image exports, comment management, and design-token extraction.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
