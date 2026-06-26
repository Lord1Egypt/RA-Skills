## Description: <br>
AI Travel Agent helps users plan single-destination or multi-stop trips by searching flights, hotels, and ground transport through SerpAPI, suggesting seasonal destinations, and optionally using calendar availability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[floogles](https://clawhub.ai/user/floogles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to compare real travel options, build costed itineraries, and refine routes before booking through external providers. It provides search results and booking links only; it does not book travel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [AI Travel Agent on ClawHub](https://clawhub.ai/floogles/ai-travel-agent) <br>
- [SerpAPI](https://serpapi.com) <br>
- [SerpAPI Reference](references/serpapi.md) <br>
- [Seasonal Destination Guide](references/seasonal-destinations.md) <br>
- [Multi-Stop Route Templates](references/multi-stop-routes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with itinerary options, cost comparisons, booking links, and optional shell commands for travel searches.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a user-provided SERPAPI_KEY from the environment or documented credential files. Risk mitigations: store the key only in the documented locations, avoid passing keys as CLI arguments, review trip details before sending searches to SerpAPI, and approve optional calendar access only when availability checks or calendar events are wanted.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
