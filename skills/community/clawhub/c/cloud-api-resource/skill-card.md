## Description: <br>
Cloud API Resource helps an agent gather required UCloud parameters, confirm the requested configuration, sign UCloud API requests, and return creation results for resources such as UHost instances, API keys, storage buckets, databases, and VPCs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[892577738-bot](https://clawhub.ai/user/892577738-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to let an agent help configure and create UCloud resources through official API calls. It is intended for workflows where the user reviews the resource and billing details before the agent sends a provider request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create billable UCloud resources. <br>
Mitigation: Require explicit provider-side confirmation and review the full resource and billing summary before any API call. <br>
Risk: The skill requires sensitive UCloud credentials. <br>
Mitigation: Use least-privilege subaccount keys, avoid broad or long-lived private keys in chat, and ensure private keys are not logged or persisted. <br>
Risk: Broad creation requests may result in unintended resources or configurations. <br>
Mitigation: Review required parameters, defaults, region, resource type, and custom parameters before approving the request. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/892577738-bot/cloud-api-resource) <br>
- [UCloud API endpoint example: CreateUHostInstance](https://api.ucloud.cn/?Action=CreateUHostInstance) <br>
- [UCloud API endpoint example: CreateUMInferAPIKey](https://api.ucloud.cn/?Action=CreateUMInferAPIKey) <br>
- [UCloud API endpoint example: CreateBucket](https://api.ucloud.cn/?Action=CreateBucket) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, text] <br>
**Output Format:** [Structured object with success status, HTTP status code, raw response data, extracted resource ID, and error message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UCloud public and private keys, explicit user confirmation before API calls, and careful review of provider responses and billing impact.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
