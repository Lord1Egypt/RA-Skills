## Description: <br>
Docx Generation helps an agent create professional Microsoft Word-compatible documents from scratch using documented design rules, templates, structured content planning, formatting, and local .docx output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and office-document agents use this skill to plan and generate styled Microsoft Word-compatible .docx documents from user requirements, including reports, proposals, contracts, resumes, tables, images, page elements, and templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated local .docx files can overwrite existing documents or be saved somewhere unintended if the task is ambiguous. <br>
Mitigation: Provide a clear filename and save location, and avoid overwriting existing documents unless that is the intended action. <br>
Risk: Generated Word documents may contain content or formatting that should not be shared as-is. <br>
Mitigation: Open and review generated documents in Microsoft Word or compatible software before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/skills/docx-generation) <br>
- [docx-catalog.md](artifact/references/docx-catalog.md) <br>
- [docx-requirements.md](artifact/references/docx-requirements.md) <br>
- [exemplars.md](artifact/references/exemplars.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, files, guidance] <br>
**Output Format:** [Markdown guidance and generated .docx files; may include document-generation code, structured document content, and file-location notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill expects a clear document type, formatting requirements, filename, and save location; generated documents should be opened with Microsoft Word or compatible software for review.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
