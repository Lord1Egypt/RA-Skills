## Description: <br>
Deepaistudy Errors is a CLI skill for uploading photographed incorrect exercises to DeepAIStudy for AI analysis, review tracking, and variation-question generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stoneyshum](https://clawhub.ai/user/stoneyshum) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, tutors, and study-support agents use this skill to add worksheet photos to a DeepAIStudy error book, review analyzed mistakes, mark mastery, and generate practice variants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Worksheet photos and extracted study content are uploaded to the configured DeepAIStudy server. <br>
Mitigation: Use only an approved server and avoid uploading pages with names, school identifiers, grades, or other personal data. <br>
Risk: Reusable DeepAIStudy credentials are stored locally in plaintext configuration. <br>
Mitigation: Use dedicated credentials where possible, restrict access to the local config file, and remove stored credentials when the skill is no longer needed. <br>
Risk: Preview and count flags are advertised but may not prevent upload or saving. <br>
Mitigation: Do not rely on those flags as a privacy or persistence control; verify the command and input images before running upload actions. <br>
Risk: Delete operations may remove remote error-book records immediately. <br>
Mitigation: Confirm the target record ID and retain any required backup or export before deleting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stoneyshum/deepaistudy-errors) <br>
- [DeepAIStudy service](https://www.deepaistudy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload worksheet images to the configured DeepAIStudy server and modify or delete remote error-book records.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and setup.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
