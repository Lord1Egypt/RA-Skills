## Description: <br>
Provides Bash wrappers for Doubao/Volcengine ARK text-to-image, image-editing, text-to-video, and task-status APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenkangwei](https://clawhub.ai/user/wenkangwei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to call Doubao/Volcengine ARK from shell workflows, generate or edit images, start text-to-video jobs, check task status, and save generated media locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The image-editing flow defaults to watermark or logo removal, which can be inappropriate for content the user does not own or have permission to modify. <br>
Mitigation: Use image editing only with authorized content and avoid watermark or logo removal unless the user owns the material or has explicit permission. <br>
Risk: ARK_API_KEY handling guidance can lead users to expose credentials in shells, screenshots, command history, or shared configuration files. <br>
Mitigation: Use scoped or temporary keys, store them in an approved secret store or protected environment, avoid sharing them in prompts or screenshots, and rotate keys periodically. <br>
Risk: Prompts, source images, and generated media are sent to Volcengine ARK and generated files are saved locally under the skill data directory. <br>
Mitigation: Send only prompts and images authorized for the external service and periodically delete generated media that may contain sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wenkangwei/doubao-skill-v2) <br>
- [Volcengine ARK API documentation](https://www.volcengine.com/docs/82379/1520757?lang=zh#y2hhTyHB) <br>
- [Volcengine ARK console](https://console.volcengine.com/ark) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Files, Configuration] <br>
**Output Format:** [JSON responses with generated media URLs, task IDs, local file paths, and downloaded image or video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARK_API_KEY and a shell environment with curl; jq is recommended for JSON formatting.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
