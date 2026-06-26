## Description: <br>
自动化发布抖音视频。上传到抖音平台。全自动操作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuhongfeii2](https://clawhub.ai/user/xuhongfeii2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and agents use this skill to prepare Douyin login cookies and publish local videos to Douyin Creator Center with titles, tags, covers, and optional scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a metered third-party platform flow and can deduct points before publishing. <br>
Mitigation: Confirm platform authorization details and point cost before each publish request. <br>
Risk: The default platform base URL uses unencrypted HTTP for platform credentials. <br>
Mitigation: Set CHANJING_PLATFORM_BASE_URL to a trusted HTTPS endpoint before use. <br>
Risk: Saved Douyin cookie files can represent an active logged-in account session. <br>
Mitigation: Protect cookie files, avoid sharing them, and delete or rotate them when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuhongfeii2/douyin-upload-mul-cookie) <br>
- [Publisher profile](https://clawhub.ai/user/xuhongfeii2) <br>
- [Douyin Creator Center](https://creator.douyin.com/) <br>
- [Douyin Creator upload page](https://creator.douyin.com/creator-micro/content/upload) <br>
- [easyclaw user portal](http://easyclaw.bar/shuziren/user) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch local Playwright browser automation and create local cookie and log files when the generated commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
