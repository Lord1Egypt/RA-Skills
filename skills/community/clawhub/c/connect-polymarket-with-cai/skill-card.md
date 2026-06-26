## Description: <br>
Connect Polymarket to your CAI account using platforms_supported_list and platform_one_click_register when F-16 applies; wallet derivation via catalog driver. Requires platform or full API scope. Powered by CAI.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernardtai](https://clawhub.ai/user/bernardtai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to link a user's Polymarket account with CAI so the agent can register, retrieve profile or balance data, and use vault-backed credential metadata without exposing secrets in chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive CAI API keys, wallet derivation flows, private-key fallback paths, and platform vault credentials. <br>
Mitigation: Treat these credentials as sensitive, confirm platform identity and requested scopes, and avoid echoing secrets in chat. <br>
Risk: Polymarket registration or linking may require human steps such as CAPTCHA or regional gate checks. <br>
Mitigation: Use a human verification link when needed and do not present registration as fully automatic when external checks are required. <br>


## Reference(s): <br>
- [CAI skill reference](https://cai.com/skill.md) <br>
- [CAI onboarding reference](https://cai.com/skill-references/onboarding.md) <br>
- [CAI developers](https://cai.com/developers.html) <br>
- [ClawHub skill page](https://clawhub.ai/bernardtai/connect-polymarket-with-cai) <br>
- [Publisher profile](https://clawhub.ai/user/bernardtai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell command and ordered tool-call steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAI_API_KEY and may involve wallet or platform vault credentials.] <br>

## Skill Version(s): <br>
1.0.15 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
