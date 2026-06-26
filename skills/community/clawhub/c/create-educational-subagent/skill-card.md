## Description: <br>
Guides users through creating an educational subagent that records class activity, tracks teaching progress, answers progress questions, and maintains course-outline status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2070super](https://clawhub.ai/user/2070super) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators and education-operations users use this skill to create an OpenClaw subagent for recording class sessions, tracking each class's course progress, and answering later progress queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to approve broad OpenClaw administrative, pairing, approval, write, and secrets-related permissions that are not justified by classroom progress tracking. <br>
Mitigation: Review the exact OpenClaw request ID, requester, device, and scopes before approval; avoid granting admin, approval, pairing, or secrets permissions unless an authorized administrator has confirmed they are necessary. <br>
Risk: The included approval script can approve the latest pending OpenClaw device request without showing whether it belongs to this workflow. <br>
Mitigation: Inspect pending requests before running any approval command, and prefer approving a specific reviewed request rather than using a latest-request shortcut. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2070super/create-educational-subagent) <br>
- [Publisher profile](https://clawhub.ai/user/2070super) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and companion shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw command examples for approving a device request and spawning an ACP runtime subagent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
