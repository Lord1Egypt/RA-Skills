## Description: <br>
Delegates longer coding tasks to Sourcegraph Amp, an autonomous coding agent that can read, edit, refactor, and test code across a repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minerva-care](https://clawhub.ai/user/minerva-care) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to delegate multi-file code changes, feature implementation, bug fixes, refactors, and test writing to Amp from the correct project directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Amp is invoked with unsupervised authority to edit and run actions in the selected repository. <br>
Mitigation: Use trusted projects, preferably on a clean branch or disposable checkout, and review diffs and test results before merging or deploying. <br>
Risk: Running the wrong amp binary or using a repository that contains secrets can increase execution and data exposure risk. <br>
Mitigation: Verify which amp binary will run and avoid using the skill in repositories containing secrets. <br>


## Reference(s): <br>
- [Amp Code on ClawHub](https://clawhub.ai/minerva-care/amp-code) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text, Code, Files] <br>
**Output Format:** [Markdown guidance with bash command examples and Amp command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the amp binary; the wrapper prints the thread ID, selected mode, working directory, and Amp final response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
