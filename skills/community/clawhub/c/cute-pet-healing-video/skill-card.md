## Description: <br>
Generate vertical healing-style cute pet shorts with WeryAI, using text-to-video or a single pet image to create soft, warm, slow-paced videos for short-form feeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and agent users use this skill to prepare and submit cozy pet video generation requests to WeryAI. It helps expand short pet briefs into production prompts, choose supported model parameters, and return generated video URLs or actionable error details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WERYAI_API_KEY and can spend paid WeryAI credits during generation. <br>
Mitigation: Use a trusted installation, keep the API key out of the package, confirm parameters before running, and use dry-run/status commands when appropriate. <br>
Risk: Supplying a local image path can upload that image to WeryAI before video generation. <br>
Mitigation: Prefer public HTTPS image URLs; use local paths only after explicit consent and after confirming the image is intended for upload. <br>
Risk: Unsupported model parameters or content-safety filtering can cause generation failures. <br>
Mitigation: Follow the bundled WeryAI model constraints for duration, aspect ratio, resolution, audio, and negative prompts, and revise inputs when the API returns an error code. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zoucdr/cute-pet-healing-video) <br>
- [Publisher Profile](https://clawhub.ai/user/zoucdr) <br>
- [WeryAI Video API Reference](artifact/resources/WERYAI_VIDEO_API.md) <br>
- [WeryAI Video Tasks API](https://api.weryai.com) <br>
- [WeryAI Models and Upload API](https://api-growth-agent.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON command payloads and returned video URLs or error details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, network access, and WeryAI credits for non-dry-run generation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
