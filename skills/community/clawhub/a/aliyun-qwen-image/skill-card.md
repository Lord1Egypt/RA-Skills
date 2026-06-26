## Description: <br>
Qwen Image helps an agent use Aliyun DashScope/Model Studio models for text-to-image generation, image editing, and mixed text/image Wan 2.6 workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awsl1110](https://clawhub.ai/user/awsl1110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate images, edit images, and produce mixed text/image outputs through Aliyun DashScope or Model Studio. It provides command examples, region selection guidance, dependency setup, and a bundled CLI script for the agent to run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and input images to external Aliyun DashScope or Model Studio APIs. <br>
Mitigation: Only submit prompts and images that are appropriate to share with the external provider, and confirm the intended region before running commands. <br>
Risk: The skill requires a DASHSCOPE_API_KEY and can also accept an API key as a command-line argument. <br>
Mitigation: Use a scoped key, prefer environment variables over command-line arguments, and avoid printing the full key in shared logs. <br>
Risk: Generated images and Wan 2.6 text outputs are saved to the selected local output directory. <br>
Mitigation: Review the output directory and generated files before reusing, publishing, or committing them. <br>


## Reference(s): <br>
- [Aliyun Model Studio text-to-image documentation](https://help.aliyun.com/zh/model-studio/text-to-image) <br>
- [PEP 723 inline script metadata](https://peps.python.org/pep-0723/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; the bundled CLI writes image files and optional text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and either uv or pip with Python 3.9 or newer.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
