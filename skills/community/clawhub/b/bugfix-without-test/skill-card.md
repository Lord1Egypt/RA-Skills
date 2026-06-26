## Description: <br>
A fix is applied without a reproduction test, leaving no proof the bug is fixed and no regression coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvogt99](https://clawhub.ai/user/mvogt99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to identify bug fixes that lack regression tests and to add or document verification before accepting the fix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: When followed by a coding agent with repository write access, the skill may lead to added or modified tests and code while fixing bugs. <br>
Mitigation: Review the resulting code changes and run the normal test suite and CI before merging. <br>
Risk: Manual verification may be substituted when a bug is hard to test, which can leave weaker regression coverage. <br>
Mitigation: Require an explicit explanation of why automated coverage is not practical and record the manual verification performed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mvogt99/bugfix-without-test) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mvogt99) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown] <br>
**Output Format:** [Markdown guidance and checklist-style recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance-only skill with no hidden access or execution behavior reported by security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
