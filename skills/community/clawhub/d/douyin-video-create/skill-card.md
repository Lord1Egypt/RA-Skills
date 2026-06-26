## Description: <br>
根据主题自动搜索整理信息，生成多风格视频脚本，并调用数字人平台创建完整短视频。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyang399](https://clawhub.ai/user/chenyang399) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and developers use this skill to turn a topic into organized source notes, short-video scripts, and digital-avatar video generation requests for Douyin-style videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated scripts or source material may be uploaded to third-party avatar video providers. <br>
Mitigation: Use non-sensitive scripts, confirm the selected provider before running the pipeline, and review the content before any API submission. <br>
Risk: Provider API calls may incur costs or use credentials beyond the intended scope. <br>
Mitigation: Use scoped API keys, confirm provider pricing and request behavior, and avoid sharing long-lived credentials. <br>
Risk: The pipeline writes generated scripts, reports, and provider responses to local output directories. <br>
Mitigation: Choose an appropriate output directory and review generated files before sharing or retaining them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chenyang399/douyin-video-create) <br>
- [HeyGen](https://www.heygen.com) <br>
- [D-ID](https://www.d-id.com) <br>
- [Synthesia](https://www.synthesia.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated search results, organized data, scripts, video provider responses, and reports under an output timestamp directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
