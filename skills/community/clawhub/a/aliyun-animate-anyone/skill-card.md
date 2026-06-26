## Description: <br>
Use when generating dance or motion-transfer videos with Alibaba Cloud Model Studio AnimateAnyone (`animate-anyone-gen2`) using a detected character image and an action template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative automation agents use this skill to prepare Alibaba Cloud Model Studio AnimateAnyone detect, template, and generation requests for dance or large body motion-transfer video workflows. <br>

### Deployment Geography for Use: <br>
China mainland (Beijing region) <br>

## Known Risks and Mitigations: <br>
Risk: Input media and generated request artifacts may expose personal, confidential, or biometric content through public URLs or local output files. <br>
Mitigation: Avoid confidential or biometric media, prefer short-lived public URLs, and clean up output/aliyun-animate-anyone/ when request payloads or task IDs are sensitive. <br>
Risk: Alibaba Cloud Model Studio requests require credentials and region-specific service access. <br>
Mitigation: Use a dedicated DASHSCOPE_API_KEY where possible and confirm access to the China mainland Beijing region before running workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-animate-anyone) <br>
- [Artifact source references](references/sources.md) <br>
- [Alibaba Cloud Model Studio video generation overview](https://help.aliyun.com/zh/model-studio/use-video-generation) <br>
- [AnimateAnyone quick start](https://help.aliyun.com/zh/model-studio/animateanyone-quick-start/) <br>
- [AnimateAnyone image detection API](https://help.aliyun.com/zh/model-studio/animate-anyone-detect-api) <br>
- [AnimateAnyone action template API](https://help.aliyun.com/zh/model-studio/animate-anyone-template-api) <br>
- [AnimateAnyone video generation API](https://help.aliyun.com/zh/model-studio/animateanyone-video-generation-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON files] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes normalized request payloads, detection outputs, template IDs, and task polling snapshots under output/aliyun-animate-anyone/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
