## Description: <br>
Guides agents in using the Dreamina CLI for image and video generation workflows, including account checks, task submission, and async result queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mr-j-j](https://clawhub.ai/user/mr-j-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Dreamina image and video generation through the local CLI while checking help output, account session state, credits, task submission, and follow-up status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dreamina generation commands may consume paid account credits. <br>
Mitigation: Warn the user before running credit-consuming commands and check account credit when budget matters. <br>
Risk: Async generation submissions can be misreported if only the shell exit code is checked. <br>
Mitigation: Treat submissions as successful only when a submit ID is returned with an expected generation status, then query results by submit ID. <br>


## Reference(s): <br>
- [Dreamina on ClawHub](https://clawhub.ai/mr-j-j/dreamina) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command records, submit IDs, generation statuses, and warnings before credit-consuming actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
