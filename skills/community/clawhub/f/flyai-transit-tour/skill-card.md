## Description: <br>
中转不浪费 helps travelers find 6-15 hour connecting-flight options that can support a safe half-day transit-city visit, with flight comparison, POI planning, visa checks, time-buffer calculations, and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers use this skill to compare transit itineraries and decide whether a 6-15 hour layover can support a safe city visit. It produces transit-city sightseeing plans with time buffers, visa notes, direct-flight comparison, destination hotels or attractions, and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask the agent to install or upgrade the FlyAI CLI using global @latest packages, and its fallback guidance includes sudo. <br>
Mitigation: Verify the package and source before installation, prefer a user-scoped Node environment such as nvm, and do not approve sudo or global @latest installation without review. <br>
Risk: The skill includes a TLS troubleshooting path that disables certificate verification for FlyAI commands. <br>
Mitigation: Do not disable TLS certificate validation by default; resolve certificate or network configuration problems before running travel searches. <br>
Risk: The skill can read and persist travel-profile data through memory tools or a local ~/.flyai/user-profile.md file. <br>
Mitigation: Ask for user confirmation before saving preferences, and review or delete stored profile data when the user does not want travel preferences reused. <br>
Risk: The skill can surface booking links and travel recommendations that may affect purchases or itinerary decisions. <br>
Mitigation: Review booking links before purchase and confirm visa, baggage, timing, and itinerary details with official providers. <br>


## Reference(s): <br>
- [Workflow](reference/workflow.md) <br>
- [Flight Search Reference](reference/search-flight.md) <br>
- [POI / Attraction Search Reference](reference/search-poi.md) <br>
- [Hotel Search Reference](reference/search-hotel.md) <br>
- [Keyword Search Reference](reference/keyword-search.md) <br>
- [AI Search Reference](reference/ai-search.md) <br>
- [Train Search Reference](reference/search-train.md) <br>
- [Marriott Hotel Search Reference](reference/search-marriott-hotel.md) <br>
- [Marriott Package Search Reference](reference/search-marriott-package.md) <br>
- [Airport Layover Guide](reference/airport-guide.md) <br>
- [User Profile Storage](reference/user-profile-storage.md) <br>
- [Examples](reference/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown travel plan with tables, timelines, command snippets, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include FlyAI booking links, visa notes, time-buffer calculations, and saved travel-profile preferences when the user consents.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
