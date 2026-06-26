## Description: <br>
Helps an agent complete user-delegated data analysis tasks using files intentionally uploaded into the working directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realRoc](https://clawhub.ai/user/realRoc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to delegate data analysis tasks to an agent, including analysis that reads uploaded working-directory files by filename. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded datasets are visible to the agent session and may contain sensitive data. <br>
Mitigation: Upload only files intended for analysis and avoid sensitive data unless processing in the agent session is acceptable. <br>
Risk: Generated analysis, code, or shell commands may produce incorrect or misleading results for a dataset. <br>
Mitigation: Review generated outputs and commands before relying on them or running them against uploaded files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown responses with optional code blocks and file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses uploaded filenames directly when code operates on user-provided files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
