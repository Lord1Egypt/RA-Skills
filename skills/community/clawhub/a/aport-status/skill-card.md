## Description: <br>
Show your current APort passport status, including capabilities, deliverable contract, pending tasks, and recent decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uchibeke](https://clawhub.ai/user/uchibeke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to check an agent's APort identity, allowed capabilities, deliverable requirements, pending tasks, and recent decision history before or during work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts APort and can expose agent identity, passport status, owner details, capabilities, and recent decision metadata. <br>
Mitigation: Install it only when APort identity/status checks are intended, treat full status output as potentially private, and avoid sharing it in public logs or transcripts. <br>
Risk: The artifact includes optional external setup commands and API calls. <br>
Mitigation: Review external commands and endpoints before running them in an agent environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/uchibeke/aport-status) <br>
- [APort passport web app](https://aport.id) <br>
- [APort agent skill](https://aport.id/skill) <br>
- [APort dashboard](https://aport.io/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown status summary with inline API endpoints and optional shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include agent identity, passport URL, capabilities, deliverable contract, and recent authorization decisions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
