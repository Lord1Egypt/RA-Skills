## Description: <br>
Sets up and optimizes ComfyUI on AMD GPUs with DirectML on Windows, including compatibility fixes, model guidance, benchmarks, and configuration examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vilda007](https://clawhub.ai/user/vilda007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to configure a local Windows ComfyUI installation for AMD Radeon GPUs through DirectML, apply documented compatibility fixes, and choose settings and models that fit available VRAM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill patches a local ComfyUI installation file for AMD DirectML compatibility. <br>
Mitigation: Confirm the target ComfyUI directory, keep the generated backup, and review the resulting model_patcher.py change before continuing. <br>
Risk: Force-stopping a process can terminate the wrong Python process if the target is not checked first. <br>
Mitigation: Avoid Stop-Process -Force unless the exact ComfyUI process has been confirmed. <br>
Risk: Separately obtained downloader or benchmark scripts may run commands or downloads outside the included artifact. <br>
Mitigation: Inspect any separately obtained downloader or benchmark script before running it. <br>


## Reference(s): <br>
- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI) <br>
- [DirectML Documentation](https://learn.microsoft.com/en-us/windows/ai/directml/) <br>
- [AMD ROCm Blogs](https://rocm.blogs.amd.com/) <br>
- [CivitAI Models](https://civitai.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/vilda007/comfyui-directml-amd) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with command snippets, configuration examples, and a Python patching script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup and troubleshooting instructions for Windows ComfyUI with AMD DirectML.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
