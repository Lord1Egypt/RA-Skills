## Description: <br>
Helps agents fill Word .docx templates by replacing placeholders, populating marked tables, inserting images, and generating documents without modifying the original template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huagc](https://clawhub.ai/user/huagc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document automation users use this skill to guide agents in filling Word templates for reports, contracts, forms, and batch document generation while preserving template structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated output paths could overwrite user files or original templates. <br>
Mitigation: Review output paths before saving and keep original templates unchanged. <br>
Risk: Document contents supplied for template filling may contain sensitive information. <br>
Mitigation: Provide only content appropriate for local processing and review generated documents before sharing. <br>


## Reference(s): <br>
- [README.md](artifact/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/huagc/fill-docx-template) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code] <br>
**Output Format:** [Markdown guidance with Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local generation of .docx files when the agent applies the documented Python workflow.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
