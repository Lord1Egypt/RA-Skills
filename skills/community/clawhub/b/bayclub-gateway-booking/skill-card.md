## Description:

Book and manage tennis/pickleball courts at Bay Club.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elizabethsiegle](https://clawhub.ai/user/elizabethsiegle)

### License/Terms of Use:


## Use Case:

External users can ask an agent to check Bay Club Gateway tennis or pickleball court availability and attempt a court reservation for a requested day and time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The booking action can make real Bay Club reservations with too little user confirmation.

Mitigation: Require an explicit final confirmation from the user before attempting any booking.

Risk: The automation may accept page checkboxes or choose booking partners automatically.

Mitigation: Review selections before execution and avoid blanket checkbox acceptance or automatic partner selection.

Risk: Google Calendar integration uses credentials and calendar access that may be broader than needed.

Mitigation: Use narrowly scoped calendar credentials, restrict the target calendar, and store credentials outside the skill directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elizabethsiegle/skills/bayclub-gateway-booking)
- [Publisher profile](https://clawhub.ai/user/elizabethsiegle)
- [Bay Club Connect](https://bayclubconnect.com/home/dashboard)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [JSON result objects and console text from TypeScript browser automation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform real booking side effects and optionally create Google Calendar events when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
