## Description: <br>
Book Calendly meetings instantly from natural-language requests without sending a scheduling link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dompi123](https://clawhub.ai/user/Dompi123) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
People who schedule meetings use this skill to book Calendly events from a natural-language request, including attendee details, timezone, and requested time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real Calendly bookings through the user's Calendly account. <br>
Mitigation: Confirm the attendee name, email, timezone, event type, and meeting time before booking. <br>
Risk: The skill requires a Calendly API token for account access. <br>
Mitigation: Use a revocable Calendly token and remove it from OpenClaw config when the skill is no longer used. <br>


## Reference(s): <br>
- [Calendly API and Webhooks](https://calendly.com/integrations/api_webhooks) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/Dompi123/calendly-quick-book) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with booking status messages and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CALENDLY_API_TOKEN and can create Calendly bookings through the user's account.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
