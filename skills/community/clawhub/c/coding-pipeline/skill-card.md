## Description: <br>
Enforces a disciplined four-phase pipeline for non-trivial coding tasks: plan with a hypothesis, make one focused change, validate the root cause, and use bounded debugging before escalation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brasco05](https://clawhub.ai/user/brasco05) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to structure feature work, bug fixes, refactors, test failures, and deployment investigations into a phase-gated process with explicit planning, focused changes, validation evidence, and bounded debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local debugging notes and phase logs may capture sensitive details if secrets are included in errors or prompts. <br>
Mitigation: Keep secrets out of logs and periodically review `.learnings/ERRORS.md` and `.pipeline-state/`. <br>
Risk: Optional prompt-time hooks may add reminders to agent workflows when enabled. <br>
Mitigation: Enable optional hooks only in workspaces where prompt-time reminders are desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brasco05/coding-pipeline) <br>
- [Phase 1 Planner](references/phase-1-planner.md) <br>
- [Phase 2 Coder](references/phase-2-coder.md) <br>
- [Phase 3 Validator](references/phase-3-validator.md) <br>
- [Phase 4 Debugger](references/phase-4-debugger.md) <br>
- [Integration with Other Skills](references/integration.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup](references/hooks-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional shell commands and local state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local phase-tracking and failed-attempt logs when optional helper scripts or related workflow guidance are used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
