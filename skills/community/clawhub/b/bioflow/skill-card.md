## Description: <br>
Quick guide for BioFlow backend API usage and integration, covering signup/login, file upload/download, token balance queries, task submission, and result retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashipiling](https://clawhub.ai/user/ashipiling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integration agents use this skill to explain or execute the BioFlow API path from account setup through dataset handling, token balance checks, PTMPred task submission, polling, and result download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API examples may send credentials, datasets, or task submissions to a BioFlow service and could consume account credits. <br>
Mitigation: Verify the API host, use only intended credentials and datasets, and confirm task submissions before execution. <br>
Risk: Endpoint examples may drift from the currently deployed BioFlow backend. <br>
Mitigation: Confirm the auth flow, endpoint paths, and required parameters against the active BioFlow service before automating calls. <br>


## Reference(s): <br>
- [BioFlow Project Snapshot](references/current-auth-map.md) <br>
- [BioFlow API Call Flow](references/api-call-flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, API request examples, configuration] <br>
**Output Format:** [Markdown with concise endpoint notes and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Bearer-token API examples, required parameters, and key response fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
