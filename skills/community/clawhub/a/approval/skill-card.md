## Description: <br>
企业办公流程与工时管理 Agent，支持办公流程导航、流程申请与审批、待办事项统计、请假调休申请等。当用户需要查询审批、提交申请、查看待办时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sangjie123](https://clawhub.ai/user/sangjie123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees use this agent to navigate enterprise office workflows, check pending approvals, submit or approve workflow requests, and manage leave or compensatory time requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated workflow and HR-related requests may view, submit, approve, or change sensitive workplace records. <br>
Mitigation: Use least-privilege Beyond-Token credentials and avoid placing real tokens in shared prompts, transcripts, or logs. <br>
Risk: Approval, workflow submission, or leave-related changes may be sent without enough user scoping or confirmation. <br>
Mitigation: Require explicit user confirmation before sending any approval, workflow submission, or leave-related change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sangjie123/approval) <br>
- [Publisher profile](https://clawhub.ai/user/sangjie123) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Guidance] <br>
**Output Format:** [Natural language responses with JSON-RPC workflow requests when the authenticated service is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Beyond-Token header for authenticated requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
