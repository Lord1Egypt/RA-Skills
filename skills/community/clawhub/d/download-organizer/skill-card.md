## Description: <br>
Download Organizer helps organize files in a chosen local folder by categorizing common file extensions into documents, images, videos, audio, installers, archives, code, and other folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and general users can use this skill to plan or run local download-folder cleanup workflows, preview file categorization, and undo a prior organization pass when the local backup mapping is still available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running file organization against the wrong directory or output path can copy files into an unintended folder structure. <br>
Mitigation: Use preview mode first, run the tool against a narrow folder such as Downloads, and verify the output path before confirming. <br>
Risk: Undo depends on the local backup mapping and may not reverse later manual changes or missing backup data. <br>
Mitigation: Keep separate backups for important files and confirm the backup mapping remains available before relying on undo. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utopiabenben/download-organizer) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths, preview output, and undo guidance for the selected folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact changelog, released 2026-03-06) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
