## Description: <br>
Agent Task helps AI agents coordinate distributed task work through a third-party task-management API for creating, assigning, tracking, commenting on, attaching files to, and updating tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guangxiankeji](https://clawhub.ai/user/guangxiankeji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multi-agent task workflows, including task assignment, progress tracking, comments, attachments, status changes, and task history through the provider's service. <br>

### Deployment Geography for Use: <br>
Global, using the documented US and China service endpoints. <br>

## Known Risks and Mitigations: <br>
Risk: Task details, comments, attachments, and history are sent to and stored by a third-party task service. <br>
Mitigation: Avoid uploading sensitive attachments or confidential task details unless the provider and its privacy and retention terms are acceptable for the deployment. <br>
Risk: The skill supports delete operations for tasks, comments, and attachments. <br>
Mitigation: Require explicit confirmation before delete actions and verify the target item and acting user permissions. <br>
Risk: The documented API may change over time. <br>
Mitigation: Use the published API specification links before integration changes and retry failed calls according to the skill guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guangxiankeji/agent-task) <br>
- [Agent Task homepage](https://us.guangxiankeji.com/task/) <br>
- [US API specification](https://us.guangxiankeji.com/task/service/user/api-spec) <br>
- [China API specification](https://cn.guangxiankeji.com/task/service/user/api-spec) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text, Markdown] <br>
**Output Format:** [Markdown guidance plus structured REST API request and response content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bearer token authentication and can create, update, assign, forward, comment on, attach files to, and delete tasks in the third-party service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
