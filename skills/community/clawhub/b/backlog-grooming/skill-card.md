## Description: <br>
Workflow-driven skill that autonomously manages stale items in Google Tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill on a schedule or by user request to trigger backlog grooming for stale Google Tasks items and report the resulting task summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger unscoped automated changes to Google Tasks through an external grooming plugin. <br>
Mitigation: Before installation or scheduled use, confirm what the plugin does, which Google account and task lists it can access, and whether it can delete or complete tasks. <br>
Risk: Scheduled backlog grooming may apply changes without a human preview. <br>
Mitigation: Require a preview or explicit confirmation for scheduled runs when task changes could affect production workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zvirb/backlog-grooming) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/zvirb) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON] <br>
**Output Format:** [JSON summary returned by the backlog grooming plugin] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Retries tool errors up to three times before notifying the user.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
