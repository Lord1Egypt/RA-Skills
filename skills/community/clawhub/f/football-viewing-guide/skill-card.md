## Description:

Builds dated, country-specific football broadcast guides from FotMob schedules or Flashscore match listings without promising streaming access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Football viewers and their assistants use this skill to find listed matches and broadcasters for a chosen market and date window, with local kick-off times and source links where available.

### Deployment Geography for Use:

Global; listings depend on the selected viewer market.

## Known Risks and Mitigations:

Risk: Football lookup parameters and the Crawlora API key are sent to Crawlora.

Mitigation: Use only if that disclosure is acceptable, and provide the key through the CRAWLORA_API_KEY environment variable.

Risk: Fixture times and broadcaster listings may change, and a listed channel does not guarantee viewing access.

Mitigation: Show the collection time and viewer market, flag conflicting times, and avoid claiming subscription inclusion or playable streams.

## Reference(s):

- [Football Viewing Guide on ClawHub](https://clawhub.ai/crawlora-org/skills/football-viewing-guide)
- [Endpoint reference](artifact/reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown fixture table with market-specific channels, local dates and times, and source links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies the viewer market and timezone; notes missing or out-of-window coverage and does not promise streaming access.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
