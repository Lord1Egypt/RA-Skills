## Description:

Enforces a disciplined 4-phase pipeline for non-trivial coding tasks: Plan, Code, Validate, and Debug with explicit hypotheses, focused changes, root-cause checks, and bounded retry attempts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brasco05](https://clawhub.ai/user/brasco05)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to structure non-trivial bug fixes, feature work, refactors, test failures, and error investigations into a phase-gated workflow. It helps agents plan before editing, make one focused change at a time, validate root cause, and escalate after three documented debug attempts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad always-on hooks can influence routine coding sessions even when the pipeline is not appropriate.

Mitigation: Enable reminders at the project level, narrow hook matchers where possible, and skip the pipeline for trivial edits as documented by the skill.

Risk: Persistent learning files or workspace memory updates can affect future agent behavior beyond the current task.

Mitigation: Review .learnings entries and workspace memory or rule updates before allowing them to persist.

Risk: The phase tracker writes local workflow state under .pipeline-state in the current workspace.

Mitigation: Run the helper only in the intended project and inspect or reset .pipeline-state when task state should not carry forward.

## Reference(s):

- [Skill Definition](SKILL.md)
- [README](README.md)
- [Phase 1 Planner](references/phase-1-planner.md)
- [Phase 2 Coder](references/phase-2-coder.md)
- [Phase 3 Validator](references/phase-3-validator.md)
- [Phase 4 Debugger](references/phase-4-debugger.md)
- [Anti-Patterns](references/anti-patterns.md)
- [Worked Examples](references/examples.md)
- [Hook Setup](references/hooks-setup.md)
- [Integration with Other Skills](references/integration.md)
- [Multi-Agent Support](references/multi-agent.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [ClawHub Skill Page](https://clawhub.ai/brasco05/skills/coding-pipeline)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional checklist templates, hook reminders, and local phase-state tracking guidance.]

## Skill Version(s):

1.0.1 (source: evidence.release.version, artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
