## Description: <br>
AI image generation and editing skill for text-to-image, image-and-text generation, and style conversion with multiple aspect ratios and standard, 2K, and 4K resolution options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiujiahong](https://clawhub.ai/user/qiujiahong) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to generate or edit images from prompts, choose aspect ratio and resolution-specific Gemini Flash Image models, and save generated image files for downstream use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and API credentials are sent to the configured image-generation endpoint, and the default endpoint is a third-party API proxy. <br>
Mitigation: Use an official or trusted provider endpoint where supported, avoid sensitive prompts, and install only if the endpoint and credential handling are acceptable. <br>
Risk: Generated image files are written to disk at a user-provided path or the current working directory. <br>
Mitigation: Review output paths before execution and verify where generated files are saved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiujiahong/ai-image-gen) <br>
- [Publisher profile](https://clawhub.ai/user/qiujiahong) <br>
- [Default Gemini-compatible endpoint](https://code.newcli.com/gemini) <br>
- [FoxCode API key registration](https://foxcode.rjj.cc/auth/register?aff=R0P5ZY) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown instructions with shell commands and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated image output to the requested path or to generated_image.<ext> in the current working directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
