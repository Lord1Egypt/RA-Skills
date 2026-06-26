## Description: <br>
Generates slide presentations through the AnyGen CLI and AnyGen service for decks, reports, proposals, trainings, launches, and similar presentation work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[logictortoise](https://clawhub.ai/user/logictortoise) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to turn presentation requests into slide-generation workflows, including business decks, training materials, reports, proposals, and launch presentations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation content is sent to the AnyGen service and the skill requires an AnyGen API key. <br>
Mitigation: Confirm the user trusts AnyGen and is comfortable sending the presentation content to that service before use. <br>
Risk: The workflow may install the anygen-workflow-generate skill if it is missing, creating a persistent change to the agent environment. <br>
Mitigation: Ask the user to approve that installation only after verifying the source and accepting the environment change. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/logictortoise/anygen-slide-generator) <br>
- [AnyGen](https://www.anygen.io) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated presentation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the anygen CLI and ANYGEN_API_KEY; presentation content may be sent to AnyGen's service.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
