## Description: <br>
Use when generating template-driven emoji videos with Alibaba Cloud Model Studio Emoji (`emoji-v1`) from a detected portrait image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare Alibaba Cloud Model Studio Emoji detection and generation requests for fixed-template facial animation clips from a single portrait image. <br>

### Deployment Geography for Use: <br>
China mainland (Beijing) <br>

## Known Risks and Mitigations: <br>
Risk: Portrait image URLs and saved request evidence can contain personal data or long-lived public links. <br>
Mitigation: Use images you have permission to process, avoid sensitive or long-lived public portrait URLs, and delete or protect output/aliyun-emoji when trace evidence is no longer needed. <br>
Risk: Alibaba Cloud Model Studio requests require an API key. <br>
Mitigation: Use a dedicated scoped API key and avoid placing credentials in generated request artifacts. <br>


## Reference(s): <br>
- [Artifact reference list](references/sources.md) <br>
- [Alibaba Cloud Model Studio video generation overview](https://help.aliyun.com/zh/model-studio/use-video-generation) <br>
- [Emoji image detection API reference](https://help.aliyun.com/zh/model-studio/emoji-detect-api) <br>
- [Emoji video generation API reference](https://help.aliyun.com/zh/model-studio/emoji-api) <br>
- [Emoji quick start](https://help.aliyun.com/zh/model-studio/emoji-quick-start/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes normalized detect or generate request JSON under output/aliyun-emoji by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
