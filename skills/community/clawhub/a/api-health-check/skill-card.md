## Description: <br>
Check the health and status of popular AI APIs and services -- OpenAI, Anthropic, Pollinations, OpenRouter, Gemini, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudcompile](https://clawhub.ai/user/cloudcompile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to check whether common AI API services are responding and to troubleshoot apparent service outages or connectivity problems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The health-check script disables normal TLS verification, so a network attacker or proxy could spoof service health results. <br>
Mitigation: Treat results as advisory, restore TLS verification before operational reliance, and confirm important incidents with trusted status pages or independent checks. <br>
Risk: The skill contacts several public AI service domains when checking all APIs. <br>
Mitigation: Install only when those outbound checks are acceptable, and request a specific service check when broad network contact is unnecessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cloudcompile/api-health-check) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/cloudcompile) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Console status table with optional Markdown troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports per-service UP or DOWN status, HTTP status details, and response time in milliseconds for all configured services or a named service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
