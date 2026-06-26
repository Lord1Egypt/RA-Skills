## Description: <br>
Invokes the Coze Workflow stream_run API from OpenClaw with a workflow ID, JSON parameters, and a PAT token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chocolatemale](https://clawhub.ai/user/chocolatemale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to call Coze workflows from OpenClaw, pass workflow IDs and JSON parameters, and inspect streamed workflow responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a Coze PAT, workflow ID, and workflow input parameters to Coze. <br>
Mitigation: Use a dedicated limited-scope Coze token where possible and avoid placing secrets or regulated data in workflow parameters. <br>
Risk: Saved workflow responses may contain sensitive data if written to a shared temporary path. <br>
Mitigation: Write results to a private location with appropriate permissions when responses may be sensitive. <br>


## Reference(s): <br>
- [Coze Workflow stream_run API endpoint](https://api.coze.com/v1/workflow/stream_run) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with bash code blocks and streamed API response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save streamed workflow results to a user-selected file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
