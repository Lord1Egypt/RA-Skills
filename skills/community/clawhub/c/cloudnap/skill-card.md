## Description: <br>
CloudNap lets agents manage AWS EC2 instances by listing, starting, stopping, and scheduling them through the CloudNap API with the user's API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bhushan21z](https://clawhub.ai/user/bhushan21z) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and control EC2 instances and automate start/stop schedules through CloudNap. It is intended for users who already have a CloudNap API key and managed AWS resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start or stop EC2 instances and remove schedules, which may interrupt services or remove automation. <br>
Mitigation: Use a least-privileged CloudNap API key, verify instance and schedule details, and require explicit confirmation before stopping resources or deleting schedules. <br>
Risk: Installing the skill gives an agent access to CloudNap actions through the configured API key. <br>
Mitigation: Install only when the publisher and CloudNap account are trusted, and keep the API key secret in the configured environment variable. <br>


## Reference(s): <br>
- [CloudNap Skill on ClawHub](https://clawhub.ai/bhushan21z/cloudnap) <br>
- [CloudNap API Base URL](https://cloudnap.in/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Guidance] <br>
**Output Format:** [Plain text responses with CloudNap API requests and response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CLOUDNAP_API_KEY for authenticated requests and should not expose the key.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
