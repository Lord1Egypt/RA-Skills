## Description: <br>
Deprecated CTG Travel Booking helps agents guide users through CTG travel searches, bookings, cancellations, and refunds for flights, hotels, trains, and attraction tickets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaosai](https://clawhub.ai/user/xiaosai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-service agents use this skill to collect trip details, present CTG travel options, and execute booking, cancellation, or refund flows after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, cancel, or refund real travel bookings. <br>
Mitigation: Require the agent to show a final summary and obtain explicit user confirmation before any booking, cancellation, or refund action. <br>
Risk: Passenger identity data and contact details may be collected or saved during booking flows. <br>
Mitigation: Use the skill only with a trusted CTG account and API key, and provide only the passenger information needed for the requested transaction. <br>
Risk: This release is marked as expired and no longer maintained. <br>
Mitigation: Prefer the newer CTG Travel skill linked in the artifact before installing or using this release. <br>
Risk: Misconfigured endpoints or transport settings could send travel data to an unintended service. <br>
Mitigation: Verify the HTTPS CTG endpoint in configuration before running API-backed workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaosai/ctg-travel-booking) <br>
- [Publisher profile](https://clawhub.ai/user/xiaosai) <br>
- [Latest CTG Travel skill](https://clawhub.ai/ctg-travel/ctg-travel) <br>
- [CTG skill access guide](https://pro-m.ourtour.com/new-journey/static-page/openClawGuide) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration or request parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-facing travel options, booking summaries, refund summaries, and operational instructions for CTG API-backed flows.] <br>

## Skill Version(s): <br>
0.2.5 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
