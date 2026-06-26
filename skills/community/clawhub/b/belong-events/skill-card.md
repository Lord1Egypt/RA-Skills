## Description: <br>
Discover events and hubs, manage branding, CheckIn venues, bracelets, wallets, and NFT tickets on the Belong platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nomadcalendar](https://clawhub.ai/user/nomadcalendar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External event attendees and organizers use this skill to discover Belong events and hubs, link accounts, and manage event, venue, check-in, bracelet, wallet, branding, custom-domain, and NFT ticket workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an authenticated agent broad control over events, venues, payments, bracelets, wallets, withdrawals, branding, custom domains, and NFT ticket workflows. <br>
Mitigation: Require explicit approval before any create, update, delete, payment, check-in, bracelet, wallet, withdrawal, branding, custom-domain, or NFT-ticket action. <br>
Risk: BELONG_EVENTS_API_KEY is a sensitive account-linked credential sent to the configured Belong endpoint. <br>
Mitigation: Treat the key as a secret, store it only in trusted environment or configuration storage, and avoid sharing files that contain it. <br>
Risk: An endpoint override can route credentials and action requests away from the default Belong service. <br>
Mitigation: Use the default Belong endpoint unless the alternate BELONG_EVENTS_ENDPOINT is intentionally trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nomadcalendar/belong-events) <br>
- [nomadcalendar publisher profile](https://clawhub.ai/user/nomadcalendar) <br>
- [Belong OpenClaw skill proxy endpoint](https://join.belong.net/functions/v1/openclaw-skill-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON responses from shell-invoked JSON-RPC calls, with markdown guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and BELONG_EVENTS_API_KEY for protected actions; BELONG_EVENTS_ENDPOINT can override the default endpoint.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
