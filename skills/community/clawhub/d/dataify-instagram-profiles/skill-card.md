## Description: <br>
Submit Dataify Instagram Profile Builder tasks for two Instagram profile collection modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit Dataify Builder jobs that collect Instagram profile data by username or profile URL and return task status details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create external Dataify jobs using a Dataify API TOKEN. <br>
Mitigation: Use a limited-scope token if available, avoid sharing real tokens in chats or terminals, and review task parameters before submission. <br>
Risk: Incorrect mode or parameter values can submit the wrong Instagram profile collection task. <br>
Mitigation: Confirm whether the user wants username or profile URL mode, validate required fields, and submit only parameters for the selected mode. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-instagram-profiles) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands and JSON task summaries from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Submits external Dataify Builder jobs and reports task_id, status, selected mode, parameters, file name, and dashboard URL.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
