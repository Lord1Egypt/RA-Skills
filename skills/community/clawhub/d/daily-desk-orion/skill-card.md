## Description: <br>
Get a daily pre-session crypto market brief with BTC bias, Korean exchange flows, whale activity, Fear & Greed index, and macro context valid for 24 hours. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokoju007](https://clawhub.ai/user/kokoju007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Portfolio agents, trading bots, and orchestrators use this skill to request a same-day crypto market baseline before a session opens. It summarizes BTC direction, Korean exchange activity, whale movement, Fear & Greed, and macro context, with an optional paid Orion ACP path for structured JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic phrases such as "morning brief" may invoke this skill unexpectedly. <br>
Mitigation: Confirm the user wants the Daily Desk crypto brief before invoking the skill or automating the trigger phrases. <br>
Risk: The Orion ACP upgrade is a paid daily call path. <br>
Mitigation: Ask for explicit confirmation before hiring Orion on ACP or scheduling paid recurring calls. <br>
Risk: Crypto market outputs are time-sensitive and may be incomplete or inaccurate. <br>
Mitigation: Verify the brief against trusted market data before using it for portfolio, trading, or automation decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kokoju007/daily-desk-orion) <br>
- [Orion ACP listing](https://app.virtuals.io/virtuals/1809) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown daily brief with optional structured JSON from Orion ACP] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily market snapshot is valid for 24 hours and should be checked against trusted market sources before trading or automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
