## Description: <br>
Check EV charger availability (favorites, nearby search) via Google Places. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Borahm](https://clawhub.ai/user/Borahm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators use this skill to check EV charger availability for saved favorites, place IDs, or nearby locations and to receive a notification when a charger becomes available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence notes that the referenced charger CLI is missing from the artifact. <br>
Mitigation: Confirm the trusted charger CLI source and install it before relying on scheduled availability checks. <br>
Risk: Google Places requests require an API key and may reveal location queries to the API provider. <br>
Mitigation: Use a restricted, quota-limited GOOGLE_PLACES_API_KEY and only check locations you intend to share with Google Places. <br>
Risk: Cron or Telegram notifications can expose charger locations and availability details through the notification channel. <br>
Mitigation: Enable notifications only for locations you are comfortable sending through that channel and configure scheduling or quiet hours as needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Borahm/charger) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and one-line shell notification output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOOGLE_PLACES_API_KEY and stores notification state under ~/.cache/charger-notify.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
