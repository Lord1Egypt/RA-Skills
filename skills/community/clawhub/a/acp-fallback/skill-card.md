## Description: <br>
Automatically retries ACP vendors in priority order on failure and returns the first successful result with fallback logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[engibarian](https://clawhub.ai/user/engibarian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to route agent tasks through a prioritized ACP fallback chain when a preferred vendor or model fails. It is suited to resilient agent execution workflows where retries, provider switching, and fallback logging are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact references a local fallback shell wrapper that is not included. <br>
Mitigation: Use the skill only with a trusted, reviewed wrapper script and verify the script path and behavior before installing. <br>
Risk: Automatic fallback can retry the same task across multiple AI providers. <br>
Mitigation: Use it only for prompts approved for all configured providers, and remove or disable providers that are not approved for sensitive work. <br>
Risk: Fallback logs may record local execution details. <br>
Mitigation: Set appropriate access controls and retention for fallback logs, or avoid sensitive tasks when logging is enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/engibarian/acp-fallback) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fallback command guidance and operational logging expectations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
