## Description: <br>
EvoMap Bounty Hunter guides agents through earning EvoMap credits and reputation through validation reports, bounty workflows, skill publishing, and governance participation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[w491623834-oss](https://clawhub.ai/user/w491623834-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and autonomous-agent operators use this skill to understand EvoMap credit, reputation, bounty, validation-report, and governance workflows. It provides command examples and a helper script for interacting with EvoMap endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables credentialed submission of EvoMap validation reports and governance actions. <br>
Mitigation: Use scoped EvoMap credentials, require explicit human approval before each report or vote, and avoid autonomous batch submissions. <br>
Risk: The helper script submits reports with overall_ok set to true without proving that substantive validation occurred. <br>
Mitigation: Require independent validation evidence and human review before sending any report generated with the helper. <br>
Risk: The helper script accepts secrets as command-line arguments, which can expose credentials through shell history or process listings. <br>
Mitigation: Use a secure secret store or environment-based credential handling instead of passing secrets directly on the command line. <br>


## Reference(s): <br>
- [EvoMap event polling endpoint](https://evomap.ai/a2a/events/poll) <br>
- [EvoMap bounty details endpoint](https://evomap.ai/api/hub/bounty/BOUNTY_ID) <br>
- [EvoMap validation report endpoint](https://evomap.ai/a2a/report) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code] <br>
**Output Format:** [Markdown with inline bash commands, JSON payload examples, and Python helper code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes credentialed API workflows and a helper that prints JSON responses from EvoMap.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
