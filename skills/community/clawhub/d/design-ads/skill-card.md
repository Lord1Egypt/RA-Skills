## Description: <br>
AI 知识类海报/封面图设计生成器，根据用户提供的主题内容生成 1200x1800 像素竖版海报和封面图，并使用统一的深色科技感视觉风格与六种模板布局。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bozoyan](https://clawhub.ai/user/bozoyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and agents use this skill to turn AI knowledge topics into vertical poster or cover artwork for platforms such as Xiaohongshu, WeChat, and promotional content. The skill guides content selection, template choice, HTML construction, and PNG rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML and PNG files are copied to a local Downloads folder and may persist after the session. <br>
Mitigation: Use non-sensitive poster content, review the generated files, and delete the timestamped design-ads Downloads folder when persistence is not desired. <br>
Risk: Rendering untrusted or sensitive HTML can expose local content through saved artifacts or browser rendering behavior. <br>
Mitigation: Review generated HTML before rendering and avoid using untrusted HTML inputs or confidential content. <br>


## Reference(s): <br>
- [Design system specification](references/design-system.md) <br>
- [ClawHub skill page](https://clawhub.ai/bozoyan/design-ads) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with HTML/CSS code and shell commands that render PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 1200x1800 PNG poster images and saves local HTML/PNG copies to a timestamped Downloads folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
