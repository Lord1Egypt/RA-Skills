## Description: <br>
Alias of air-train-ev. Unified travel + mobility skill: (1) flight pricing with Amadeus (flight offers), (2) public transport/train journey planning with Navitia (journeys, departures), and (3) find nearby EV charge points using Open Charge Map. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaureli](https://clawhub.ai/user/aaureli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up flight prices, public transport or train journeys, and nearby EV charge points through the aliased air-train-ev tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The alias runs scripts from the canonical air-train-ev skill, so the effective API behavior is controlled by that local implementation. <br>
Mitigation: Review and trust the canonical air-train-ev skill before installing or executing this alias. <br>
Risk: Live travel and EV charging lookups require third-party API credentials. <br>
Mitigation: Use scoped, revocable API keys for Amadeus, Navitia, and Open Charge Map and rotate them if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaureli/air-train-ev-alias) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text responses with script-backed lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured Amadeus, Navitia, and Open Charge Map credentials for live lookup behavior.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
