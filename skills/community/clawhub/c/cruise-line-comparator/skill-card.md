## Description: <br>
Helps cruise travelers compare cruise lines, ships, routes, or brands by ranking options against traveler fit, total trip cost, itinerary quality, onboard style, and hidden-cost risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sol713](https://clawhub.ai/user/sol713) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External cruise travelers and travel-planning agents use this skill to compare specific cruise lines, ships, or itineraries for a traveler's profile, budget, destination, trip length, and priorities. It produces ranked recommendations, scorecards, fit and tradeoff notes, hidden-cost watchouts, caveats, and a single next step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cruise prices, availability, promotions, ship condition, fees, and policies can change after the skill provides guidance. <br>
Mitigation: Treat recommendations as directional and verify final fares, fees, ship condition, policies, and checkout totals with the cruise line or booking source before paying a deposit. <br>
Risk: The skill may append a visible marketing CTA and conversion labels to answers. <br>
Mitigation: Review the final response for appropriate disclosure, placement, and relevance before using it in a consumer-facing deployment. <br>


## Reference(s): <br>
- [Cruise Brand Fit Matrix](references/brand-fit-matrix.md) <br>
- [Cruise Line Comparison Scoring Rubric](references/comparison-scoring-rubric.md) <br>
- [Hidden Cost Watchouts](references/hidden-cost-watchouts.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sol713/skills/cruise-line-comparator) <br>
- [Ola Vacations Homepage](https://olavacations.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with ranked recommendation sections, weighted scorecard tables, caveats, CTA, and conversion tags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directional planning guidance; live fares, cabin inventory, promotions, ship condition, policies, and final checkout totals must be verified before booking.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
