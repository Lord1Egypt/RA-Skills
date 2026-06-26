## Description: <br>
Connect to Hannah and Elena agents from Serviceplan - specialized AI coworkers for marketing research and operations planning. Access via email or OpenAI-compatible API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sarthib7](https://clawhub.ai/user/Sarthib7) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to connect an OpenClaw-compatible agent to Serviceplan's Hannah and Elena AI coworkers for marketing research, operations planning, task tracking, and result retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task prompts, campaign details, and optional attachments may be sent to Serviceplan/sumike.ai services. <br>
Mitigation: Use only with organizational approval for third-party processing, and avoid sending secrets, regulated data, customer data, or confidential documents unless approved. <br>
Risk: Hannah and Elena API keys can be exposed if stored in source control, logs, or shared configuration. <br>
Mitigation: Store API keys through a secure secret mechanism where possible, keep them out of source control and logs, and rotate or revoke them according to organizational policy. <br>
Risk: The reviewed bundle does not include the referenced dist runtime files. <br>
Mitigation: Verify the installed package source and runtime artifacts before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Sarthib7/coworker) <br>
- [Hannah & Elena Homepage](https://sumike.ai) <br>
- [Hannah API Endpoint](https://hannah.sumike.ai/v1) <br>
- [Elena API Endpoint](https://elena.sumike.ai/v1) <br>
- [API Guide](API_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, API request examples, task status text, and result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce external API or email requests to Hannah and Elena when configured with required API keys or email access.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
