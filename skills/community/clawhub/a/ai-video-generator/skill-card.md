## Description: <br>
Generates videos from text prompts or images through Luma Dream Machine, Runway ML, and Kling AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaozewen0519](https://clawhub.ai/user/zhaozewen0519) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative users can use this skill to run text-to-video or image-to-video generation workflows against supported third-party video providers. It helps configure provider credentials, choose a platform, and save generated video files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video generation requests may consume paid provider quota or billing credits. <br>
Mitigation: Use the skill only with intended Luma, Runway, or Kling accounts and monitor provider quota before running long or repeated generations. <br>
Risk: Prompts and optional input images are sent to the selected third-party video provider. <br>
Mitigation: Avoid confidential prompts or private images unless the provider's data-handling terms are acceptable for the use case. <br>
Risk: Supplying API keys on the command line can expose credentials through shell history or process inspection. <br>
Mitigation: Prefer the documented environment variables for provider API keys and avoid passing secrets with the --api-key option in shared environments. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/zhaozewen0519/ai-video-generator) <br>
- [Luma documentation](https://docs.lumalabs.ai) <br>
- [Runway documentation](https://docs.runwayml.com) <br>
- [Kling AI](https://klingai.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown instructions with bash command examples; the script saves MP4 video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a provider API key through an environment variable or --api-key, plus a prompt, output filename, platform, and optional input image.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
