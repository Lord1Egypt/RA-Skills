## Description: <br>
从抖音视频反推AI绘画提示词和分镜脚本。当用户提到反推提示词、视频反推、抖音分析、分镜反推、游戏改写、视频转提示词时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clair-001](https://clawhub.ai/user/clair-001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to download or analyze a Douyin or local video, extract scene-by-scene storyboard details, and generate AI image prompts. It can also produce game-style and Rusty Lake-style rewrites when the required analyzer skills and ARK_API_KEY are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses ARK_API_KEY and sends selected videos or downloaded media to Volcengine/Doubao and downloader helper services. <br>
Mitigation: Use a dedicated API key, avoid sensitive private videos, and run the skill only when that third-party processing is acceptable. <br>
Risk: The workflow writes downloaded media and generated analysis files to a local output directory. <br>
Mitigation: Use a dedicated output directory and review generated files before sharing or reusing them. <br>
Risk: The skill depends on referenced downloader and analyzer skills for key behavior. <br>
Mitigation: Review and install the referenced helper skills before running this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clair-001/douyin-reverse-engineer) <br>
- [Publisher profile](https://clawhub.ai/user/clair-001) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration] <br>
**Output Format:** [CLI text plus JSON, Markdown, and CSV output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and ARK_API_KEY; optional output includes downloaded video files, analysis.json, prompt Markdown, storyboard Markdown, and storyboard CSV files.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
