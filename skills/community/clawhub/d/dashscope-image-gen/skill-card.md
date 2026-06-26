## Description: <br>
Generate images through Alibaba DashScope compatible-mode using qwen-image-max. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DHDragon](https://clawhub.ai/user/DHDragon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate image files from text prompts through Alibaba DashScope compatible-mode, including scriptable CLI workflows and OpenAI-style /images/generations calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to Alibaba DashScope and may consume the user's DashScope quota. <br>
Mitigation: Use the skill only with prompts appropriate for DashScope processing and confirm account quota expectations before running generation. <br>
Risk: The tool can read a DashScope key from ~/.openclaw/openclaw.json when DASHSCOPE_API_KEY is not set. <br>
Mitigation: Set DASHSCOPE_API_KEY explicitly when a specific credential should be used, and avoid passing secrets with --api-key. <br>
Risk: Changing the base URL can send prompts and credentials to an untrusted endpoint. <br>
Mitigation: Keep the default DashScope compatible-mode base URL unless the replacement endpoint is trusted. <br>
Risk: The requested output path is written with the generated image and may overwrite an existing file. <br>
Mitigation: Choose the --out path deliberately and check for existing files before running the command. <br>


## Reference(s): <br>
- [DashScope OpenAI Compatible-mode notes](references/dashscope-openai-compatible.md) <br>
- [DashScope OpenAI-compatible endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance with bash commands and a Python CLI that writes image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DashScope API key; sends prompts to DashScope and writes the generated image to the requested output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
