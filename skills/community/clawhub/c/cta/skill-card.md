## Description:

Chicago CTA transit provides real-time L train arrivals, bus predictions, service alerts, and route information for Chicago public transit queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianleach](https://clawhub.ai/user/brianleach)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to answer Chicago CTA transit questions, including train arrivals, bus predictions, route lookups, nearby stops, fares, and active service alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Train and bus commands require CTA developer API keys that are sent as query parameters to CTA's official HTTPS APIs.

Mitigation: Install only in trusted environments, keep API keys in environment variables or a local .env file, and use keys only for CTA API access.

Risk: GTFS refresh downloads and extracts CTA schedule data into a local cache under the user's home directory.

Mitigation: Review local storage expectations before running refresh-gtfs and remove or refresh the cache according to local policy.

Risk: Transit answers depend on CTA API availability and the freshness of live and cached schedule data.

Mitigation: Treat results as operational guidance, check active service alerts, and refresh GTFS data when CTA schedules change.

## Reference(s):

- [CTA Train Tracker API](https://www.transitchicago.com/developers/traintracker/)
- [CTA Train Tracker API key application](https://www.transitchicago.com/developers/traintrackerapply/)
- [CTA Bus Tracker API](https://www.transitchicago.com/developers/bustracker/)
- [CTA Customer Alerts API](https://www.transitchicago.com/developers/alerts/)
- [CTA GTFS static feed](https://www.transitchicago.com/downloads/sch_data/google_transit.zip)
- [ClawHub skill page](https://clawhub.ai/brianleach/skills/cta)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with optional shell commands and transit result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include real-time CTA arrivals, predictions, alerts, route information, and setup guidance for required API keys.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
