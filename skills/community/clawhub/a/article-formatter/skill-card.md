## Description:

根据调研报告或公文规范模板，将原始文本自动排版成标准 .docx 格式，支持格式自动识别和参考文件规范应用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshineorangejuice](https://clawhub.ai/user/sunshineorangejuice)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, staff, and agents preparing Chinese research reports, official documents, or general articles use this skill to convert draft text into a standardized Word document with official-document-style layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default output path can create a .docx file under ~/Desktop/openclaw专属文件夹, which may be inappropriate for sensitive drafts or shared machines.

Mitigation: Use the -o option to write sensitive documents to an intended private or managed location.

Risk: The produced document uses Chinese official-document font choices that may fall back on systems without those fonts.

Mitigation: Review the generated .docx in the target office suite and install the expected fonts when exact visual fidelity is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshineorangejuice/skills/article-formatter)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [.docx Word document with console status text and optional command-line arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local Word document; by default the artifact behavior writes under ~/Desktop/openclaw专属文件夹 unless an output path is provided.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
