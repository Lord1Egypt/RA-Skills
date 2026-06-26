## Description: <br>
Automates browser-assisted reporting of harassing phone calls through the 12321 complaint form, with user confirmation for captcha, phone, SMS verification, report details, validation, and submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnqxu](https://clawhub.ai/user/johnqxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to guide an agent through filing a 12321 harassment-call complaint while reviewing the captcha result, phone number, report fields, SMS verification step, and final submission decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates an official complaint submission and can trigger SMS verification. <br>
Mitigation: Require explicit user approval before requesting SMS verification, accepting consent checkboxes, or submitting the final report. <br>
Risk: The workflow handles phone numbers, captcha data, SMS codes, and report details. <br>
Mitigation: Show all captured and defaulted fields to the user for confirmation and allow edits before any site interaction that sends or submits data. <br>
Risk: The artifact contains hard-coded phone behavior and default complaint fields. <br>
Mitigation: Replace defaults with user-confirmed values for each run and verify the reporting phone number and target phone number every time. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnqxu/12321-harass-report) <br>
- [12321 report site](https://www.12321.cn) <br>
- [12321 field mapping reference](references/field-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown instructions with JavaScript snippets, shell commands, and user confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides browser actions, captcha handling, SMS verification, complaint form filling, validation checks, and final submission.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
