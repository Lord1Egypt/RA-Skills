## Description: <br>
Enhanced terminal AI agent orchestrator with parallel execution, health checks, and workflow presets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qriiz112](https://clawhub.ai/user/qriiz112) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate terminal AI agents for discovery, health checks, single-agent runs, parallel or sequential task files, workflow presets, and JSON-formatted agent output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch and parallel task files can coordinate powerful terminal agent workflows. <br>
Mitigation: Review task files before running batch or parallel modes, especially when prompts or command flags come from untrusted sources. <br>
Risk: External packages and optional agent CLIs execute runtime code that was not included in the reviewed skill artifacts. <br>
Mitigation: Verify the external acpx npm package and any optional agent CLIs before installation or use. <br>
Risk: No-confirm or yolo-style execution flags can reduce oversight of agent actions. <br>
Mitigation: Avoid untrusted prompts and no-confirm execution flags unless the environment is isolated and the task has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qriiz112/acpx-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and task-file examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can also request JSON-formatted agent output through the documented acpx json command.] <br>

## Skill Version(s): <br>
4.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
