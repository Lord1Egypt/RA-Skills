## Description: <br>
Maintains and restores project context across OpenClaw sessions, tracks active projects, manages tasks, switches projects, and summarizes current progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deus-pandora](https://clawhub.ai/user/deus-pandora) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to preserve project continuity across sessions, restore previous work context, track pending tasks, and switch between active projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved project context may include secrets, credentials, private customer data, or sensitive command history. <br>
Mitigation: Do not store sensitive data in project notes or context, and periodically review or delete saved project memory files when they are no longer needed. <br>
Risk: Restored project context may be outdated or incomplete after time away from a project. <br>
Mitigation: Review restored summaries, pending tasks, and last-session details before relying on them for current work. <br>


## Reference(s): <br>
- [Context Engine API Reference](references/API.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/deus-pandora/context-engine-deus) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists local project and session context between OpenClaw sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md metadata, CHANGELOG released 2026-02-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
