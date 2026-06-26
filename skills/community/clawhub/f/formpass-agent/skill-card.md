## Description: <br>
Register as a verified AI agent on the FormPass network. Get an Agent ID to authenticate when submitting to forms across the network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jezjsa](https://clawhub.ai/user/jezjsa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to register an AI agent with FormPass, obtain an Agent ID, and configure bearer-token authentication for verified form submissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent IDs can authorize verified FormPass submissions if exposed. <br>
Mitigation: Treat the Agent ID as a secret, store it securely, and avoid sharing it in transcripts or public logs. <br>
Risk: Form submissions may send personal or sensitive data to FormPass endpoints. <br>
Mitigation: Confirm the user approves the destination, form ID, and submitted data before running the curl examples. <br>
Risk: Using the wrong FormPass form ID or endpoint can submit data to an unintended destination. <br>
Mitigation: Verify the form ID and destination URL before submitting. <br>


## Reference(s): <br>
- [FormPass homepage](https://form-pass.com) <br>
- [FormPass agent registration](https://form-pass.com/dashboard/agents/new) <br>
- [FormPass agent integration docs](https://form-pass.com/docs/agent-integration) <br>
- [FormPass discovery docs](https://form-pass.com/docs/discovery) <br>
- [ClawHub skill page](https://clawhub.ai/jezjsa/formpass-agent) <br>
- [Publisher profile](https://clawhub.ai/user/jezjsa) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for command examples; the skill itself is instruction-only and does not generate files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
