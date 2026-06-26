## Description: <br>
Synchronizes audio with lip movements in videos using the NewportAI/Dreamface LipSync 2.0 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hy-1990](https://clawhub.ai/user/hy-1990) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to configure an agent for video lip synchronization workflows that submit video and audio inputs to the LipSync 2.0 cloud API and retrieve asynchronous results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video and audio inputs may be uploaded to third-party cloud services for processing. <br>
Mitigation: Use the skill only when NewportAI/Dreamface storage, retention, regional handling, and data-use terms are acceptable for the media being processed. <br>
Risk: The required API key may incur usage or billing if exposed or misused. <br>
Mitigation: Use a dedicated DREAMLIPSYNC_API_KEY where possible, keep it out of shared prompts and logs, and monitor provider usage. <br>
Risk: Private, regulated, proprietary, or biometric media may create compliance obligations when sent to the provider. <br>
Mitigation: Avoid uploading sensitive media unless the provider's handling terms satisfy the applicable privacy, consent, and compliance requirements. <br>


## Reference(s): <br>
- [Dream LipSync ClawHub page](https://clawhub.ai/hy-1990/dream-lipsync) <br>
- [LipSync 2.0 API reference](https://api.newportai.com/api-reference/LipSync-2.0) <br>
- [DreamAPI getting started](https://api.newportai.com/api-reference/get-started) <br>
- [Dreamface tools](https://tools.dreamfaceapp.com/home) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DREAMLIPSYNC_API_KEY and may describe upload, polling, and result retrieval steps.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
