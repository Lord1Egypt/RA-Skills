## Description: <br>
Agent Work Visibility adds a progress and health-status visibility layer for long-running agent tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rachelw0212](https://clawhub.ai/user/rachelw0212) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to make long-running work visible by showing task phase, progress percentage, health status, blocker state, and user-intervention requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The activation script persistently edits SOUL.md or AGENTS.md and changes agent behavior in later sessions. <br>
Mitigation: Review activate.js before running it, keep a backup of affected files, and use deactivate.js or remove the marked protocol block to roll back the change. <br>
Risk: Snapshot history APIs can write task snapshots and reports to paths supplied by the caller. <br>
Mitigation: Use trusted task IDs and output paths only, and do not expose snapshot-writing functions to untrusted input. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rachelw0212/agent-work-visibility) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Agent Work Visibility MVP design](docs/agent_work_visibility_mvp.md) <br>
- [Phase 2 integration design](docs/integration_phase2.md) <br>
- [Phase 2 validation report](docs/validation_report_phase2.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown-style progress text and JSON task snapshots] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes progress bars, phase names, health indicators, blocker messages, elapsed time, and optional user input prompts.] <br>

## Skill Version(s): <br>
3.0.5 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
