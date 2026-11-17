## Description:

Agent Work Visibility helps OpenClaw agents show progress, health, blockers, and user-input needs during long-running tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rachelw0212](https://clawhub.ai/user/rachelw0212)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add visible progress tracking, blocker reporting, and user-intervention prompts to long-running OpenClaw tasks such as research, browser, API, and multi-step analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent activation changes workspace-wide agent behavior rules.

Mitigation: Review activate.js before use, back up SOUL.md and AGENTS.md, confirm OPENCLAW_WORKSPACE targets the intended workspace, and use deactivate.js to remove the injected protocol when no longer needed.

Risk: Local snapshot handling may be unsafe when task IDs or output paths come from untrusted inputs.

Mitigation: Use trusted task identifiers and output paths only, and avoid exposing SnapshotHistoryManager to untrusted callers until path containment is fixed.

Risk: Activation and snapshot files can leave persistent state in the workspace.

Mitigation: Plan cleanup for .visibility-state*.json files and artifacts/phase2 snapshots during uninstall or environment reset.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rachelw0212/skills/agent-work-visibility)
- [Publisher profile](https://clawhub.ai/user/rachelw0212)
- [README](README.md)
- [MVP design document](docs/agent_work_visibility_mvp.md)
- [Phase 2 integration design](docs/integration_phase2.md)
- [Phase 2 validation report](docs/validation_report_phase2.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Human-readable progress and status snapshots with CLI commands and markdown-style task updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent workspace protocol text and local visibility snapshot files after manual activation.]

## Skill Version(s):

3.0.5 (source: server release metadata, skill.json, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
