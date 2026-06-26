## Description: <br>
Doubao Image Video Skill helps agents use ByteDance/Doubao through Volcengine ARK for text-to-image generation, image editing, text-to-video generation, and task status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenkangwei](https://clawhub.ai/user/wenkangwei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to submit prompts or image URLs to Volcengine ARK, receive generated image or video results, and check asynchronous video task status. It is intended for workflows where the user supplies their own ARK API key and reviews generated media before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and task metadata are sent to Volcengine ARK under the user's API key. <br>
Mitigation: Use a limited ARK API key, avoid sensitive prompts or private image URLs, and follow the Volcengine ARK terms for submitted data. <br>
Risk: The artifact presents watermark, logo, attribution, or ownership mark removal as a default image-editing workflow. <br>
Mitigation: Use the edit workflow only for content you own or are explicitly authorized to modify. <br>
Risk: The security guidance states that the advertised edit capability may not be implemented in the shipped backend script. <br>
Mitigation: Verify the edit action in a controlled test before depending on it in an agent workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wenkangwei/doubao-skill) <br>
- [Volcengine ARK documentation](https://www.volcengine.com/docs/82379) <br>
- [Volcengine ARK console](https://console.volcengine.com/ark) <br>
- [Integration guide](references/INTEGRATION_GUIDE.md) <br>
- [Quick start reference](references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON API results with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARK_API_KEY. Image generation returns image URLs, asynchronous video generation returns task IDs, synchronous video generation returns result URLs, and status checks return task state.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
