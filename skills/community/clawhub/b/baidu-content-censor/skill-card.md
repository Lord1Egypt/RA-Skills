## Description: <br>
Provides Baidu Cloud text and image content moderation APIs that return detailed JSON audit results and user-facing conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HeKe-UESTC](https://clawhub.ai/user/HeKe-UESTC) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit user-selected text, image URLs, or local image files for Baidu Cloud content safety review and present the returned moderation findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Moderated text, image URLs, and local image file contents are sent to Baidu Cloud. <br>
Mitigation: Use the skill only for content that is allowed to leave the local environment and is appropriate for Baidu Cloud processing. <br>
Risk: Baidu API credentials and cached access tokens could expose moderation access if committed, logged, or left behind after rotation. <br>
Mitigation: Store BCE_SINAN_AK and BCE_SINAN_SK only in environment variables, avoid logging credential-bearing URLs, rotate credentials when needed, and delete the local token cache during rotation or uninstall. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HeKe-UESTC/baidu-content-censor) <br>
- [Baidu text moderation endpoint](https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined) <br>
- [Baidu image moderation endpoint](https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON moderation results with concise Markdown or plain-text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Baidu audit fields such as request log ID, conclusion, conclusion type, and detailed result data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
