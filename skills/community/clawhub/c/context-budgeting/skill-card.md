## Description: <br>
Manage and optimize OpenClaw context window usage via partitioning, pre-compression checkpointing, and information lifecycle management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SarielWang93](https://clawhub.ai/user/SarielWang93) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill to manage long-running sessions by partitioning context, preserving key decisions before compaction, and reducing context-related latency or information loss. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may change local OpenClaw memory or checkpoint state and run its bundled compaction script. <br>
Mitigation: Review the checkpoint content and script before execution, and run it only in an intended OpenClaw workspace where local state changes are expected. <br>
Risk: The bundled script targets a fixed local workspace path and invokes the OpenClaw CLI. <br>
Mitigation: Confirm or adapt the workspace path before use, and verify the OpenClaw CLI command matches the active environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide updates to HOT_MEMORY.md and execution of the bundled checkpoint script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
