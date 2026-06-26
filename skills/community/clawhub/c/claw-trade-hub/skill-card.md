## Description: <br>
Claw Trade Hub provides a Python WebSocket client for service listings, bids, negotiations, and transaction record management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangboheng](https://clawhub.ai/user/tangboheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect to a Claw-Service-Hub WebSocket endpoint and manage service marketplace flows such as listing creation, bid handling, negotiations, cancellations, price updates, and transaction history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security depends on the WebSocket hub selected by the user; unsafe or untrusted hubs can affect trading, accounting, or settlement workflows. <br>
Mitigation: Install only when the hub is trusted, use wss:// outside local testing, and require server-side authentication and authorization for bid acceptance, listing changes, batch cancellations, and transaction creation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangboheng/claw-trade-hub) <br>
- [Publisher profile](https://clawhub.ai/user/tangboheng) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [Python module and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the websockets Python package, and HUB_URL for the target WebSocket hub.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
