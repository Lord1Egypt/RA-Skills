## Description: <br>
Automates ComfyUI workflows by collecting required assets, executing tasks via the RunningHub API, and returning execution status and results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuxiaosa86-cmd](https://clawhub.ai/user/wuxiaosa86-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to collect workflow inputs, upload required media, run ComfyUI workflows through RunningHub, and review task status and results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow prompts, node parameters, selected local media files, image URLs, optional webhook URLs, and the RunningHub API key may be sent to RunningHub. <br>
Mitigation: Use only non-confidential inputs, review RunningHub privacy and retention terms, avoid regulated files unless approved, and provide only webhook endpoints you control. <br>
Risk: Workflow execution can consume external service resources or run with unintended parameters. <br>
Mitigation: Review workflow identifiers, selected nodes, collected materials, and execution confirmation prompts before running; test workflows in RunningHub when practical. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuxiaosa86-cmd/comfyui-automation-skill) <br>
- [RunningHub](https://www.runninghub.cn) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or console text with JSON task responses and execution status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include RunningHub task IDs, status polling updates, uploaded file names, and final workflow result payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
