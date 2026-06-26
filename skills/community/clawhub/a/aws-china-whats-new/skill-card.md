## Description: <br>
Provides AWS China Region service launch announcements and availability details for Beijing and Ningxia from 2016 to present, including dates and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jowhee327](https://clawhub.ai/user/jowhee327) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud teams use this skill to query AWS China Region service launch announcements, compare Beijing and Ningxia availability signals, and summarize matching results with announcement dates and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Querying can execute the bundled Python refresh script, make network requests to www.amazonaws.cn, and update the local JSON data file. <br>
Mitigation: Review command execution, network access, and file updates before using the refresh workflow in restricted environments. <br>
Risk: Absence of an indexed announcement may be mistaken for definitive service unavailability. <br>
Mitigation: State that missing results do not guarantee unavailability and include AWS China announcement links when available. <br>


## Reference(s): <br>
- [AWS China What's New](https://www.amazonaws.cn/en/new/) <br>
- [AWS China What's New skill on ClawHub](https://clawhub.ai/jowhee327/aws-china-whats-new) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with JSON query results and announcement links when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries may refresh the local JSON index from public AWS China pages before producing results.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
