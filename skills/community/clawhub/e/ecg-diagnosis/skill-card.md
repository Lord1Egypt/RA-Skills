## Description:

Automates ECG image submission to a third-party web service, fills age and sex metadata from filenames, extracts diagnosis text, and saves results to an Excel workbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanglucheng](https://clawhub.ai/user/fanglucheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users processing ECG image batches can use this skill to enforce filename metadata checks, run the provided browser automation workflow, and collect returned diagnosis summaries in an Excel file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles sensitive ECG images and may expose patient-identifying metadata from filenames.

Mitigation: Avoid real patient data unless consent, data retention, and disclosure requirements for the third-party service are satisfied.

Risk: The automation uploads ECG images, age, and sex to a hard-coded third-party website.

Mitigation: Review the third-party domain, privacy terms, and retention practices before installing or running the skill.

Risk: The browser workflow uses a persistent local browser profile in the selected folder.

Mitigation: Use a disposable working directory or clear the generated browser profile after each run, especially for sensitive cases.

Risk: The skill depends on user-supplied folder and image names for local execution.

Mitigation: Validate paths and filenames before execution and invoke shell commands with argument-safe handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanglucheng/skills/ecg-diagnosis)
- [Third-party ECG web service](https://www.xin-gou.com/chat/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Text guidance, a local Python command, console progress messages, and an Excel .xlsx result file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local ECG image files with metadata encoded in filenames and writes diagnosis results to the selected folder.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
