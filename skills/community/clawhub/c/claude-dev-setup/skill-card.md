## Description: <br>
Complete Claude Code CLI integration with session management and APEX cognitive framework for setting up coding agents with persistent task tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dhruvarvindsingh](https://clawhub.ai/user/dhruvarvindsingh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to configure Claude Code CLI workflows, track background sessions, and add project guidance for persistent task management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may gain access to the user's Claude OAuth token and operate Claude Code under that account. <br>
Mitigation: Install only when this account-level access is intended; keep tokens out of logs, committed files, and reusable command strings. <br>
Risk: Default workflows use Claude Code with permission prompts disabled. <br>
Mitigation: Remove permission-skipping flags from routine workflows and require explicit user approval before starting background Claude Code tasks. <br>
Risk: Adding token extraction to shell startup files can expose credentials beyond the immediate task. <br>
Mitigation: Prefer per-command or short-lived environment variables and avoid placing OAuth token extraction in shell profiles. <br>


## Reference(s): <br>
- [Claude Dev Setup on ClawHub](https://clawhub.ai/dhruvarvindsingh/claude-dev-setup) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Claude Code CLI and an authenticated Claude account; includes local session-tracking and agent-instruction files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
