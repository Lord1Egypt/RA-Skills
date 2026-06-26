## Description: <br>
Search for campgrounds, check availability and book campsites across the entire world. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jsuppers](https://clawhub.ai/user/jsuppers) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search campground, glamping, and RV listings, inspect amenities and reviews, check date-specific availability, and retrieve booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a third-party npm MCP server. <br>
Mitigation: Install and use it only when you trust Campertunity and the campertunity-ai-tools package. <br>
Risk: Booking links can lead users to external providers that may request trip, account, or payment information. <br>
Mitigation: Verify the booking provider before sharing sensitive information or completing a reservation. <br>
Risk: Direct availability is not supported for every listing. <br>
Mitigation: Treat manual availability links as handoff points and confirm availability directly with the provider when needed. <br>


## Reference(s): <br>
- [Campertunity homepage](https://campertunity.com) <br>
- [ClawHub skill page](https://clawhub.ai/jsuppers/campertunity) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jsuppers) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with setup JSON, campground result tables, availability summaries, and booking links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the Campertunity MCP server through npx or campertunity-ai-tools; some listings may provide a manual availability link instead of direct availability results.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
