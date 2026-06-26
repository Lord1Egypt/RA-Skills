## Description: <br>
Generate, edit, or compose images with EchoFlow API using Nano Banana Pro (Gemini 3 Pro Image), including multi-image composition with up to 14 input images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjx15296694073](https://clawhub.ai/user/zjx15296694073) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate new images, edit existing images, or combine multiple images through a third-party EchoFlow API gateway. It is suited for workflows that need a saved image file and an attachable MEDIA path returned to the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to EchoFlow or another configured OpenAI-compatible API endpoint. <br>
Mitigation: Use this skill only with prompts and images approved for that third-party service, and avoid private or sensitive image inputs unless the endpoint is explicitly approved. <br>
Risk: The script can fall back to OPENAI_API_KEY or GEMINI_API_KEY if ECHOFLOW_API_KEY is not set, which could send unrelated credentials to the configured endpoint. <br>
Mitigation: Set ECHOFLOW_API_KEY explicitly and run the skill in an environment that does not expose unrelated provider keys. <br>
Risk: The configurable API base can redirect requests to a different service, changing where credentials, prompts, and image data are processed. <br>
Mitigation: Keep the default EchoFlow base URL unless a reviewed endpoint is required, and verify any custom API base before use. <br>


## Reference(s): <br>
- [EchoFlow API Reference](references/echoflow_api.md) <br>
- [EchoFlow API Homepage](https://api.echoflow.cn/) <br>
- [ClawHub skill page](https://clawhub.ai/zjx15296694073/echoflow-banana-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Console text containing saved image paths and MEDIA tokens; generated or edited images are written as image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an API key and can use prompt text plus up to 14 input image files; supported output resolutions are 1K, 2K, and 4K.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
