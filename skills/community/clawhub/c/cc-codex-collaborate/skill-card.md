## Description: <br>
Coordinates Claude Code and Codex in a milestone-based collaboration loop where Claude Code discovers, plans, implements, and fixes while Codex performs adversarial planning and read-only milestone reviews with working documents stored under docs/cccc. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayl1n](https://clawhub.ai/user/jayl1n) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate Claude Code implementation with Codex planning, milestone, and final reviews. It is intended for repository-based coding work where plans, state, reviews, and generated context are tracked under docs/cccc. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent hooks can alter Claude Code stop behavior and automate continuation. <br>
Mitigation: Keep loop automation off unless explicitly intended; enable it only with the loop-start command after reviewing .claude/settings.json, and use the loop-stop command to disable it. <br>
Risk: Broad project context may be sent to Codex during planning and milestone reviews. <br>
Mitigation: Use the skill only in repositories where Codex receiving project context is acceptable, and inspect docs/cccc/context-bundle.md before reviews on sensitive projects. <br>
Risk: Maintenance commands can rewrite workflow state or interact with preexisting configuration. <br>
Mitigation: Review configuration and backups before using doctor, import, reset, or repair commands against untrusted repositories or existing project configs. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/jayl1n/cc-codex-collaborate) <br>
- [Publisher profile](https://clawhub.ai/user/jayl1n) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, generated project documents, and review summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates and updates docs/cccc planning, state, review, and context files; optional loop commands can install Claude Code hook scripts and update .claude/settings.json.] <br>

## Skill Version(s): <br>
0.1.13 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
