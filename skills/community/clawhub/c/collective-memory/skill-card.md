## Description: <br>
Broadcast a single memory note to multiple AI-agent workspaces in one shot, upserting into MEMORY.md, AGENTS.md, TOOLS.md, USER.md, or another Markdown file across all targets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep Markdown-based memory notes consistent across local agent workspaces. It helps broadcast one note, preview changes, and idempotently update or append matching memory sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad trigger phrase could cause a memory broadcast when the user intended a narrower update. <br>
Mitigation: Require the agent to show the target files, content preview, and lookup key before multi-target writes, and use dry-run when intent is uncertain. <br>
Risk: Sensitive information may be written into multiple shared memory files. <br>
Mitigation: Avoid broadcasting secrets or credentials; when sensitive terms appear, warn the user and require explicit confirmation before writing. <br>
Risk: Auto-discovery may select more workspaces than intended. <br>
Mitigation: Prefer explicit targets for normal use and review discovered targets before committing changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/songhonglei/collective-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Files] <br>
**Output Format:** [Markdown guidance, shell command examples, human-readable status lines, optional JSON status, and Markdown file updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update or append sections in one or more local Markdown memory files; dry-run mode previews without writing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
