## Description: <br>
Diagnoses Douyin accounts from a name or account ID by using RedFox data to produce four-dimension scoring, account performance analysis, and optimization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, brands, MCN teams, self-media creators, and content operators use this skill to evaluate Douyin account health, compare account quality, and receive data-based optimization suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key. <br>
Mitigation: Store REDFOX_API_KEY in the runtime environment and avoid exposing it in prompts, code, logs, or generated reports. <br>
Risk: Douyin account names or IDs are sent to RedFox for lookup and report generation. <br>
Mitigation: Use the skill only for accounts that are appropriate to submit to RedFox and disclose this data flow to users when needed. <br>
Risk: When an account is not found, replying with an account ID can submit it to RedFox for asynchronous collection. <br>
Mitigation: Confirm the user intends to enroll the account before submitting an ID for collection. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/redfox-data/douyin-account-diagnosis-redfox) <br>
- [Core Workflow Reference](references/core_workflow.md) <br>
- [RedFox API Endpoint](https://redfox.hk/story/api/dyUser/query) <br>
- [RedFox Website](https://redfox.hk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown diagnostic report with scoring breakdowns, tables, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and sends Douyin account names or IDs to RedFox for lookup and report generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
