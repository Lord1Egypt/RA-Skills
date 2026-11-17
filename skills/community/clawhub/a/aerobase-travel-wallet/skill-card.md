## Description:

Credit cards, loyalty balances, transfer partners, and transfer bonuses. Calculates CPP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurosh87](https://clawhub.ai/user/kurosh87)

### License/Terms of Use:

MIT

## Use Case:

External users and travel rewards agents use this skill to inspect linked travel wallet data, find transfer opportunities, compare credit cards, and calculate cents-per-point from fare and mileage context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose linked travel rewards wallet data through responses from the Aerobase service.

Mitigation: Use it only with an Aerobase API key you are comfortable connecting to the agent environment, and avoid sharing bank passwords, OTPs, cookies, or loyalty account credentials.

Risk: Raw API keys could be disclosed if an agent repeats environment values or request headers.

Mitigation: Follow the skill protocol by using the Authorization Bearer header and redacting API keys in output as sk_live_***.

Risk: Quota limits, authentication failures, or service errors may prevent complete wallet or transfer-bonus results.

Mitigation: Handle 401, 403, 429, timeout, and 5xx responses as documented, retry transient failures once, and return partial guidance with clear next steps when needed.

Risk: Cents-per-point calculations can be misleading if fare amounts or displayed miles are incorrect.

Mitigation: Validate required parameters and compute CPP only from user-provided fare numbers and displayed miles.

## Reference(s):

- [Aerobase homepage](https://aerobase.app)
- [Aerobase OpenClaw travel agent setup](https://aerobase.app/openclaw-travel-agent)
- [ClawHub skill page](https://clawhub.ai/kurosh87/skills/aerobase-travel-wallet)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Markdown]

**Output Format:** [Concise text or Markdown summaries of travel rewards data, transfer options, wallet balances, and cents-per-point calculations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AEROBASE_API_KEY for Aerobase API access; responses should redact raw API keys and present top options before follow-up actions.]

## Skill Version(s):

3.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
