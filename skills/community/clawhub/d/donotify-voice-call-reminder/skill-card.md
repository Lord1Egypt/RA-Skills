## Description: <br>
Send immediate voice call reminders or schedule future calls via DoNotify. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MicahelE](https://clawhub.ai/user/MicahelE) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to check DoNotify usage, place immediate voice-call reminders, and schedule future reminder calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends reminder text and call scheduling details to DoNotify, and those details may be spoken aloud in a phone call. <br>
Mitigation: Confirm the date, time, timezone, title, and spoken description with the user before placing or scheduling a call. <br>
Risk: The skill requires a DoNotify API token and endpoint URL. <br>
Mitigation: Keep DONOTIFY_API_TOKEN private and set DONOTIFY_URL only to the intended DoNotify endpoint. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/MicahelE/donotify-voice-call-reminder) <br>
- [DoNotify OpenClaw homepage](https://donotifys.com/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls] <br>
**Output Format:** [Markdown guidance with HTTP request details and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DONOTIFY_API_TOKEN and DONOTIFY_URL; reminder title and description may be spoken in voice calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
