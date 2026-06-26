## Description: <br>
Order food delivery via browser automation from trusted calendar events, with Direct and Discovery modes for DoorDash, Uber Eats, and Grubhub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ThisIsJeron](https://clawhub.ai/user/ThisIsJeron) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users with logged-in delivery accounts use this skill to turn trusted calendar events into direct restaurant orders or criteria-based restaurant discovery, then review a pre-checkout summary before any live purchase is placed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a logged-in Chrome profile with saved delivery accounts, payment methods, and addresses to place real food orders. <br>
Mitigation: Use it only when comfortable granting that account access, and require review of restaurant, items, address, fees, tip, total, ETA, and payment method before confirming. <br>
Risk: Calendar events from shared calendars or external invites may not reflect the user's intent. <br>
Mitigation: Trigger ordering only from calendar events the user created, and call out externally modified events in the pre-confirmation summary. <br>
Risk: Incorrect allergy or dietary handling could create unsafe food choices. <br>
Mitigation: Treat allergy and dietary constraints as mandatory, skip ambiguous items, and do not proceed when allergen safety cannot be confirmed. <br>


## Reference(s): <br>
- [DoorDash Browser Flow](references/doordash.md) <br>
- [Grubhub Browser Flow](references/grubhub.md) <br>
- [Uber Eats Browser Flow](references/ubereats.md) <br>
- [DoorDash](https://www.doordash.com) <br>
- [Grubhub](https://www.grubhub.com) <br>
- [Uber Eats](https://www.ubereats.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with inline browser-automation tasks, confirmation prompts, and JSON state-tracking examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces live ordering guidance and requires user confirmation before checkout.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
