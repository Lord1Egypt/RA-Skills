## Description: <br>
Generate images using DashScope wan2.6-t2i model (Tongyi Wanxiang) when a user asks to create images, illustrations, or visual content through DashScope. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoyang78](https://clawhub.ai/user/chaoyang78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to have an agent generate DashScope image-generation commands and retrieve PNG images or image URLs from Chinese or English prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local dashscope-imagegen.py helper that is referenced but not included in the artifact. <br>
Mitigation: Review and trust the local helper before installation or execution. <br>
Risk: The skill requires DASHSCOPE_API_KEY, which is a sensitive credential. <br>
Mitigation: Store the API key only in the expected local environment configuration and avoid exposing it in prompts, logs, or shared output. <br>
Risk: Generated images may be written to a caller-selected output directory. <br>
Mitigation: Use an output directory intended for generated assets and review files before sharing or committing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chaoyang78/dashscope-imagegen) <br>
- [Publisher profile](https://clawhub.ai/user/chaoyang78) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Markdown with inline bash commands; generated outputs are PNG files or image URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY; supports size, count, negative prompt, output directory, and URL-only options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
