## Description: <br>
Forces M2.7 to produce an explicit structured plan before writing code, capturing sub-problems, APIs with version requirements, risks, files affected, and implementation order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephenlthorn](https://clawhub.ai/user/stephenlthorn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent orchestrators use this skill to decompose complex or multi-file coding tasks into a structured implementation plan before code generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send the user's task and retrieved context to an external AI service without clear user disclosure. <br>
Mitigation: Review and approve the configured LLM endpoint before installation, and avoid using secrets, customer data, proprietary code, or sensitive retrieved context unless the endpoint is approved for that data. <br>
Risk: A generated plan can provide incorrect API, file, risk, or implementation guidance that downstream coding steps may follow. <br>
Mitigation: Review the structured plan before execution and validate listed APIs, file changes, ordering, and risk assumptions against the target project. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance] <br>
**Output Format:** [Structured JSON plan] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes sub-problems, APIs, risks, files affected, implementation order, and estimated LOC; may add a warning when estimated LOC exceeds 500.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
