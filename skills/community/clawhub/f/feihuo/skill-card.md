## Description: <br>
飞伙 helps agents search flights, hotels, trains, visas, travel insurance, Eurail passes, point-to-point rail journeys, and ferry tickets through the feihuo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bitbrewing](https://clawhub.ai/user/bitbrewing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travel-assistant agents and developers use this skill to turn travel-search requests into feihuo CLI commands and present returned booking options in Chinese Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a local access token for authenticated travel-search requests. <br>
Mitigation: Keep ~/.openclaw/qclaw/user-info.json private and do not paste or log its accessToken. <br>
Risk: Travel-search and booking results may include external purchase links. <br>
Mitigation: Review booking links before purchase and install only if the feihuo-cli package and Feihuo service are trusted with travel-search data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bitbrewing/feihuo) <br>
- [Publisher Profile](https://clawhub.ai/user/bitbrewing) <br>
- [一起飞·飞伙](https://yiqifei.net) <br>
- [Flight Search Reference](references/flight-search.md) <br>
- [Hotel Search Reference](references/hotel-search.md) <br>
- [Train Search Reference](references/train-search.md) <br>
- [Visa Search Reference](references/visa-search.md) <br>
- [Insurance Search Reference](references/insurance-search.md) <br>
- [Eurail Pass Search Reference](references/eur-rail-pass-search.md) <br>
- [Eurail P2P Resolve Reference](references/eur-rail-p2p-resolve-local.md) <br>
- [Eurail P2P Search Reference](references/eur-rail-p2p-search.md) <br>
- [Ship Resolve Reference](references/ship-resolve-local.md) <br>
- [Ship Search Reference](references/ship-search.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and an authenticated feihuo CLI; booking links should be reviewed before purchase.] <br>

## Skill Version(s): <br>
2.0.0-beta2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
