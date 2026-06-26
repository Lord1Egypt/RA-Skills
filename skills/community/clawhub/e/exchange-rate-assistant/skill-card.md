## Description: <br>
exchange_rate_assistant helps users query exchange rates, calculate currency conversions, analyze exchange-rate trends, and retrieve historical exchange rates for major global currencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luokeer52](https://clawhub.ai/user/luokeer52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill for exchange-rate lookups, currency conversion calculations, trend analysis, and historical rate checks. Developers or operators can run the included client scripts to send requests to the configured Prana/Claw service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, API keys, and payment-history requests to the configured Prana/Claw service. <br>
Mitigation: Install only if you trust that service with the data being sent, and avoid submitting sensitive prompts unless approved for that environment. <br>
Risk: API key handling can leave credential material available to the local runtime. <br>
Mitigation: Use scoped and revocable credentials, set PRANA_SKILL_SKIP_WRITE_API_KEY=1 when plaintext key caching is not acceptable, and delete any generated config/api_key.txt after use. <br>
Risk: Prior conversation context can carry over through the stored thread ID. <br>
Mitigation: Use --new-session when a request should not reuse previous conversation context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luokeer52/exchange-rate-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and service-returned JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include session thread IDs; payment-history links should be passed directly to the user without logging.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
