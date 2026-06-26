## Description: <br>
Provides multi-dimensional A-share stock analysis across financial metrics, technical indicators, valuation, shareholder holdings, market sentiment, brokerage forecasts, K-line charts, filings, announcements, news, and exchange Q&A. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luokeer52](https://clawhub.ai/user/luokeer52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request A-share stock analysis and related market context through a Prana/Claw wrapper. Developers can run it through the provided Python or Node client when they need an agent-callable stock-analysis capability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock-analysis prompts are sent to a remote Prana/Claw service for processing. <br>
Mitigation: Use service-specific credentials and avoid putting unrelated secrets or sensitive personal information in prompts. <br>
Risk: The wrapper can store its API credentials in config/api_key.txt. <br>
Mitigation: Keep config/api_key.txt private and set PRANA_SKILL_SKIP_WRITE_API_KEY=1 when credentials should not be written to disk. <br>
Risk: Generated stock analysis may be incomplete, stale, or unsuitable as the sole basis for financial decisions. <br>
Mitigation: Review results against authoritative market sources and apply human judgment before acting on investment-related output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luokeer52/getmeastock) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [skill.yaml](skill.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain-text stock-analysis response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market analysis returned from the remote Prana/Claw service and threaded follow-up context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
