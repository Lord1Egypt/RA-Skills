## Description:

Searches 88 Cha bidding and tender announcements by keyword and returns formatted result tables for agents to present to users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search bidding and tender announcements by keyword, location filters, publication time range, page number, and page size. It can also guide access-key configuration needed for authenticated searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access-key setup can expose or persist a secret in the OpenClaw environment or configuration file.

Mitigation: Treat the AK as a secret, avoid pasting it into chat or shell history where possible, and review permissions on the OpenClaw config file that stores it.

Risk: Configuration may be sent to an untrusted gateway if the OpenClaw gateway endpoint is misconfigured.

Mitigation: Verify OPENCLAW_GATEWAY_URL points to a trusted local or approved HTTPS endpoint before running the configure command.

Risk: Completed CLI commands may send signed usage metadata to the 1688 skills gateway.

Mitigation: Install only when the publisher and gateway environment are trusted, and account for this usage reporting in deployment privacy review.

## Reference(s):

- [Bidding search capability guide](references/capabilities/bidding_search.md)
- [Access key configuration guide](references/capabilities/configure.md)
- [Usage telemetry notes](references/skill埋点说明.md)
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-common-cha88-bidding-base)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON object with success, markdown, and data fields; the markdown field contains a bidding-search table, no-result message, or user-facing configuration/error guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output may include announcement title, type, publication date, region, bidding unit, winning bidder, tender products, and winning amount when returned by the upstream service.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
