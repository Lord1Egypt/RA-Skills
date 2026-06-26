## Description: <br>
Generates images from Chinese prompts through NVIDIA NIM or SiliconFlow APIs, supporting models such as flux.2-klein-4b, Kolors, and Qwen-Image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lianghaoxun](https://clawhub.ai/user/lianghaoxun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to turn prompt text into locally saved PNG image files through configured NVIDIA NIM or SiliconFlow provider credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to NVIDIA or SiliconFlow cloud APIs. <br>
Mitigation: Avoid sensitive personal, business, or regulated content in prompts and review provider terms before use. <br>
Risk: Provider API keys are stored in a local plaintext config.json file. <br>
Mitigation: Use restrictive filesystem permissions or adapt the scripts to read credentials from environment variables or a secret store on shared machines. <br>
Risk: Generated images are written to local files that may later be shared by an agent. <br>
Mitigation: Review generated images and file paths before forwarding them outside the local workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lianghaoxun/ai-photo-pro) <br>
- [NVIDIA NIM](https://nim.nvidia.com/) <br>
- [SiliconFlow](https://cloud.siliconflow.cn/i/IOo0eaWy) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell and Python examples; runtime scripts return PNG file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved under the skill scripts directory in img_data.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
