## Description: <br>
Find and monitor gas prices with daily notifications. Use when searching for the cheapest gas in a specific area, tracking Costco and other discount fuel stations, or setting up daily gas price alerts. Supports any US location with configurable radius and fuel type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GustavoZiaugra](https://clawhub.ai/user/GustavoZiaugra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search for US gas stations by ZIP code or coordinates, compare estimated fuel prices, and configure daily fuel-price notifications. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: ZIP codes or coordinates may be sent to external mapping or gas-price services during searches. <br>
Mitigation: Install and run the skill only when sharing searched locations with those services is acceptable. <br>
Risk: Displayed prices and non-Columbus search results may be approximate or incomplete. <br>
Mitigation: Treat prices as estimates unless using a real price source, and verify important results with the station or a current fuel-price service. <br>
Risk: Scheduled alerts can continue sending location-based requests after the user no longer needs them. <br>
Mitigation: Review cron alert configuration and disable recurring searches when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/GustavoZiaugra/gas-price-alert) <br>
- [Locations Reference](references/locations.md) <br>
- [ZIP Codes Reference](references/zip_codes.md) <br>
- [OpenStreetMap Overpass API](http://overpass-api.de/api/interpreter) <br>
- [GasBuddy](https://www.gasbuddy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, cron configuration snippets, and JSON station results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Gas prices may be estimates, and station coverage depends on external mapping and price services.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
