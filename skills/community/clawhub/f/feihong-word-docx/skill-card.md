## Description: <br>
Create, inspect, and edit Microsoft Word documents and DOCX files with reliable styles, numbering, tracked changes, tables, sections, and compatibility checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunyue1977](https://clawhub.ai/user/sunyue1977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, document authors, and review teams use this skill when an agent needs to create, inspect, or edit Word and DOCX files while preserving styles, numbering, tracked changes, comments, tables, sections, fields, and round-trip compatibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential DOCX contents may be read or modified by the agent tools selected for a task. <br>
Mitigation: Use approved document tools, limit input files to the minimum necessary, and review tool permissions before working with sensitive documents. <br>
Risk: Complex Word documents can lose formatting fidelity through style, numbering, field, comment, or section changes. <br>
Mitigation: Use structure-preserving workflows and verify the final document in the target editors before delivery. <br>
Risk: Macro-bearing or legacy Word files can require additional caution beyond normal DOCX handling. <br>
Mitigation: Treat .docm files as macro-bearing and convert or inspect legacy .doc inputs before applying DOCX-specific assumptions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunyue1977/feihong-word-docx) <br>
- [Skill homepage](https://clawic.com/skills/word-docx) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Code, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with optional code or shell command snippets; agent workflows may produce or modify DOCX files when paired with appropriate document tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance-only skill; the provided artifact contains no executable code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
