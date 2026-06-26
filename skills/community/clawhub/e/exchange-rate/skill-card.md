## Description: <br>
Real-time forex and cryptocurrency exchange rate lookup and amount conversion powered by QVeris. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ax2](https://clawhub.ai/user/ax2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to look up exchange rates and convert amounts between supported fiat or cryptocurrency pairs through QVeris-backed tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Currency pairs, amounts, and optional dates are sent to QVeris for lookup and conversion. <br>
Mitigation: Use a scoped or revocable QVeris API key where available, and avoid sending sensitive transaction details unless that data sharing is acceptable. <br>
Risk: Returned exchange rates may be unsuitable as the sole basis for financial, contractual, or compliance decisions. <br>
Mitigation: Treat results as reference data and verify important rates against an authoritative source before making binding decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ax2/exchange-rate) <br>
- [QVeris](https://qveris.ai) <br>
- [QVeris API endpoint](https://qveris.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [Human-readable Markdown or machine-readable JSON containing exchange-rate or conversion results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QVERIS_API_KEY; supports rate and convert modes, optional historical date, and configurable request timeout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
