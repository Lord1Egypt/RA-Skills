## Description: <br>
Provides portable ComfyUI workflow and API guidance for building, validating, troubleshooting, and submitting image or video workflows across unknown local, remote, or cloud installs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zambav](https://clawhub.ai/user/zambav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ComfyUI operators use this skill to build, validate, submit, and debug portable image/video workflows while discovering live server capabilities before relying on models, nodes, paths, or hardware assumptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connecting an agent to an untrusted ComfyUI server can expose prompts, workflow details, or generated outputs. <br>
Mitigation: Use only trusted ComfyUI servers and avoid putting secrets or private credentials in setup notes. <br>
Risk: Large batches or cloud GPU runs can create unexpected cost or resource usage. <br>
Mitigation: Confirm with the user before starting large batches or paid cloud GPU work. <br>
Risk: Retrieving outputs from hosted systems or interrupting active jobs can affect user data or running work. <br>
Mitigation: Confirm before retrieving hosted outputs or interrupting active jobs, and rely on user-provided server and output rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zambav/comfyui-complete-toolkit-skill) <br>
- [Setup and onboarding](references/setup.md) <br>
- [ComfyUI API guidance](references/api.md) <br>
- [Workflow patterns](references/workflow-patterns.md) <br>
- [Model-family guidance](references/models.md) <br>
- [Compatibility checks](references/compatibility.md) <br>
- [LoRA guidance](references/lora.md) <br>
- [Graph conventions](references/graph-conventions.md) <br>
- [Config template](references/config-template.md) <br>
- [Prompting guidance](references/prompting.md) <br>
- [Changelog](references/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON workflow examples, API endpoint references, and inline shell or code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts the agent to discover ComfyUI server capabilities and user-owned configuration before submitting workflows or retrieving outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and references/changelog.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
