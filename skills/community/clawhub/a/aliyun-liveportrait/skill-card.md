## Description: <br>
Use when generating lightweight talking-head portrait videos with Alibaba Cloud Model Studio LivePortrait (`liveportrait`) from a detected portrait image and speech audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content automation teams use this skill to prepare Alibaba Cloud LivePortrait detection and generation requests for talking-head videos from portrait images and speech audio. <br>

### Deployment Geography for Use: <br>
China mainland, Beijing region <br>

## Known Risks and Mitigations: <br>
Risk: Portrait image and speech audio URLs can expose private or consent-sensitive media. <br>
Mitigation: Use media you have rights and consent to use, prefer short-lived or controlled URLs, avoid secrets in URL query strings, and remove output artifacts that contain private links. <br>
Risk: The skill requires Alibaba Cloud DashScope credentials for LivePortrait requests. <br>
Mitigation: Provide credentials through environment or local credential files, use least-privileged access, and do not embed API keys in prompts, URLs, or generated request files. <br>


## Reference(s): <br>
- [LivePortrait source links](references/sources.md) <br>
- [Alibaba Cloud Model Studio video generation overview](https://help.aliyun.com/zh/model-studio/use-video-generation) <br>
- [LivePortrait image detection API reference](https://help.aliyun.com/zh/model-studio/liveportrait-detect-api) <br>
- [LivePortrait video generation API reference](https://help.aliyun.com/zh/model-studio/liveportrait-api) <br>
- [LivePortrait quick start](https://help.aliyun.com/zh/model-studio/liveportrait-quick-start/) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON request payloads and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes normalized request payloads and task evidence under output/aliyun-liveportrait/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
