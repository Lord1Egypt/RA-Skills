## Description: <br>
Austrian public transport (VOR AnachB) for all of Austria. Query real-time departures, search stations/stops, plan routes between locations, and check service disruptions. Use when asking about Austrian trains, buses, trams, metro (U-Bahn), or directions involving public transport in Austria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manmal](https://clawhub.ai/user/manmal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up Austrian public transport stations, real-time departures, routes, and current service disruptions. It is useful for travel planning involving Austrian trains, buses, trams, metro service, and cross-border routes covered by the underlying transit API. <br>

### Deployment Geography for Use: <br>
Global; transit lookups and route planning are focused on Austria. <br>

## Known Risks and Mitigations: <br>
Risk: Station names or other arguments containing quotes or unexpected characters can produce malformed API requests. <br>
Mitigation: Use ordinary station names, station IDs, and small numeric counts; prefer JSON-safe request construction before production deployment. <br>
Risk: Large numeric counts can create oversized transit API requests or responses. <br>
Mitigation: Keep result counts small and appropriate for a single lookup. <br>
Risk: The skill depends on a disclosed external transit API for live results. <br>
Mitigation: Treat returned departures, routes, and disruptions as live transit data that may vary with API availability and provider updates. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/manmal/a-nach-b) <br>
- [VOR AnachB HAFAS API Endpoint](https://vao.demo.hafas.de/gate) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [JSON responses from shell scripts with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; results depend on the live transit API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
