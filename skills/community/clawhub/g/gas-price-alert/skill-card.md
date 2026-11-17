## Description:

Find and monitor gas prices for U.S. locations with daily notifications, configurable radius and fuel type, and emphasis on Costco and other discount stations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gustavoziaugra](https://clawhub.ai/user/gustavoziaugra)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to search nearby gas stations, estimate discount-station fuel prices, save station results, and configure recurring gas-price alerts for U.S. locations.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Location searches and repeated scheduled alerts can disclose a user's travel area to external services.

Mitigation: Use scheduled alerts only when repeated location queries are acceptable, and limit queries to the minimum location detail and radius needed.

Risk: Fuel prices and station rankings may be inaccurate because the skill relies on estimates, OpenStreetMap coverage, and Columbus-specific logic.

Mitigation: Treat results as planning guidance, verify prices with station apps or GasBuddy before purchase, and test or adjust the location logic before relying on non-Columbus results.

Risk: The Overpass request uses an unencrypted endpoint.

Mitigation: Change the Overpass endpoint to HTTPS before production or privacy-sensitive use.

## Reference(s):

- [Gas Price Alert - US City Coordinates](references/locations.md)
- [Columbus, OH Area ZIP Codes](references/zip_codes.md)
- [OpenStreetMap Overpass API](http://overpass-api.de/api/interpreter)
- [GasBuddy](https://www.gasbuddy.com)
- [Costco Warehouse Locations](https://www.costco.com/warehouse-locations)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown-style summaries, JSON station records, shell command examples, and scheduled alert configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write station results to a configured JSON output file; price values are often estimates or N/A.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
