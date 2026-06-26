## Description: <br>
Find, book, change, and cancel flights through BonBook using email-based travel requests and human-approved checkout steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aSzelem](https://clawhub.ai/user/aSzelem) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Travelers and their agents use this skill to search flight options, book trips, and manage changes or cancellations through BonBook. The workflow is designed for email-based requests, with explicit human confirmation for account setup, traveler data entry, payments, bookings, changes, cancellations, and optional calendar sync. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight booking and account setup can involve sensitive personal, itinerary, and payment information. <br>
Mitigation: Use the skill only with explicit human approval for account creation, traveler data entry, payment, booking, changes, cancellations, and calendar sync; keep sensitive payment and identity entry on BonBook's approved website channel. <br>
Risk: Agent email permissions may expose broader mailbox access than the booking workflow itself requires. <br>
Mitigation: Limit skill use to messages to and from book@bonbook.co where possible, and have the human review offers, checkout pages, confirmations, cancellation details, and refund eligibility before final action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aSzelem/book-flight) <br>
- [BonBook access](https://bonbook.co/access) <br>
- [BonBook terms](https://bonbook.co/terms) <br>
- [BonBook privacy](https://bonbook.co/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Markdown instructions and plain-text email workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires existing email send and receive permissions; optional web, calendar, and form-completion actions require explicit human approval.] <br>

## Skill Version(s): <br>
2.4.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
