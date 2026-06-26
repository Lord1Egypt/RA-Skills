## Description: <br>
Creates Microsoft Word (.docx) documents with an AI-generated disclaimer footer, including support for headings, paragraphs, lists, tables, code blocks, images, and hyperlinks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[983488728](https://clawhub.ai/user/983488728) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to programmatically generate formatted Word documents, reports, and exported content with an automatic AI disclaimer footer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is Chinese-first, which may not fit workflows that require English or multilingual documentation. <br>
Mitigation: Confirm language requirements before use and provide language-specific generation instructions when needed. <br>
Risk: The skill writes .docx files to the requested output path and can create missing directories. <br>
Mitigation: Review the requested output path and write only to intended workspace locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/983488728/docx-generator) <br>
- [Publisher profile](https://clawhub.ai/user/983488728) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [DOCX generator script](artifact/scripts/docx_generator.py) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Microsoft Word .docx files and Python usage snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated documents include an AI-generated disclaimer footer by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
