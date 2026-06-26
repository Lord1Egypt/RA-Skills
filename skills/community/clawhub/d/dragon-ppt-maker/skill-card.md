## Description: <br>
使用 python-pptx 创建科技风、现代或企业风 PowerPoint 演示，支持标题页、内容页、特性网格、对比页、图片页和 HTML 内容摘要页。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dragon015](https://clawhub.ai/user/dragon015) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, content creators, and business users use this skill to generate styled PowerPoint presentations from command-line arguments or a Python API, including reusable layouts for titles, bullet content, feature grids, comparisons, images, and HTML previews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes generated presentation files to local paths, and demo mode uses a hardcoded save location. <br>
Mitigation: Choose output paths deliberately and avoid demo mode when that hardcoded location is not desired. <br>
Risk: Slide content and HTML previews may include sensitive text provided by the user. <br>
Mitigation: Do not include passwords, tokens, private URLs, or other sensitive content in presentation text or HTML preview inputs. <br>
Risk: The Python dependencies execute in the local environment used to generate presentations. <br>
Mitigation: Install and run the dependencies only in an environment you trust. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dragon015/dragon-ppt-maker) <br>
- [Publisher profile](https://clawhub.ai/user/dragon015) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with Python and shell command snippets; generated .pptx presentation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local PowerPoint files and supports theme, title, content, and output-path options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
