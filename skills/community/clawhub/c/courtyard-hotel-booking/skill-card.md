## Description: <br>
Searches Courtyard by Marriott hotels and returns real-time prices, booking links, hotel details, and package offers through connected travel-platform APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search Courtyard-only hotel results, inspect hotel details, and compare package offers with booking links. It provides travel search guidance and handoff links; it does not complete reservations or payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search terms, dates, and hotel names are sent to a configured proxy service to retrieve real-time results. <br>
Mitigation: Configure PROXY_URL only to a trusted HTTPS endpoint, protect PROXY_TOKEN, and avoid entering unnecessary personal details in search fields. <br>
Risk: Prices, availability, policies, and package details can change after the skill returns results. <br>
Mitigation: Verify final rates, policies, and availability on the returned booking page before making a reservation. <br>
Risk: The skill returns external booking links and does not handle payments or complete bookings inside the agent. <br>
Mitigation: Complete reservations and payment only on trusted external booking pages after reviewing the destination URL and terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/courtyard-hotel-booking) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text containing hotel search results, hotel details, package listings, prices, and external booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prices and availability are real-time and may change; reservations and payments occur through external links.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
