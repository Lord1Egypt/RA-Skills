## Description:

Track parcels and shipments via the 17TRACK API with local SQLite storage, status polling, webhook ingestion, and daily reports with delivered-package cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[f-liva](https://clawhub.ai/user/f-liva)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to register tracking numbers, poll shipment status, summarize delivery events, and maintain a local package-tracking database through 17TRACK.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracking numbers, carrier data, optional parameters, language settings, token-authenticated requests, and label-derived tags may be sent to 17TRACK.

Mitigation: Use this skill only when sharing shipment data with 17TRACK is acceptable, and avoid labels or tags that contain sensitive personal or business information.

Risk: The optional webhook path can accept and store untrusted data too broadly, and signature rejection and request-size limits are not fixed.

Mitigation: Prefer manual polling over webhooks, keep the webhook server bound to localhost, and do not expose it externally until signature enforcement and request-size limits are addressed.

Risk: The daily report removes delivered packages from the local database.

Mitigation: Run the daily report only when delivered-package cleanup is desired, or use manual sync and list commands when retaining delivered records matters.

## Reference(s):

- [17TRACK](https://www.17track.net/)
- [17TRACK API](https://api.17track.net/)
- [17TRACK Tracking API v2.2 Endpoint](https://api.17track.net/track/v2.2)
- [17TRACK Carrier Metadata](https://res.17track.net/asset/carrier/info/apicarrier.all.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands and status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TRACK17_TOKEN for API calls and stores tracking data in a local SQLite database.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
