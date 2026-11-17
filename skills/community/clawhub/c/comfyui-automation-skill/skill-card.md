## Description:

Automates ComfyUI workflow execution by collecting required inputs, calling RunningHub APIs, monitoring task status, and returning results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuxiaosa86-cmd](https://clawhub.ai/user/wuxiaosa86-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run ComfyUI workflows through RunningHub by supplying a workflow ID or nickname, required media or prompt inputs, and optional webhook details. It is useful for image, video, audio, and multimodal workflow automation where task status and results need to be returned to the agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RunningHub API keys are entered through an interactive prompt and may be exposed if terminal output is visible or shared.

Mitigation: Use a dedicated, low-privilege RunningHub API key and rotate it if it was exposed during setup or use.

Risk: The skill can upload user-provided local files to RunningHub without strong path scoping or a separate upload confirmation.

Mitigation: Run the skill in a restricted working directory or sandbox and provide only intended, non-sensitive file paths.

Risk: The skill depends on local Python dependencies and network access to RunningHub.

Mitigation: Review and pin dependencies before installation, and allow network access only for the intended RunningHub workflow operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuxiaosa86-cmd/skills/comfyui-automation-skill)
- [RunningHub](https://www.runninghub.cn)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Console text with JSON task status and result payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workflow IDs, task IDs, status updates, uploaded file names, error messages, and RunningHub result data.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
