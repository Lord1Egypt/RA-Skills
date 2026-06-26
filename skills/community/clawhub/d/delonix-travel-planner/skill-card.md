## Description: <br>
Plans business travel by comparing rail, flight, hotel, map, weather, itinerary, budget, and booking-link options, then can generate an HTML travel report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external business travelers, and travel coordinators use this skill to gather trip requirements, compare transportation and hotel options, estimate budgets, and prepare a shareable itinerary report. <br>

### Deployment Geography for Use: <br>
Global; strongest practical support is for China-focused rail, map, hotel, and travel-search providers described by the artifact. <br>

## Known Risks and Mitigations: <br>
Risk: Trip dates, destinations, meeting locations, budgets, and preferences may be shared with external map, search, travel, and booking providers. <br>
Mitigation: Install only when this sharing is acceptable, use scoped Amap API keys, and avoid entering unnecessary sensitive trip details. <br>
Risk: Generated HTML reports and booking links may contain private travel details or outdated prices and availability. <br>
Mitigation: Keep reports private and verify booking links, prices, and availability directly with providers before acting. <br>
Risk: Optional MCP packages can extend the execution surface of the agent environment. <br>
Mitigation: Review optional MCP packages before enabling them and deploy only the integrations needed for the travel-planning workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chaoliuzhu/delonix-travel-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, HTML, files, configuration, guidance] <br>
**Output Format:** [Conversational planning guidance with optional generated HTML travel report, booking links, budget tables, and itinerary details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on external travel, map, search, and booking providers; prices, availability, and booking links should be verified before action.] <br>

## Skill Version(s): <br>
9.9.9 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
