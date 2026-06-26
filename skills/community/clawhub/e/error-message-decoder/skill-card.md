## Description: <br>
Error Message Decoder helps agents interpret common error messages, identify likely causes, and suggest practical fixes with multilingual support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HonestQiao](https://clawhub.ai/user/HonestQiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and support agents use this skill to decode common runtime, network, file, API, and service errors into likely causes and suggested next steps. It is most useful for lightweight troubleshooting guidance before consulting authoritative logs or product documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting suggestions are generic and may not fit the user's exact runtime, framework, or deployment environment. <br>
Mitigation: Treat the output as a starting point and verify fixes against logs, documentation, and environment-specific configuration before applying changes. <br>
Risk: Broad error-related trigger phrases may activate the skill when a narrower diagnostic response is expected. <br>
Mitigation: Invoke it intentionally for error-message analysis and confirm the language and scope of the response before relying on the guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HonestQiao/error-message-decoder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, JSON] <br>
**Output Format:** [Structured JSON-style troubleshooting summary or Markdown explanation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May respond in Chinese or English depending on the requested language; recommendations are generic debugging hints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
