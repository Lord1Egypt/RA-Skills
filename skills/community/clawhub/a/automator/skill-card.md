## Description: <br>
Automate macOS tasks by composing and executing Automator workflows through automator CLI and AppleScript control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and macOS power users use this skill to run, inspect, compose, and troubleshoot Automator .workflow automations through local Automator CLI and AppleScript interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automator workflows can modify files, application state, or large batches of items when run against the wrong target or with unbounded input. <br>
Mitigation: Require absolute workflow paths, state expected side effects and bounded inputs, confirm rollback plans for write operations, and use two-step confirmation before destructive runs. <br>
Risk: macOS automation or privacy permission prompts can block execution or change the expected run flow. <br>
Mitigation: Treat permission prompts as part of the run state, ask the user to grant the needed permission, and retry first with a small read-only probe before running the intended workflow. <br>
Risk: Local memory can retain workflow paths, action names, and diagnostics that may expose user workflow details. <br>
Mitigation: Store only reusable non-secret context in ~/automator/ and avoid saving secrets or unrelated command output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/automator) <br>
- [Skill homepage](https://clawic.com/skills/automator) <br>
- [Interface Matrix - Automator](interface-matrix.md) <br>
- [Execution Guardrails](execution-guardrails.md) <br>
- [Workflow Authoring With AppleScript](workflow-authoring.md) <br>
- [Troubleshooting - Automator](troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and AppleScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths, workflow variables, preflight checks, confirmation prompts, and run notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
