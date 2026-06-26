## Description: <br>
上下文记忆球 helps an agent save, load, merge, and archive conversation-context snapshots as reusable memory balls for session switching and context recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to checkpoint task context, restore previous work, and manage multiple active sessions through structured memory-ball summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved memory balls may capture secrets, personal data, or project-sensitive details. <br>
Mitigation: Preview and redact memory contents before saving, and avoid storing credentials or personal data. <br>
Risk: Loading or merging memory balls can reintroduce stale, incorrect, or unrelated context into an active session. <br>
Mitigation: Require preview and confirmation before restore or merge, and keep memory scoped to one user and project. <br>
Risk: The artifact includes example mempalace shell commands that depend on a separate local tool. <br>
Mitigation: Run those commands only when the local tool is independently installed and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/context-memory-ball) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with optional shell command examples and structured memory-ball fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include memory-ball IDs, topics, summaries, decisions, pending work, token counts, and active, complete, or archived states.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
