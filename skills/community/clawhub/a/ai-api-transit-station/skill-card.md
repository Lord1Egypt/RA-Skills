## Description: <br>
API-Station helps agents query and use a third-party AI API service covering chat, image, video, audio, Midjourney, and related API examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QB-Chen](https://clawhub.ai/user/QB-Chen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to find endpoint patterns, authentication requirements, and example calls for a third-party AI API service that offers chat, image, video, audio, Midjourney, and task-query workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Use of a third-party AI API service may incur charges or expose account activity. <br>
Mitigation: Use a dedicated API token, monitor usage and billing, and confirm model pricing before running calls. <br>
Risk: Media upload workflows may send files to external services where URLs could be externally accessible or retained. <br>
Mitigation: Do not upload private, regulated, or sensitive media unless the provider is trusted and retention expectations are acceptable. <br>
Risk: The skill provides example calls for external APIs whose availability, limits, and responses can change. <br>
Mitigation: Check the linked provider documentation, handle failures, and apply conservative polling or rate limiting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QB-Chen/ai-api-transit-station) <br>
- [API documentation](https://winfull.apifox.cn/) <br>
- [API service and token management](https://api.winfull.cloud-ip.cc/) <br>
- [Image upload endpoint](https://imageproxy.zhongzhuan.chat/api/upload) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-supplied Bearer token; some workflows upload media to external endpoints and poll asynchronous tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
