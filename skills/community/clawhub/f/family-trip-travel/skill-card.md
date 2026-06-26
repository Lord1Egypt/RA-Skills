## Description: <br>
Helps agents produce family-friendly travel plans by using a disclosed travel-search CLI for hotels, flights, attractions, packages, images, and booking links when a destination is provided, while switching to text-only guidance when the user asks for non-booking advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuckonit](https://clawhub.ai/user/zuckonit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to turn family travel requests into practical itineraries, hotel and attraction comparisons, booking references, and pre-trip checklists that account for children, stroller needs, nap timing, weather alternatives, single-parent travel, allergies, and ticket-rule caveats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send travel details such as destination, dates, child age, family composition, budget, and special needs to an external travel-search provider. <br>
Mitigation: Use it only with a trusted @fly-ai/flyai-cli installation, avoid entering unnecessary sensitive details, and request text-only advice when searches or booking links are not desired. <br>
Risk: Booking details, prices, child ticket rules, cancellation terms, allergy accommodations, and accessibility information may be incomplete or change after search results are returned. <br>
Mitigation: Confirm these details on the booking page or directly with the hotel, airline, attraction, or provider before purchase or travel. <br>
Risk: Optional API-key configuration may expose provider access if reused across environments. <br>
Mitigation: Use a dedicated API key for this CLI and rotate or revoke it if it is no longer needed. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [flyai CLI Capabilities and Family Travel Mapping](references/cli-capabilities.md) <br>
- [Professional Family Trip Output Guidance](references/output-professional.md) <br>
- [Family Query Patterns](references/family-queries.md) <br>
- [Family Hotel Search Guidance](references/search-hotels-family.md) <br>
- [Family Flight Search Guidance](references/search-flight-family.md) <br>
- [Family POI Search Guidance](references/search-poi-family.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zuckonit/family-trip-travel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown travel-planning guidance with tables, checklists, optional shell commands, images, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search-backed recommendations should use provider-returned images and booking links when available; prices, child ticket rules, cancellation terms, allergy needs, and accessibility details should be confirmed on the booking page or with the provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
