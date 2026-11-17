## Description:

AI phone receptionist for any business that can scrape a website or use a knowledge base, create a VAPI voice assistant, connect a Twilio phone number, and log calls to HubSpot CRM with optional SMS follow-ups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windseeker1111](https://clawhub.ai/user/windseeker1111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business operators use this skill to set up an AI phone receptionist that answers caller questions from business content, connects a phone number, and records call outcomes in CRM. It is intended for customer-facing reception workflows that require careful credential, consent, and webhook controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The webhook can receive public call events and trigger billable CRM or SMS actions without authentication.

Mitigation: Add a shared secret or signature validation, apply rate limits, and avoid exposing the webhook publicly until those controls are in place.

Risk: SMS follow-ups and CRM logging may create consent, privacy, or regulatory obligations for callers.

Mitigation: Keep SMS follow-up disabled until caller consent, transcript handling, retention, and CRM data policies are confirmed.

Risk: Automatic Twilio number purchase can create unexpected costs.

Mitigation: Use an existing Twilio number or require explicit purchase confirmation before buying a new number.

Risk: Installation pulls dependencies and browser assets into the local environment.

Mitigation: Install in an isolated virtual environment and pin dependencies before production use.

## Reference(s):

- [FlowConcierge ClawHub skill page](https://clawhub.ai/windseeker1111/skills/flowconcierge)
- [windseeker1111 ClawHub publisher profile](https://clawhub.ai/user/windseeker1111)
- [VAPI](https://vapi.ai)
- [Twilio](https://twilio.com)
- [HubSpot](https://hubspot.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python command examples, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local shell configuration during installation and may trigger external VAPI, Twilio, and HubSpot API actions when used with credentials.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
