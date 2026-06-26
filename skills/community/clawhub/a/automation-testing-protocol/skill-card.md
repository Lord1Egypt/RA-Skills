## Description: <br>
A comprehensive framework for testing and validating automation projects to ensure stability, security, and scalability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vetmomen](https://clawhub.ai/user/vetmomen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to plan, run, and evaluate testing for automation projects across unit, integration, end-to-end, idempotency, regression, and logging checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause agents to apply broad QA/testing guidance, run tests, create helper files, or enforce timezone behavior. <br>
Mitigation: Install it only where that behavior is intended, review actions before execution, and override fixed timezone guidance with the project's configured timezone for production-sensitive or multi-region projects. <br>


## Reference(s): <br>
- [Automation Testing Protocol on ClawHub](https://clawhub.ai/vetmomen/automation-testing-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and testing criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to run tests or create a run_tests.py helper when a project lacks tests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
