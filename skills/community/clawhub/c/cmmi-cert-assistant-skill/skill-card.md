## Description: <br>
CMMI V3.0 Certification Assistant helps project managers and EPG teams match project documents to CMMI V3.0 Practice Areas, analyze evidence gaps, and draft compliant certification documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kooui](https://clawhub.ai/user/kooui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Project managers and EPG teams use this skill to prepare for CMMI V3.0 appraisals by mapping uploaded project documents to Practice Areas, identifying missing evidence, and producing draft compliant document structures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded project documents may contain sensitive organizational evidence. <br>
Mitigation: Use the skill only where document analysis is acceptable, and review uploaded content handling before use. <br>
Risk: Generated CMMI documents and gap analyses may be incomplete or inaccurate for an appraisal. <br>
Mitigation: Treat outputs as drafts and have qualified CMMI reviewers validate evidence and recommendations manually. <br>
Risk: Generated DOCX outputs could overwrite existing files if an unsafe path is chosen. <br>
Mitigation: Choose output paths carefully and review generated filenames before running document-generation commands. <br>


## Reference(s): <br>
- [CMMI Certification Assistant README](README.md) <br>
- [CMMI Certification Assistant Skill Instructions](SKILL.md) <br>
- [Practice Area Knowledge References](references/PA_knowledge/) <br>
- [Practice Area Document Configuration](scripts/pa_config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured analysis, optional shell commands, and draft document-generation outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce CMMI Practice Area matches, gap-analysis reports, compliant document outlines, and DOCX generation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
