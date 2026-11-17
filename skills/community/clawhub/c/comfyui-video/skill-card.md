## Description:

Automates AI video generation with ComfyUI and LTX-2.3 for text-to-video, image-to-video, batch scene rendering, progress monitoring, fault recovery, and performance tuning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3165458](https://clawhub.ai/user/a3165458)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video creators use this skill to guide ComfyUI LTX-2.3 text-to-video, image-to-video, batch scene rendering, monitoring, and troubleshooting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SSH tunneling and remote shell commands can affect a ComfyUI host if used on systems the user does not control.

Mitigation: Use the skill only with authorized ComfyUI hosts, review each command before execution, and close background SSH tunnels when finished.

Risk: Browser-console JavaScript changes the active ComfyUI workflow graph.

Mitigation: Run the script only in the intended ComfyUI session, review scene parameters before running, and reload the workflow before generation.

Risk: Large LTX-2.3 generation jobs can exhaust VRAM or leave long-running workloads active.

Mitigation: Run one generation at a time, monitor logs and output files, and restart ComfyUI after out-of-memory failures.

## Reference(s):

- [Workflow Nodes Reference](references/workflow_nodes.md)
- [Tips & Best Practices](references/tips.md)
- [ClawHub Skill Page](https://clawhub.ai/a3165458/skills/comfyui-video)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser-console JavaScript for ComfyUI and SSH commands for authorized remote hosts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
