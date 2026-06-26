## Description: <br>
Adversarial Verification helps agents challenge code and system changes with real command execution, targeted checks, and explicit PASS or FAIL reporting. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[minijoy-b](https://clawhub.ai/user/minijoy-b) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to verify frontend, backend, CLI, configuration, package, and bug-fix changes by running concrete checks and reporting an explicit PASS or FAIL result. It is most useful before commits, deployments, major changes, or third-party code review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute shell, npm, build, and target JavaScript commands against a selected project path. <br>
Mitigation: Use it only on trusted repositories or inside a disposable sandbox, and review the target path and commands before execution. <br>
Risk: Automation guidance includes Git hook, CI, and deployment check integrations that could run verification commands automatically. <br>
Mitigation: Avoid wiring the skill into hooks, CI, or deployment workflows until the command behavior and project impact are accepted. <br>
Risk: The artifact recommends destructive or adversarial testing as part of validation. <br>
Mitigation: Run destructive checks in isolated test environments with backups and avoid direct production execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minijoy-b/adversarial-verification) <br>
- [Publisher profile](https://clawhub.ai/user/minijoy-b) <br>
- [Quick start guide](examples/quick-start.md) <br>
- [Package metadata](package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or terminal text with command lists, execution results, and PASS or FAIL verdicts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include stdout, stderr, exit status summaries, reproduction steps, and suggested fixes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
