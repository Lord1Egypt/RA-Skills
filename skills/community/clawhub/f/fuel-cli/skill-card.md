## Description:

Fuel CLI helps agents check UK petrol and diesel prices, find nearby stations by postcode or coordinates, inspect station details, and request structured JSON or projected fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shan8851](https://clawhub.ai/user/shan8851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to run the Fuel CLI for UK station search, fuel-price comparison, station lookup, and structured fuel-price data retrieval.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned global npm CLI, so the installed command may change over time.

Mitigation: Review the npm package before installing and prefer a pinned version or local install where possible.

Risk: Live data access requires Fuel Finder OAuth credentials.

Mitigation: Store FUEL_FINDER_CLIENT_ID and FUEL_FINDER_CLIENT_SECRET securely outside committed files.

Risk: Setting FUEL_FINDER_BASE_URL to an untrusted endpoint could expose requests or credentials.

Mitigation: Only set FUEL_FINDER_BASE_URL to a trusted HTTPS Fuel Finder endpoint.

Risk: Cached or stale price data could lead to outdated fuel-price decisions.

Mitigation: Check data.quality.advisories and freshnessCounts, and use refresh behavior when current prices matter.

## Reference(s):

- [Fuel CLI homepage](https://fuel-cli.xyz)
- [UK Fuel Finder service](https://www.fuel-finder.service.gov.uk)
- [ClawHub skill page](https://clawhub.ai/shan8851/skills/fuel-cli)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON envelope examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports TTY text output, piped JSON output, field projection with --output <path>, structured error envelopes, and data-quality advisories.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
