## Description: <br>
Standard Operating Procedure (SOP) that routes unstructured text to Tasks or LanceDB based on urgency using atomic nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this SOP to route captured notes or transcripts into either a task workflow or a vector-memory workflow based on whether the text is actionable or informational. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Captured notes or transcripts can be stored in Google Tasks or a vector database without clear user confirmation or privacy limits. <br>
Mitigation: Require explicit confirmation before routing, restrict accepted sources, redact sensitive details, and define deletion and retention rules. <br>
Risk: Sensitive meeting, customer, credential, medical, legal, financial, or private workspace content could be routed into persistent storage. <br>
Mitigation: Avoid those content classes unless the deployment adds source limits, redaction, retention controls, and user-visible review before storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/capture-classification) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zvirb) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, text] <br>
**Output Format:** [JSON log] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Confirms the routed destination and action taken by the selected atomic node.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
