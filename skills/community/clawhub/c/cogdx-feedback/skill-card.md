## Description: <br>
CogDx Feedback helps agents submit pre/post-change evaluation data to Cerebratech's CogDx API to verify whether retraining or prompt changes improved performance and to earn credits toward diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drkavner](https://clawhub.ai/user/drkavner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill after retraining, prompt changes, or instruction updates to submit reviewed outcome data and check whether an observed improvement transferred. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feedback submissions are sent to a third-party Cerebratech service and may contribute to a shared calibration commons. <br>
Mitigation: Review payloads before submission, remove secrets, personal data, customer data, proprietary prompts, internal system instructions, and confidential notes, and use a non-identifying agent_id where possible. <br>


## Reference(s): <br>
- [CogDx Feedback API Reference](references/api.md) <br>
- [Cerebratech Feedback API](https://api.cerebratech.ai/feedback) <br>
- [Cerebratech API Catalog](https://api.cerebratech.ai/catalog) <br>
- [ClawHub Skill Page](https://clawhub.ai/drkavner/cogdx-feedback) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown with HTTP request examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No local file output; API responses include verification, score, credits, and next-step fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
