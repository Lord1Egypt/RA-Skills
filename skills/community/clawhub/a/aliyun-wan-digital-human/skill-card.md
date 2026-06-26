## Description: <br>
Use when generating talking, singing, or presentation videos from a single character image and audio with Alibaba Cloud Model Studio digital-human model `wan2.2-s2v`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to prepare Alibaba Cloud Model Studio digital-human detection and video generation requests for narrated avatars, singing portraits, and presentation-style talking-head clips. <br>

### Deployment Geography for Use: <br>
China (Beijing) region <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends image and audio URLs to Alibaba Cloud for digital-human generation, which can expose personal images or voice recordings. <br>
Mitigation: Use time-limited or access-controlled media URLs where possible and delete local request and evidence files when no longer needed. <br>
Risk: DashScope credentials are required and could be exposed if committed or reused too broadly. <br>
Mitigation: Use a dedicated restricted DashScope key and keep credentials in environment variables or local credential storage, not in source files. <br>


## Reference(s): <br>
- [Aliyun Model Studio video generation overview](https://help.aliyun.com/zh/model-studio/use-video-generation) <br>
- [Aliyun wan2.2-s2v video generation API reference](https://help.aliyun.com/zh/model-studio/wan-s2v-api) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON request files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes normalized request payloads and task evidence under output/aliyun-wan-digital-human/ by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
