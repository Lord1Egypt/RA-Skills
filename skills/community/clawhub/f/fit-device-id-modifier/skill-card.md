## Description:

Modify FIT ride files so their device identifiers report Garmin manufacturer 1 and Garmin Edge 500 China product ID 1030 for Garmin Connect recognition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckboss](https://clawhub.ai/user/ckboss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cycling data users use this skill to run a local Python workflow that creates modified copies of FIT files for Garmin Connect compatibility while preserving the original files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated FIT files can be corrupted by simple binary editing or invalid field replacement.

Mitigation: Run the script on copies, keep backups of original FIT files, and validate generated files before relying on or uploading them.

Risk: Existing _GM.fit outputs may be overwritten when the same input path is processed again.

Mitigation: Avoid running the script in directories where existing _GM.fit files must be preserved, or move generated files before reprocessing.

Risk: The script depends on the local Python environment and the fitparse package.

Mitigation: Use a virtual environment and pin or review fitparse before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, code, files]

**Output Format:** [Markdown guidance with shell commands and Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces modified FIT files with a _GM.fit suffix and leaves source FIT files unchanged.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
