## Description: <br>
Prevent context loss during LLM compaction with Write-Ahead Logging, a working buffer, and recovery steps that preserve decisions, preferences, values, and paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rustyorb](https://clawhub.ai/user/rustyorb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to keep critical working context available across LLM compaction events. It guides the agent to capture exact details before responding, maintain local working-memory files, and recover recent task state after compaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist broad conversation details in local memory files. <br>
Mitigation: Use it only in workspaces where persistent conversation memory is intended, and avoid sharing secrets or regulated data while it is active. <br>
Risk: SESSION-STATE.md and files under memory/ can retain sensitive task context after the active session ends. <br>
Mitigation: Review and delete those files regularly, especially before sharing a workspace or changing tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rustyorb/compaction-survival) <br>
- [Publisher profile](https://clawhub.ai/user/rustyorb) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Files] <br>
**Output Format:** [Markdown guidance and local memory file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates SESSION-STATE.md and files under memory/ when active.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
