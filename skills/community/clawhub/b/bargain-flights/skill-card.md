## Description: <br>
Helps users find hidden-city flight opportunities by comparing one-way direct fares with connecting itineraries that pass through the intended destination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coder-0x7fffffff](https://clawhub.ai/user/coder-0x7fffffff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search one-way hidden-city flight options, compare them with direct-flight prices, and present booking links with baggage, return-ticket, and airline-policy cautions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hidden-city ticketing may conflict with airline policies and creates baggage, return-ticket, missed-segment, and itinerary-change risks. <br>
Mitigation: Use only when the user explicitly wants hidden-city ticketing, disclose the policy and baggage risks before purchase, and prefer one-way itineraries without checked baggage. <br>
Risk: The skill can activate for ordinary cheap-flight requests and may present skipped-segment booking guidance. <br>
Mitigation: Present direct-flight comparison results first, label hidden-city options clearly, and treat the skipped-segment strategy as an optional choice that requires explicit user understanding. <br>
Risk: Generated QR-code links send booking URLs to a third-party QR provider, which may expose personal, session, or tracking data embedded in those URLs. <br>
Mitigation: Avoid QR generation for sensitive booking URLs unless the user accepts the data-sharing risk; use a direct or sanitized booking link when possible. <br>
Risk: Flight searches depend on the external FlyAI CLI and Feizhu service. <br>
Mitigation: Install the FlyAI CLI only from the referenced npm package, review it before use, and avoid entering credentials or secrets into generated commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/coder-0x7fffffff/bargain-flights) <br>
- [bargain-flights reference](references/bargain-flights.md) <br>
- [FlyAI CLI package](https://www.npmjs.com/package/@fly-ai/flyai-cli) <br>
- [Feizhu flight service endpoint](https://a.feizhu.com) <br>
- [QR Server API](https://api.qrserver.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and guidance with JSON helper-script output and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes generated booking QR-code URLs and hidden-city travel risk notices when presenting results.] <br>

## Skill Version(s): <br>
1.0.8 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
