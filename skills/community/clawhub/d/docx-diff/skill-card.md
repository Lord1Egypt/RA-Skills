## Description:

Compares two local Word .docx files to identify text, image, and style changes, then generates highlighted Word, HTML, and plain-text diff reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mypicko](https://clawhub.ai/user/mypicko)

### License/Terms of Use:

MIT-0

## Use Case:

Document reviewers, project teams, and developers use this skill to compare two versions of a Word document locally and produce reviewable diff artifacts without relying on an online comparison service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may contain document text and embedded images from the compared DOCX files.

Mitigation: Run the skill only on intended documents, store outputs in an appropriate project folder, and review reports before sharing them.

Risk: The workflow installs and uses python-docx in the local Python environment.

Mitigation: Use a project folder or virtual environment, and consider pinning python-docx before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mypicko/skills/docx-diff)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance plus generated DOCX, HTML, and plain-text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script reads the two user-selected DOCX files and writes diff outputs to the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
