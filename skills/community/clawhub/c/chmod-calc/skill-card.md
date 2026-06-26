## Description: <br>
Calculate chmod permissions by converting between numeric and symbolic notation and generating the corresponding chmod command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ohernandez-dev-blossom](https://clawhub.ai/user/ohernandez-dev-blossom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and technical users use this skill to understand Unix file permissions, convert between octal and symbolic forms, and draft chmod commands for files or directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chmod commands can grant overly broad access, especially permissions such as 777. <br>
Mitigation: Review generated commands before running them and prefer the least permissive permission set that satisfies the intended access need. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with chmod command examples and plain-English explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes numeric and symbolic permission notation, generated chmod commands, validation feedback, and warnings for insecure permissions when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
