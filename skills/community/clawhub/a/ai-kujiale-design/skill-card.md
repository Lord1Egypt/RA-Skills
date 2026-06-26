## Description: <br>
室内智能设计skill，分步式对话完成户型确认→风格选择→布局确认→渲染出图。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuweiqi1993](https://clawhub.ai/user/wuweiqi1993) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and design-assistant agents use this skill to guide an interior design workflow: find or upload a floor plan, confirm style preferences, trigger Kujiale layout and rendering jobs, and return design images, panorama links, and design highlights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Kujiale access token that can create designs, upload floor-plan images, and run layout or render jobs. <br>
Mitigation: Store the token only in a local .kjlconfig.json file, keep it out of shared workspaces and logs, and rotate it if it is exposed. <br>
Risk: Layout and rendering jobs may consume the user's Kujiale quota or account credits. <br>
Mitigation: Require explicit user confirmation before triggering intelligent layout or rendering work that may use quota. <br>
Risk: Uploaded floor-plan images may contain private property or household information. <br>
Mitigation: Confirm the exact local image path with the user before upload and avoid uploading unrelated or sensitive files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wuweiqi1993/ai-kujiale-design) <br>
- [Publisher profile](https://clawhub.ai/user/wuweiqi1993) <br>
- [Kujiale skill token setup](https://www.kujiale.com/skills) <br>
- [Floor plan search API documentation](docs/planSearch.md) <br>
- [Floor plan upload API documentation](docs/upload.md) <br>
- [Intelligent layout API documentation](docs/layout.md) <br>
- [Rendering result API documentation](docs/renderResult.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with image links, panorama links, design detail links, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final answer follows artifact/outputs/result.md and prioritizes render images, panorama links, and design highlights.] <br>

## Skill Version(s): <br>
0.0.6 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
