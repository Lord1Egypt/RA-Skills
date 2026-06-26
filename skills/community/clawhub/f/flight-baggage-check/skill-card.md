## Description: <br>
Checks airline baggage compliance, carry-on versus checked rules, excess baggage, and the cheapest compliant packing plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinayunyunyun](https://clawhub.ai/user/tinayunyunyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-support agents use this skill to answer baggage compliance questions, decide whether items should be carried on or checked, identify overweight or oversize baggage, and rank compliant packing options by cost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live baggage rules and prices can change or require logged-in airline tools, which may make cost recommendations incomplete. <br>
Mitigation: Use official airline or authority sources for rules and mark unverifiable prices as pending official confirmation. <br>
Risk: The skill may use flight-helper, flyai or browser tools for live lookups, which can expose unnecessary travel or booking details if over-shared. <br>
Mitigation: Share only the minimum itinerary, baggage and item details needed for the check, and avoid booking credentials or unrelated personal information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tinayunyunyun/flight-baggage-check) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/tinayunyunyun) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Simplified Chinese Markdown report with compliance verdict, recommended plan, and special notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires official baggage and special-item rule evidence when producing reports; prices that cannot be verified should be marked as pending official confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
