## Description: <br>
Validate URLs and JSON schemas against format rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CutTheMustard](https://clawhub.ai/user/CutTheMustard) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to validate URL, JSON Schema, email, and phone-number formats through an external validation service after user consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validation requests send submitted values to an external service. <br>
Mitigation: Confirm user consent before validation and avoid submitting secrets, confidential payloads, or sensitive personal data unless sharing is acceptable. <br>
Risk: The skill documents a paid x402 query option. <br>
Mitigation: Use the free tier when appropriate and confirm any paid validation flow before initiating it. <br>


## Reference(s): <br>
- [Data Validate ClawHub page](https://clawhub.ai/CutTheMustard/data-validate) <br>
- [Validation service homepage](https://validate.agentutil.net) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with curl examples and JSON validation responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user consent before sending user-provided data to the external validation service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
