## Description: <br>
ClawLite Investigate guides agents through a disciplined root-cause debugging workflow that investigates symptoms, analyzes failure patterns, validates hypotheses, applies targeted fixes, and reports verifiable results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to debug bugs, abnormal behavior, and service errors by collecting evidence, forming testable root-cause hypotheses, validating fixes, and producing a structured debug report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can lead an agent to inspect code, run git and test commands, and make targeted code or test changes. <br>
Mitigation: Review proposed commands and diffs before execution, and require the workflow's root-cause hypothesis and validation evidence before accepting changes. <br>
Risk: Incorrect root-cause analysis can produce misleading fixes or incomplete remediation. <br>
Mitigation: Use the skill's hypothesis validation, regression-test requirement, full test run, and structured debug report to confirm the fix addresses the original failure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/x-rayluan/clawlite-investigate) <br>
- [Publisher profile](https://clawhub.ai/user/x-rayluan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with structured debug reports and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include root-cause hypotheses, validation evidence, file and line references for fixes, regression-test status, and completion state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
