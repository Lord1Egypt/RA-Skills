## Description: <br>
Track parcels and shipments via the 17TRACK API with a local SQLite database, automatic status polling, webhook ingestion, and daily reports with auto-cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[f-liva](https://clawhub.ai/user/f-liva) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to track parcels through 17TRACK, maintain a local shipment database, poll for delivery updates, ingest optional webhooks, and generate daily shipment reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a 17TRACK API token and maintains a local shipment database. <br>
Mitigation: Install only in environments where the token can be protected, avoid echoing TRACK17_TOKEN, and review local data retention needs before use. <br>
Risk: Webhook mode may accept or store payloads without rejecting invalid or missing signatures. <br>
Mitigation: Prefer polling with sync unless real-time webhook updates are required; if webhooks are enabled, bind locally or place the endpoint behind trusted network controls and configure TRACK17_WEBHOOK_SECRET. <br>
Risk: Daily reports automatically remove delivered packages from the local tracking database. <br>
Mitigation: Review or disable daily-report cleanup when delivery history must be retained. <br>


## Reference(s): <br>
- [17TRACK](https://www.17track.net/) <br>
- [17TRACK API](https://api.17track.net/) <br>
- [17TRACK Tracking API v2.2](https://api.17track.net/track/v2.2) <br>
- [17TRACK carrier metadata endpoint](https://res.17track.net/asset/carrier/info/apicarrier.all.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown and command-line text with optional JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a 17TRACK API token for API-backed tracking operations; stores package records in a local SQLite database.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
