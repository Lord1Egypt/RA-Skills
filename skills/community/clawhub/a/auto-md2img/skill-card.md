## Description: <br>
Convert Markdown content to images with GitHub styling, Chinese font support, smart pagination, emoji support, syntax highlighting, height-based pagination, and JPEG quality adjustment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fried-avocado](https://clawhub.ai/user/fried-avocado) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert Markdown replies, technical notes, tables, code snippets, and long formatted content into image files for messaging or sharing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendering untrusted Markdown in a browser may trigger outbound requests or process hostile content. <br>
Mitigation: Use the skill only with trusted Markdown, or run it in a sandbox with network access blocked. <br>
Risk: Generated images, logs, debug HTML, and page files can leave sensitive document content on disk. <br>
Mitigation: Avoid secrets and private documents, disable debug mode for sensitive content, use a controlled output directory, and clean generated artifacts after use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fried-avocado/auto-md2img) <br>
- [Publisher profile](https://clawhub.ai/user/fried-avocado) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with command examples; generated outputs are PNG or JPEG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports paginated image output, configurable JPEG quality, and debug artifacts when debug mode is enabled.] <br>

## Skill Version(s): <br>
1.3.1 (source: server evidence and changelog, released 2026-03-15) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
