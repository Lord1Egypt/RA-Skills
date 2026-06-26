## Description: <br>
Launch a local WeChat article workbench for Markdown import, WeChat HTML preview, theme tuning, image selection, and optional draft push. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abigale-cyber](https://clawhub.ai/user/abigale-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, editors, and developers use this skill to import Markdown articles into a local browser workbench, preview WeChat-ready HTML, tune themes and images, and optionally push a checked result to a WeChat draft box. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workbench can expose local workspace files and draft article data. <br>
Mitigation: Install and run it only in a trusted local workspace, and avoid importing sensitive unpublished drafts unless sharing derived prompts or media with configured providers is acceptable. <br>
Risk: SK or API tokens may be used for image generation or WeChat publishing flows. <br>
Mitigation: Do not paste or share tokens casually; review the configured provider and token fields before use. <br>
Risk: Draft push can send article content and media to the wrong WeChat target if settings are incorrect. <br>
Mitigation: Verify the target WeChat account, article metadata, cover, and image references before pressing draft push. <br>
Risk: Generated HTML or JSON may contain signed remote image links. <br>
Mitigation: Treat exported preview artifacts as potentially sensitive and avoid sharing them beyond the intended review or publishing workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abigale-cyber/content-system-wechat-studio) <br>
- [Skill README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Banana login platform](https://job.suxi.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, local preview files, JSON article state, and optional WeChat draft output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workbench produces local browser previews, article workspace state, selected image assets, and optional WeChat draft pushes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
