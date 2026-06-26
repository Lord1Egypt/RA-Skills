## Description: <br>
将用户提供的简历文本或简历文件（PDF、DOCX、DOC、TXT、Markdown，以及常见表格导出）整理成结构化候选人资料，再将这些信息填写到招聘报名表、应聘登记表、招聘网站或 ATS 招聘系统中。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thinkpeace](https://clawhub.ai/user/thinkpeace) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job applicants and agents supporting applicants use this skill to extract structured candidate information from resumes, map it into job application forms or hiring systems, and pause for review before final submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive resume, contact, identity, and job application data that could be written incorrectly or submitted prematurely. <br>
Mitigation: Use it only for a specific application, verify all resume and identity fields before writing or submitting, and pause before any final irreversible submission unless the user explicitly approves. <br>
Risk: The security review flagged an unrelated instruction about creating or moving skills into an auto-discovery directory. <br>
Mitigation: Do not allow skill-directory creation, movement, or auto-discovery changes unless the user explicitly requested that separate action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thinkpeace/fill-job-application-info) <br>
- [Candidate profile schema](references/resume-profile-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, structured candidate data, and edited application files or browser-filled form values when supporting tools are available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce filled Word, Excel, CSV, PDF, or browser form outputs through referenced document and browser automation skills; final irreversible submission should wait for user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
