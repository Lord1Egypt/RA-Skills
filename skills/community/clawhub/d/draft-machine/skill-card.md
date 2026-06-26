## Description: <br>
Draft Machine helps agents create Gmail drafts for personalized batch emails from a CSV recipient list and a Markdown/Jinja2 template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[audiojak](https://clawhub.ai/user/audiojak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to prepare Gmail mail-merge drafts for review before sending. It guides installation, Gmail OAuth setup, CSV and template preparation, previewing, draft creation, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing and using the DraftMachine CLI depends on trusting the PyPI package and linked source. <br>
Mitigation: Review the package and source before installation, and install only in an environment where that dependency is acceptable. <br>
Risk: Gmail OAuth setup handles sensitive local credential files and grants draft-related account access. <br>
Mitigation: Confirm the OAuth consent scope is limited to the expected draft access and keep ~/.draftmachine credential files private. <br>
Risk: Personalized email templates or CSV data can render incorrect or unintended draft content. <br>
Mitigation: Run the required preview, fix template or data issues before draft creation, and review all Gmail drafts before sending. <br>


## Reference(s): <br>
- [Draft Machine ClawHub Release](https://clawhub.ai/audiojak/draft-machine) <br>
- [DraftMachine on PyPI](https://pypi.org/project/draftmachine/) <br>
- [DraftMachine Source](https://github.com/johnkennedy/DraftMachine) <br>
- [Jinja2 Documentation](https://jinja.palletsprojects.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, CSV examples, and Markdown/Jinja2 template examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides a preview-first workflow; DraftMachine creates Gmail drafts for user review and does not send messages automatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
