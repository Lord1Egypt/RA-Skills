## Description: <br>
Generate hyper-personalized cold email sequences using AI. Turn lead data into high-converting outreach campaigns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bluecraft-AI](https://clawhub.ai/user/Bluecraft-AI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales and growth teams use this skill to generate personalized cold-email sequences from lead data and campaign context. Agents can list campaigns, submit single-lead or batch generation requests, poll list status, and retrieve completed sequence exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lead and prospect data is submitted to MachFive for external AI processing. <br>
Mitigation: Install only if you trust MachFive with the submitted lead data, and upload only prospect data you are authorized to use for outreach and external processing. <br>
Risk: The skill requires a MachFive API key. <br>
Mitigation: Use a dedicated or scoped API key when available, keep it in the MACHFIVE_API_KEY environment variable, and rotate it if exposure is suspected. <br>
Risk: Batch generation can process the wrong leads or campaign if campaign and list inputs are not checked. <br>
Mitigation: Confirm the target campaign and lead list before batch generation, especially when the agent had to list campaigns for selection. <br>
Risk: Long-running generation requests may time out or return before results are complete. <br>
Mitigation: Use the documented polling and export flow for batch jobs, and recover timed-out single-lead requests through the returned list status and export endpoints when available. <br>


## Reference(s): <br>
- [MachFive Cold Email on ClawHub](https://clawhub.ai/Bluecraft-AI/cold-email) <br>
- [MachFive API Key Settings](https://app.machfive.io/settings) <br>
- [MachFive Campaigns](https://app.machfive.io/campaigns) <br>
- [MachFive Website](https://machfive.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON API responses and generated email sequence text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MACHFIVE_API_KEY; single-lead generation can take 5-10 minutes, and batch generation requires polling before export.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
