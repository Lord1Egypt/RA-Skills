## Description:

Connect Polymarket to a CAI account using CAI platform discovery, one-click registration when available, and wallet derivation through the catalog driver.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernardtai](https://clawhub.ai/user/bernardtai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, agent developers, and trading or research agents use this skill to link a CAI account with Polymarket and retrieve platform account data after registration. It supports CAI platform credential setup while reminding users that CAPTCHA, regional gates, or other human verification may still be required.

### Deployment Geography for Use:

Global, subject to Polymarket regional availability and verification requirements.

## Known Risks and Mitigations:

Risk: The skill may require broad CAI API access or platform credentials to connect the user's CAI account to Polymarket.

Mitigation: Use the narrowest platform-specific CAI credential that supports the task, and avoid full API scope unless CAI clearly requires it for this exact connection flow.

Risk: The wallet setup path includes a raw private-key fallback that could expose funds if pasted into chat or generic tool fields.

Mitigation: Use a website or wallet-controlled flow when possible, and do not paste wallet private keys or seed phrases into chat.

Risk: Registration can be blocked by CAPTCHA, regional gates, or other human verification requirements.

Mitigation: Pause automated registration when verification is required and use the skill's human verification handoff guidance.

## Reference(s):

- [CAI skill reference](https://cai.com/skill.md)
- [CAI onboarding reference](https://cai.com/skill-references/onboarding.md)
- [CAI developers](https://cai.com/developers.html)
- [ClawHub skill page](https://clawhub.ai/bernardtai/skills/connect-polymarket-with-cai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and ordered platform tool-flow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CAI platform tool names, credential setup guidance, and human verification handoff guidance.]

## Skill Version(s):

1.0.15 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
