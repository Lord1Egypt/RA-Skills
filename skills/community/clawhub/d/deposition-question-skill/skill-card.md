## Description: <br>
Develop deposition question sets from Relativity-exported PDF productions using a user-provided legal theory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChipmunkRPA](https://clawhub.ai/user/ChipmunkRPA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal teams and litigation-support users use this skill to review Relativity-exported PDF productions against a legal theory and draft deposition questions grouped by document ID with supporting rationale and quotes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes selected legal PDFs that may contain confidential case material. <br>
Mitigation: Use specific PDF files or a narrow case-production folder and keep generated JSON in an appropriate secure case workspace. <br>
Risk: Extracted document IDs, quotes, and legal analysis may be incomplete or inaccurate. <br>
Mitigation: Verify document IDs, source page references, quotes, and legal conclusions before relying on the drafted questions. <br>


## Reference(s): <br>
- [Deposition Output Template](references/deposition_output_template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ChipmunkRPA/deposition-question-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown deposition-question sections with optional JSON page-extraction output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Groups questions by document ID and includes reason, supporting quote, source file, and page reference.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
