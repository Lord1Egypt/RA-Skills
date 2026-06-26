## Description: <br>
Booking.com international hotel booking assistant for hotel search, room availability, price comparison, review lookup, and reservation-management workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers, employees, and travel coordinators use this skill to search international hotels, compare rooms and prices, review cancellation policies, and manage Booking.com-oriented reservation flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that the skill advertises live Booking.com booking support while returning hardcoded hotel, room, price, policy, and review data as successful results. <br>
Mitigation: Replace mock responses with verified Booking.com API responses before relying on availability, prices, taxes, reviews, cancellation policy, or booking prompts. <br>
Risk: Booking and cancellation workflows can affect real travel plans if acted on without clear user approval. <br>
Mitigation: Require explicit user confirmation before any booking or cancellation action, showing verified hotel, dates, guests, room, price, taxes, and cancellation terms first. <br>


## Reference(s): <br>
- [Booking.com Distribution API getHotels](https://distribution-xml.booking.com/json/bookings.getHotels) <br>
- [Booking.com Distribution API JSON endpoint](https://distribution-xml.booking.com/json) <br>
- [ClawHub skill page](https://clawhub.ai/ryan-zry/business-travel-booking) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Guidance] <br>
**Output Format:** [JSON responses and Markdown-formatted hotel tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; live booking use requires verified Booking.com API credentials and verified API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata, release metadata, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
