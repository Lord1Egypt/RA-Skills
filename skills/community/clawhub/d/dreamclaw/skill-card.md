## Description: <br>
Auto Dream helps OpenClaw maintain durable local memory by appending daily log entries, consolidating them into categorized memory files, and rebuilding a concise MEMORY.md index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyunxh](https://clawhub.ai/user/cyunxh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to preserve user preferences, feedback, project context, and reference pointers across OpenClaw sessions. It supports manual append, review, consolidation, and index maintenance workflows for a single-user local workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read recent OpenClaw conversation records and convert selected details into durable local memory. <br>
Mitigation: Avoid running Dream mode after sessions that contain secrets, credentials, regulated personal data, or confidential project details. <br>
Risk: Consolidation can change long-term memory files that future agent sessions may rely on. <br>
Mitigation: Review the .auto-dream memories and MEMORY.md index before relying on or pruning stored memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyunxh/dreamclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance, CLI output, memory files, and generated consolidation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes append-only daily logs, categorized Markdown memory files, a MEMORY.md index, and a temporary dream prompt under the local OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
