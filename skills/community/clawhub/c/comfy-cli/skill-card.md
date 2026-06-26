## Description: <br>
Install, manage, and run ComfyUI instances. Use when setting up ComfyUI, launching servers, installing/updating/debugging custom nodes, downloading models from CivitAI/HuggingFace, managing workspaces, running API workflows, or troubleshooting node conflicts with bisect. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johntheyoung](https://clawhub.ai/user/johntheyoung) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install, configure, launch, update, and troubleshoot local ComfyUI workspaces, custom nodes, models, and API workflow runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install code and alter local ComfyUI workspaces, custom nodes, dependencies, and downloaded model files. <br>
Mitigation: Review generated commands before execution, keep snapshots or backups for important workspaces, and avoid untrusted model URLs or custom nodes. <br>
Risk: Provider tokens for gated CivitAI or Hugging Face models may be configured or stored for CLI use. <br>
Mitigation: Use least-privilege provider tokens and rotate or remove credentials when they are no longer needed. <br>
Risk: CLI analytics may be enabled depending on local configuration. <br>
Mitigation: Disable tracking if analytics collection is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johntheyoung/comfy-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that install packages, manage local files, download models, configure tokens, launch services, or publish custom nodes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
