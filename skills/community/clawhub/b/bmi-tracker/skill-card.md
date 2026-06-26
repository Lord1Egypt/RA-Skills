## Description: <br>
Bmi Tracker helps users calculate BMI, assess BMI ranges, receive improvement suggestions, and manage BMI history and target goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to calculate BMI, review BMI categories, receive general improvement suggestions, and track BMI history and target goals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: History and goal tracking may involve height, weight, BMI, and target values. <br>
Mitigation: Check where those values are stored, who can access them, and how to delete them before using tracking features. <br>
Risk: The artifact declares a curl requirement without explaining network use. <br>
Mitigation: Review any requested network commands before running them and avoid sending health-related values to unexpected endpoints. <br>
Risk: BMI assessments and improvement suggestions can be mistaken for individualized medical advice. <br>
Mitigation: Treat outputs as general wellness information and consult a qualified professional for medical decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may surface BMI category labels, history views, and target-goal guidance; check local storage behavior before using history or goal tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
