## Description: <br>
Use when running existing project validation commands and fixing failures after code changes, including lint, type-check, unit/integration test, build, CI, or local script failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run existing repository validation commands, triage failures, apply scoped fixes, rerun affected checks, and report remaining risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run or recommend project validation, test, build, or CI commands that execute repository scripts. <br>
Mitigation: Use it only in repositories where executing existing project scripts is acceptable, and review commands before running them in sensitive environments. <br>
Risk: Broad activation wording could make an agent select the skill for nearby quality tasks outside the intended validation-and-fix workflow. <br>
Mitigation: Keep use scoped to existing validation failures and tighten activation wording in deployments where over-selection is observed. <br>
Risk: Automated fixes for validation failures can reduce type safety, remove assertions, or touch unrelated modules if not constrained. <br>
Mitigation: Apply one root-cause fix at a time, preserve type safety and assertions, rerun affected checks, and summarize residual risk in the validation report. <br>


## Reference(s): <br>
- [Validation Repair Report Template](references/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and code/configuration changes when fixes are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a validation repair report at reports/validation-fix-YYYY-MM-DD-HHmmss.md after validation work.] <br>

## Skill Version(s): <br>
2.6.0 (source: server release evidence, README, metadata.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
