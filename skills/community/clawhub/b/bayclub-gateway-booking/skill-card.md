## Description: <br>
Book and manage tennis and pickleball courts at Bay Club Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elizabethsiegle](https://clawhub.ai/user/elizabethsiegle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Bay Club members can ask an agent to check tennis or pickleball court availability and book an available slot at Bay Club Gateway. The skill can run browser automation with Bay Club credentials and can optionally create a Google Calendar event after a booking. <br>

### Deployment Geography for Use: <br>
United States (Bay Club Gateway, San Francisco, California) <br>

## Known Risks and Mitigations: <br>
Risk: The skill can finalize a real Bay Club court reservation using the user's account. <br>
Mitigation: Confirm the sport, date, time, club, and reservation details with the user before running any booking command. <br>
Risk: The security review notes that the artifact can add hardcoded partners and accept checkboxes before submitting a reservation. <br>
Mitigation: Review or modify the booking path before use so the partner selection is explicit and required acknowledgements are shown before submission. <br>
Risk: The optional Google Calendar integration can write events to a configured calendar. <br>
Mitigation: Use least-privilege calendar credentials, confirm the target calendar, and disable calendar credentials if calendar writes are not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elizabethsiegle/bayclub-gateway-booking) <br>
- [Bay Club Connect](https://bayclubconnect.com/home/dashboard) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Google Calendar](https://calendar.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Console text and JSON result objects from a TypeScript/Node command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, Bay Club account credentials, and optional Google Calendar credentials with calendar write access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
