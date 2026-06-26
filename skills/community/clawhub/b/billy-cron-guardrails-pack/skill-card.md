## Description: <br>
Lint cron entries for schedule validity, bad model names, and missing NO_REPLY discipline markers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Highlander89](https://clawhub.ai/user/Highlander89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check cron files or stdin for malformed schedules, disallowed model names, and announce-like jobs that lack NO_REPLY markers before installing or reviewing scheduled tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The linter reads cron content from a file path or stdin selected by the user. <br>
Mitigation: Run it only on cron files or stdin content intended for inspection. <br>
Risk: Static lint checks can miss cron behavior outside the documented schedule, model-name, and NO_REPLY rules. <br>
Mitigation: Review lint results alongside normal cron validation and operational review before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Highlander89/billy-cron-guardrails-pack) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text lint results and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The linter exits 0 when no issues are found, 1 when lint issues are found, and 2 for usage or read errors.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
