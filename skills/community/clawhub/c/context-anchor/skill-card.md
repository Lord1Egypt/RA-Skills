## Description: <br>
Recover from context compaction by scanning workspace memory files and surfacing where an agent left off. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Boscoeuk](https://clawhub.ai/user/Boscoeuk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Context Anchor at session start, after context compaction, or during handoff to regain orientation from current-task notes, active context files, recent decisions, and open loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The briefing can expose sensitive, outdated, or unrelated information from workspace memory and active context files. <br>
Mitigation: Run it only in intended workspaces, prefer manual or post-compaction use when notes may be sensitive, and review the output before sharing or acting on it. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/Boscoeuk/context-anchor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Structured terminal briefing with Markdown-style sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local workspace memory and active context markdown files; no network access or credential use was reported by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
