## Description: <br>
This skill compares Claude Code and OpenClaw skill directories, reports in-sync, missing, and conflicting skills, and performs bidirectional synchronization with user confirmation before changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rushingai](https://clawhub.ai/user/rushingai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to compare and synchronize local Claude Code and OpenClaw skill directories while reviewing a report before any copy or overwrite action is applied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk approval can copy unfamiliar or untrusted skills into an active skill directory. <br>
Mitigation: Review the sync report before approving changes and avoid bulk 'all' approval for skills you have not inspected. <br>
Risk: Conflict resolution can overwrite local SKILL.md content. <br>
Mitigation: Use the conflict preview and skip any conflict until the preferred version has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rushingai/claude-skill-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown report with interactive confirmation prompts and JSON metadata files when syncing to OpenClaw] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs sync summaries and may write SKILL.md plus OpenClaw _meta.json files after user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
