## Description: <br>
Use when generating expressive portrait videos from a person image and speech audio with Alibaba Cloud Model Studio EMO (`emo-v1`), especially non-Wan avatar clips with stronger expression style control from a detected portrait image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare Alibaba Cloud Model Studio EMO detection and generation requests for portrait talking-head videos. It helps normalize request payloads, bounding boxes, style level selection, and output evidence paths for workflows that use public portrait-image and speech-audio URLs. <br>

### Deployment Geography for Use: <br>
China mainland (Beijing region) <br>

## Known Risks and Mitigations: <br>
Risk: Portrait image and speech audio URLs must be reachable for Alibaba Cloud processing, which can expose sensitive media if broad public URLs are used. <br>
Mitigation: Use non-sensitive media when possible, prefer limited-lifetime signed URLs, and avoid embedding private assets in persistent public locations. <br>
Risk: The skill requires Alibaba Cloud credentials for EMO workflows. <br>
Mitigation: Use limited-purpose API keys or scoped credentials, keep credentials out of generated request files, and rotate them according to local security policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-emo) <br>
- [Video generation overview, EMO entry](https://help.aliyun.com/zh/model-studio/use-video-generation) <br>
- [EMO video generation API reference](https://help.aliyun.com/zh/model-studio/emo-api) <br>
- [Artifact source references](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes normalized request payloads and related evidence under output/aliyun-emo/ by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
