## Description: <br>
Generate personalized cloud career development roadmaps for AWS, Azure, and GCP support roles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, training teams, career coaches, and cloud support professionals use this skill to generate tailored learning roadmaps, certification paths, skill-gap summaries, and next steps for AWS, Azure, and GCP support roles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Career assessment details are sent to the provider's external API and may include sensitive employer, role, or skills information. <br>
Mitigation: Use anonymous or null user IDs when possible, avoid cloud credentials, employer-confidential information, and account details, and review the provider's privacy practices before sending sensitive data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/cloud-support) <br>
- [OpenAPI Specification](artifact/openapi.json) <br>
- [Provider API Docs](https://api.mkkpro.com:8060/docs) <br>
- [Provider API Route](https://api.mkkpro.com/career/cloud-support) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON roadmap response with roadmap phases, topics, exercises, recommended resources, skill gaps, and next steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JSON request containing session metadata and assessment data; returns validation errors for malformed requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
