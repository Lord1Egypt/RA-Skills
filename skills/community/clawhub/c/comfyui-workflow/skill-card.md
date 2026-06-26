## Description: <br>
Comfyui Workflow helps agents inspect and run ComfyUI image and video workflows, configure prompts and media inputs, and save generated outputs from a running ComfyUI server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiqiliu2](https://clawhub.ai/user/yiqiliu2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, creators, and external users use this skill to inspect, configure, and execute ComfyUI workflow templates for image generation, image editing, and video synthesis. It is intended for environments where the user controls the ComfyUI server, model files, input media, and output directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can interact with a configured ComfyUI server and upload user-provided media files for workflow execution. <br>
Mitigation: Use a trusted ComfyUI instance that you start and configure yourself, require authentication when appropriate, and avoid sending sensitive media to untrusted remote hosts. <br>
Risk: The skill can save generated images, video, audio, and related output metadata to local directories. <br>
Mitigation: Write outputs to approved directories and review generated files and metadata before sharing them outside the environment. <br>
Risk: Model inventory and workflow maintenance behavior can expose local model paths or stale example entries if used without review. <br>
Mitigation: Limit inventory scans and documentation updates to directories you approve, and replace example inventory data with the user's actual reviewed setup before relying on it. <br>


## Reference(s): <br>
- [README](artifact/README.md) <br>
- [Practical Guide](artifact/PRACTICAL_GUIDE.md) <br>
- [Workflow Summary](artifact/WORKFLOWS_SUMMARY.md) <br>
- [Architecture](artifact/references/architecture.md) <br>
- [Maintenance](artifact/references/maintenance.md) <br>
- [Prompting Guide](artifact/references/prompting-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python examples, and JSON configuration snippets; executed workflows save generated media files locally.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interacts with a user-configured ComfyUI server and writes generated outputs to the selected local output directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
