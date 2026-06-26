## Description: <br>
Alibaba Cloud Bailian Qwen Image 2.0 image generation supports text-to-image and image-to-image workflows for product promotion, e-commerce editing, marketing material creation, Python API usage, CLI usage, and ComfyUI custom nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[navygo](https://clawhub.ai/user/navygo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and e-commerce teams use this skill to generate or edit images with Alibaba Cloud Bailian Qwen Image 2.0 through a Python API, command-line script, or ComfyUI workflow. It is suited for product promotion images, background replacement, style transfer, marketing materials, and creative image editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected reference images are sent to Alibaba Cloud Bailian/DashScope for generation. <br>
Mitigation: Use only approved prompts and images, and avoid submitting sensitive or regulated content unless the deployment is approved for that data. <br>
Risk: The skill requires a DashScope API key in the execution environment. <br>
Mitigation: Store the key in a limited .env file or environment variable, avoid committing it, and rotate it if exposure is suspected. <br>
Risk: The Python dependencies handle HTTP requests and image processing. <br>
Mitigation: Pin patched versions of requests and Pillow for production use. <br>


## Reference(s): <br>
- [Alibaba Cloud DashScope API endpoint](https://dashscope.aliyuncs.com/api/v1) <br>
- [ClawHub skill page](https://clawhub.ai/navygo/bailian-image-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local image files through the CLI or Python API and image tensors through ComfyUI nodes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
