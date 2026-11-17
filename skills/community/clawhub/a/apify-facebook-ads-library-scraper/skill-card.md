## Description:

Searches Meta’s public Ad Library by advertiser or keyword and returns ad creative, dates, platforms, and metrics Meta discloses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harshmaur](https://clawhub.ai/user/harshmaur)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers, researchers, and developers can search public Meta ads by advertiser or keyword to review creative, compare campaign timelines, and export disclosed ad data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify runs incur usage charges, and searches are processed by the hosted service.

Mitigation: Review current pricing and result limits before running; cap requested results to the research need.

Risk: The Apify token grants access to the user's Apify account.

Mitigation: Keep the token private and provide it only through the intended authentication mechanism.

Risk: Recurring schedules or app delivery can continue sending results after the user no longer needs them.

Mitigation: Enable schedules and delivery only when requested, and disable schedules when finished.

## Reference(s):

- [Apify MCP integration documentation](https://docs.apify.com/platform/integrations/mcp)
- [Scraper data and usage gotchas](artifact/references/gotchas.md)

## Skill Output:

**Output Type(s):** [JSON, CSV, Text, Markdown guidance]

**Output Format:** [Structured ad records with a concise human-readable summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some spend, impression, reach, and audience metrics are not disclosed for every ad; media links may expire.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
