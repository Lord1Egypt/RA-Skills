## Description: <br>
Disciplined diagnosis loop for hard bugs and performance regressions that guides agents through reproduction, minimisation, hypothesis testing, instrumentation, fixing, and regression testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genortg](https://clawhub.ai/user/genortg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to investigate hard bugs and performance regressions through a disciplined loop of reproduction, hypothesis testing, instrumentation, fixing, and regression testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debugging work may introduce temporary logs, throwaway harnesses, or local test code. <br>
Mitigation: Review resulting code changes and remove temporary instrumentation before merging. <br>
Risk: A diagnosis workflow can produce incorrect hypotheses if the failure is not reproduced first. <br>
Mitigation: Use the skill's feedback-loop and reproduction checks before applying fixes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/genortg/diagnose) <br>
- [GSD Core attribution](https://github.com/open-gsd/gsd-core) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code] <br>
**Output Format:** [Markdown guidance with checklists and inline command or code suggestions when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend tests, local commands, temporary logs, throwaway harnesses, and regression checks during debugging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
