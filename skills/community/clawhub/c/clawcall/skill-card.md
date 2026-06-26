## Description: <br>
ClawCall lets an agent place real US phone calls, navigate phone menus and hold time, optionally bridge the user into a live call, and return call outcomes, transcripts, and recording links when available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shreyjindal81](https://clawhub.ai/user/shreyjindal81) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to delegate routine US phone work to an AI agent, including booking, confirming, rescheduling, cancelling, checking order or appointment status, comparing options across businesses, and configuring ClawCall voice, personality, and inbound reserved-number behavior. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real US phone calls that may create bookings, cancellations, payments, or other commitments. <br>
Mitigation: Give the agent explicit call limits and decision boundaries, and use live handoff before sensitive, negotiable, payment, identity-verification, or irreversible actions. <br>
Risk: The skill stores ClawCall API key and user phone-number state locally. <br>
Mitigation: Treat the saved key and phone number as sensitive user data, and review or delete ~/.config/clawcall/key.json when retained access is not desired. <br>
Risk: Calls may involve private information, verification steps, or recording and transcript links. <br>
Mitigation: Do not invent or disclose private details, bridge the user for live verification when needed, and handle transcripts and recording URLs as sensitive outputs. <br>


## Reference(s): <br>
- [ClawCall homepage](https://clawcall.dev) <br>
- [ClawHub skill page](https://clawhub.ai/shreyjindal81/clawcall) <br>
- [API contract](references/api-contract.md) <br>
- [Outbound calls](references/outbound-calls.md) <br>
- [Inbound reserved numbers](references/inbound-reserved-numbers.md) <br>
- [Account linking and data](references/account-linking-and-data.md) <br>
- [Errors and limits](references/errors-and-limits.md) <br>
- [Profile and personality](references/profile-and-personality.md) <br>
- [Examples](references/examples.md) <br>
- [Pressure scenarios](evals/pressure-scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, configuration, guidance] <br>
**Output Format:** [JSON over HTTPS with agent-facing summaries and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Terminal call results can include lifecycle, outcome, talk_seconds, transcript, and recording_url; saved local state can include an API key and user phone number.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
