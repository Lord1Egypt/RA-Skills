## Description: <br>
fal.ai API integration with managed API key authentication for running AI models for image generation, video generation, audio processing, and related fal.ai workloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to call fal.ai queue endpoints through Maton-managed authentication for image generation, video creation, image upscaling, text-to-speech, transcription, and other model inference tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, media URLs, and model parameters to external Maton and fal.ai service boundaries. <br>
Mitigation: Avoid sending sensitive prompts or media unless the user accepts those service boundaries. <br>
Risk: MATON_API_KEY and returned connection or session URLs can grant access to managed API connections. <br>
Mitigation: Keep credentials and connection URLs private, and avoid pasting them into shared logs or transcripts. <br>
Risk: The documented workflows include state-changing actions such as creating, deleting, and canceling connections or model requests. <br>
Mitigation: Review those actions with the user before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byungkyu/fal-ai-api) <br>
- [Maton homepage](https://maton.ai) <br>
- [fal.ai Documentation](https://fal.ai/docs) <br>
- [fal.ai Model Gallery](https://fal.ai/models) <br>
- [fal.ai Queue API Reference](https://fal.ai/docs/model-endpoints/queue) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline Python, JavaScript, bash, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a configured fal.ai connection through Maton.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
