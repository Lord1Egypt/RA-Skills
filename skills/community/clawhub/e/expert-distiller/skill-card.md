## Description: <br>
Use when conducting an in-depth adaptive interview with a domain expert to extract structured Q&A pairs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billb13](https://clawhub.ai/user/billb13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and knowledge-management teams use this skill to run adaptive expert interviews that capture expert knowledge, decision frameworks, and cognitive boundaries as structured Q&A pairs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Interview answers and analysis are written to local state, backup, and JSONL export files. <br>
Mitigation: Do not enter confidential or regulated information unless authorized, and protect or delete generated state, backup, and export files according to the user's data-handling requirements. <br>
Risk: The skill workflow references interview_engine.py and prompt templates that are not included in the submitted artifact. <br>
Mitigation: Verify that the referenced Python engine and prompt files are present and trusted before relying on the workflow. <br>


## Reference(s): <br>
- [Server-resolved source repository](https://github.com/BillB13/expert-distiller) <br>
- [ClawHub skill page](https://clawhub.ai/billb13/expert-distiller) <br>
- [Publisher profile](https://clawhub.ai/user/billb13) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSONL interview export output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow saves interview state and exports one JSON object per line with question, answer, phase, type, dimension, and timestamp fields.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
