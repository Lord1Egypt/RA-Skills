## Description: <br>
Generates, edits, and composes images through the EchoFlow API using Nano Banana Pro / Gemini 3 Pro Image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjx15296694073](https://clawhub.ai/user/zjx15296694073) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to create new images, edit a provided image, or combine up to 14 images through EchoFlow-hosted image models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected input images, and the EchoFlow API key are sent to a third-party API provider. <br>
Mitigation: Install and use this skill only when EchoFlow is trusted for the intended prompts, images, and credentials. <br>
Risk: Passing the API key on the command line or changing the API base can expose credentials to process history or an untrusted host. <br>
Mitigation: Prefer the ECHOFLOW_API_KEY environment variable and keep the default EchoFlow endpoint unless another host is fully trusted. <br>
Risk: The documented Linux uv installer uses a curl-to-shell command. <br>
Mitigation: Verify the installer source before running it or install uv through a trusted package manager. <br>


## Reference(s): <br>
- [EchoFlow API Reference](references/echoflow_api.md) <br>
- [EchoFlow API](https://api.echoflow.cn/) <br>
- [ClawHub skill page](https://clawhub.ai/zjx15296694073/echoflow-banana) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG image files with terminal status output and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and ECHOFLOW_API_KEY; supports 1K, 2K, and 4K output resolutions and up to 14 input images for editing or composition.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
