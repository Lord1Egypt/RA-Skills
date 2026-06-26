## Description: <br>
Manages hierarchical OpenClaw session channels for splitting work, creating sub-channels, tracking status, and saving local tree state with inheritance and health monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuxnd](https://clawhub.ai/user/kukuxnd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and OpenClaw users use this skill to organize work across halls, universes, worlds, forests, trees, and task, QA, or branch channels. It supports local context switching, hierarchy review, and health monitoring for session organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hall, tree, channel, or context names are saved locally and may expose sensitive details if users include secrets, credentials, or personal information. <br>
Mitigation: Use non-sensitive labels and avoid placing secrets, credentials, or sensitive personal details in hierarchy or context names. <br>
Risk: Create and switch actions change local session-organization state and can make context tracking confusing if invoked against the wrong path. <br>
Mitigation: Use explicit commands and review the intended hierarchy path before running create or switch operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kukuxnd/channel-tree) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON state files] <br>
**Output Format:** [Markdown guidance with command examples and local JSON state updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists hierarchy state in /root/.openclaw/workspace/channel_tree/universe.json when the helper script is run.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
